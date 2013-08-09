'''
Created on Jul 21, 2013

Twisted network service.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.1

from podroid.comm.commcoreserver import CommCoreServerFactory
from podroid.comm.commcoreclient import CommCoreClientFactory

from podroid.comm.peers.peermanager import PeerManager
from podroid.comm.capsule.capsulemanager import CapsuleManager

from podroid.config.configuration import *

from twisted.internet import reactor

from kivy.logger import Logger

from base64 import b64encode

class CommService(PeerManager, CapsuleManager):
    """
    Twisted communications service.
    Contains both server and client code.
    """
    
    
    def __init__(self, peerid, host, port, serverinit=True, clientinit=True, printer=None):
        "Initialize communication layer."
               
        ## Initialize peer manager
        PeerManager.__init__(self)
        ## Initialize capsule manager
        CapsuleManager.__init__(self)
                
        self.peerid = peerid
        self.host   = host
        self.port   = port
        
        self._printer = printer
                 
        ## Start the listener
        if serverinit:
            self._start_server()
        
        ## Start peer connections
        if clientinit:
            self._start_peer_connections()
               
               
    def _start_server(self):
        "Start twisted server listener."
        
        reactor.listenTCP(self.port, CommCoreServerFactory(self))
        
        
    def _start_peer_connections(self):
        "Start peer connections on start."
        
        ## Connect to all peers
        for (pid, h, p, cs) in self.list_peers():
            
            ## Check conn status
            if not cs:
                ## Start a connection with peer
                conn = self.start_connection(pid, h, p)
                ## Save the connection
                self.add_peer_connection(pid, conn)
            else:
                pass
            
            
    def _update_peer_connection_status(self, peer_ip, status):
        "Change peer conn status based on connection/disconnection"
        
        ## Assuming Peer ID <-> Peer IP one to one relation
        pid = self.get_peerid_from_ip(peer_ip)
        
        if pid:
            return self.update_peer_connection_status(pid, status)
        else:
            return None
        
        
            
    def _write_into_connection(self, conn, data):
        "Write into twisted connection transport."
        
        try:
            conn.transport.write(data)
        except:
            Logger.error( "Connection to peer failed. Please try later." )
            return False
        else:
            return True
        
        
    def _transfer_data(self, pid, data_class, data_content):
        "Transfer data to client with peer id."

        ## Get peer connection
        conn = self.connect_to_peer(pid)
        
        ## Pack data into capsule
        capsule = self.pack_capsule(data_class, data_content, self.peer_host(pid))
        
        ## Send data over connection
        return self._write_into_connection(conn, capsule)
    
    def _print(self, dip, msg):
        
        print_string = constants.GUI_LABEL_PROMPT + dip + " : " + msg
        
        if self._printer:
            self._printer(print_string)
        else:
            Logger.info(print_string)
       
    
    def start_connection(self, pid, host='localhost', port=8000):
        "Start connection with server."
        
        Logger.debug( "Connecting to pid: {}".format(pid) )
        
        return reactor.connectTCP(host, port, CommCoreClientFactory(self))
        
        
    def on_server_connection(self, connection): 
        "Executed on successful server connection."
        
        peer_ip = connection.getPeer().host
        
        ## Update peer connection status to CONNECTED
        self._update_peer_connection_status(peer_ip, True)
    
    
    def on_server_disconnection(self, connection):
        "Executed on successful server disconnection."
        
        peer_ip = connection.getPeer().host
        
        ## Update peer connection status to DISCONNECTED
        self._update_peer_connection_status(peer_ip, False)
        
        
    def handle_response(self, response):
        "Handle response from server"
        
        if len(response) != constants.CAPSULE_SIZE:
            raise Exception('Capsule chunk should be equal to '+str(constants.CAPSULE_SIZE)+'B')
        
        ## Repsonse handling architecture should be placed here.
        (cid, dest_ip, captype, content, _, chksum) = self.unpack_capsule(response)
        
        ## Currently the test case is inbuilt into the pod. --## TEST BEGIN ## 
        if captype == constants.LOCAL_TEST_CAPS_TYPE:
            
            if cid     == constants.LOCAL_TEST_CAPS_ID     and \
               chksum  == constants.LOCAL_TEST_CAPS_CHKSUM and \
               content == constants.LOCAL_TEST_STR         and \
               dest_ip == constants.LOCAL_TEST_HOST:
                Logger.debug( "Sending Message Test Pass." )
            else:
                Logger.debug( """
                Sending Message Test Fail.
                For test to pass, 
                1. Test server must be running.
                2. Command is 'send 888 Hello World!'
                """ )
                
        elif captype == constants.PROTO_MACK_TYPE:
            Logger.debug( "Message ACK recieved from {}".format(dest_ip) )
            
        
    ## ------------------------------------------------
    ## Define Client Protocol defined here
    ## ------------------------------------------------
    
    def pass_message(self, pid, msg):
        "Pass message to client. Capsule Type: BULK"
        
        ## Check to see peer connection status
        if not self.get_peer_connection_status(pid):
            return False
        
        ## Assumed Bulk message transfer
        dtype = constants.PROTO_BULK_TYPE
        
        if msg ==  constants.LOCAL_TEST_STR:
            dtype = constants.LOCAL_TEST_CAPS_TYPE
                           
        ## Send message using send data API       
        return self._transfer_data(pid, dtype, msg)
    
    ## ------------------------------------------------
     
    ## ------------------------------------------------
    ## Server Protocols defined here
    ## ------------------------------------------------
    
    def on_client_connection(self, connection): pass
    
    
    def handle_recieved_data(self, serial):
        
        Logger.debug( "Handling Capsule : {}".format(b64encode(serial)) )
        
        ## Response
        rsp = serial
        
        ## Unpack capsule
        (cid, dip, c_rx_type, msg, _, _) = self.unpack_capsule(serial)
        
        Logger.debug("Received: {}".format( b64encode(serial)) )
        
        ## Source IP should be added into capsule
        sip = dip ## TODO 

        if c_rx_type == "PING":
            rsp =  "PONG" ## Legacy
            
        elif c_rx_type == constants.LOCAL_TEST_CAPS_TYPE:
            self._print(sip, msg)
            pass ## Resend the same msg.
        
        elif c_rx_type == constants.PROTO_BULK_TYPE:
            
            if msg: ## integrity check
                ## Message reciept successful
                self._print(sip, msg)
                rsp = self.pack_capsule(captype=constants.PROTO_MACK_TYPE, capcontent='', dest_host=dip)
            else:
                ## Request for message again
                Logger.error("Tampered capsule received.")
                pass

        Logger.debug( "Responded: {}".format( b64encode(rsp)) )

        return rsp