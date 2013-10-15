'''
Created on Jul 21, 2013

Twisted network service.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.2

from cryptikchaos.comm.commcoreserver import CommCoreServerFactory
from cryptikchaos.comm.commcoreclient import CommCoreClientFactory
from cryptikchaos.comm.commcoreauth   import CommCoreAuthFactory


from cryptikchaos.comm.swarm.swarmhandler import SwarmHandler
from cryptikchaos.comm.capsule.capsulemanager import CapsuleManager

from cryptikchaos.config.configuration import *

from twisted.internet import reactor, defer

from kivy.logger import Logger

from base64 import b64encode

import traceback


class CommService(SwarmHandler, CapsuleManager):

    """
    Twisted communications service.
    Contains both server and client code.
    """

    def __init__(self, peerid, peerkey, host, port,
                 serverinit=True, clientinit=True, printer=None):
        "Initialize communication layer."

        self.peerid = peerid
        self.host = host
        self.port = port
        self.peerkey = peerkey
        
        # Initialize peer manager
        SwarmHandler.__init__(self, peerid, self.peerkey)
        # Initialize capsule manager
        CapsuleManager.__init__(self, self.peerkey)

        self._printer = printer

        # Start the listener
        if serverinit:
            self._start_server()

        # Start peer connections
        if clientinit:
            self._start_peer_connections()
            
    def __del__(self):
        
        # Close swarm handler 
        SwarmHandler.__del__(self)
        # Close capsule manager
        CapsuleManager.__del__(self)

    def _start_server(self):
        "Start twisted server listener."

        reactor.listenTCP(self.port, CommCoreServerFactory(self))

    def _start_peer_connections(self):
        "Start peer connections on start."

        # Connect to all peers
        for (pid, _, h, p, cs, ) in self.list_peers():

            # Check conn status
            if not cs:
                self.start_connection(pid, h, p)
            else:
                pass

    def _update_peer_connection_status(self, peer_ip, peer_port, status, conn):
        "Change peer conn status based on connection/disconnection"
        
        # Assuming Peer ID <-> Peer IP one to one relation
        pid = self.get_peerid_from_ip(peer_ip, peer_port)
        
        # Add the peer connection if it doesnt exist
        if status:
            self.add_peer_connection(pid, conn)
        
        if pid:
            return self.update_peer_connection_status(pid, status)
        else:
            return None

    def _sendLine(self, conn, line):
        "Implementing sendLine method locally."

        try:
            r = conn.sendLine(line)
        except:
            r = conn.write(line + '\r\n')
        else:
            return r

    def _write_into_connection(self, conn, stream):
        "Write into twisted connection transport."

        try:
            self._sendLine(conn, stream)
        except:
            Logger.error("Connection to peer failed. Please try later.")
            print traceback.format_exc()
            return False
        else:
            return True
        
    def _router(self, pid):
        "Router decides best route to peer"
        
        return pid

    def _transfer_data(self, pid, data_class, data_content, desthost=None):
        "Transfer data to client with peer id."
        
        # Get peer route.
        peer_route = self._router(pid)

        # Get peer connection
        conn = self.connect_to_peer(peer_route)

        if not desthost:
            desthost = self.peer_host(pid)

        # Pack data into capsule
        stream = self.pack_capsule(
            data_class,
            data_content,
            desthost,
            self.host)
        
        # Send data over connection
        return self._write_into_connection(conn, stream)

    def _print(self, dip, msg, port=constants.PEER_PORT):
       
        peer_id = self.get_peerid_from_ip(dip, port)
        
        print_string = constants.GUI_LABEL_PROMPT + str(peer_id) + " : " + msg

        if self._printer:
            self._printer(print_string)
        else:
            Logger.info(print_string)
            
    def start_connection(self, pid, host='localhost', port=constants.PEER_PORT):
        "Start connection with server."

        Logger.debug("Connecting to pid: {}".format(pid))

        #return reactor.connectTCP(host, port, CommCoreClientFactory(self))
        if reactor.connectTCP(host, port, CommCoreClientFactory(self)):
            return True
        else:
            return False
        
    def start_authentication(self, pid, host='localhost', port=constants.PEER_PORT):
        "Start connection with server."

        Logger.debug(
            "Attempting connection to pid: {} for authentication.".format(pid)
        )

        if reactor.connectTCP(host, port, CommCoreAuthFactory(self)):
            return True
        else:
            return False
        
    def on_server_connection(self, connection):
        "Executed on successful server connection."

        peer_ip = connection.getPeer().host
        peer_port = connection.getPeer().port

        # Update peer connection status to CONNECTED
        self._update_peer_connection_status(peer_ip, peer_port, True, connection)

    def on_server_disconnection(self, connection):
        "Executed on successful server disconnection."

        peer_ip = connection.getPeer().host
        peer_port = connection.getPeer().port

        # Update peer connection status to DISCONNECTED
        self._update_peer_connection_status(peer_ip, peer_port, False, None)
   
    def on_server_authentication(self, connection):
        
        peer_ip = connection.getPeer().host
        peer_port = connection.getPeer().port

        # Pack data into capsule
        stream = self.pack_capsule(
            constants.PROTO_AUTH_TYPE,
            str(self.peerid),
            peer_ip,
            self.host)
        
        return self._write_into_connection(connection, stream)
    
    def handle_response(self, response):
        "Handle response from server"
        
        # Repsonse handling architecture should be placed here.
        # Unpack received stream
        try:
            (cid, dest_ip, src_ip, captype, content,
                 _, chksum, pkey) = self.unpack_capsule(response)
        except:
            raise 
            return None
        else:
            pass
        
        ## Default pid, port, incl because test pod has the same ip
        ## but different port. Need to simplify mapping TODO
        src_pid = constants.PEER_ID
                 
        ## It maybe from Test server if None
        if not self.get_peerid_from_ip(src_ip):
            src_pid = self.get_peerid_from_ip(src_ip, constants.LOCAL_TEST_PORT)
        else:
            src_pid = self.get_peerid_from_ip(src_ip)
        
        # Get previously stored public key
        stored_pkey = self.get_peer_key(src_pid)
        
        ## Check message authenticity
        if (pkey != stored_pkey):
            print pkey, stored_pkey
            Logger.debug("Capsule unauthenticated.")
            return None
        
        # Currently the test case is inbuilt into the pod. --## TEST BEGIN ##
        if captype == constants.LOCAL_TEST_CAPS_TYPE:

            if (cid == constants.LOCAL_TEST_CAPS_ID and
               chksum == constants.LOCAL_TEST_CAPS_CHKSUM and
               content == constants.LOCAL_TEST_STR and
               dest_ip == constants.LOCAL_TEST_HOST and
               src_ip == constants.LOCAL_TEST_HOST):
                Logger.debug("Simple Message Transfer Test Passed.")
                self._print(src_ip, 
                    "Simple Message Transfer Test Passed.", constants.LOCAL_TEST_PORT)
            else:
                Logger.debug("""
                Sending Message Test Fail.
                For test to pass,
                1. Test server must be running.
                2. Command is 'send 888 Hello World!'
                """)
                self._print(src_ip, 
                   "Simple Message Transfer Test Failed.")
               
        elif captype == constants.PROTO_MACK_TYPE:
            Logger.debug("Message ACK recieved from {}".format(src_ip))
            
    def handle_auth_response(self, response):
        "Handle authentication response to add peer."
        
        # Repsonse handling architecture should be placed here.
        (cid, dest_ip, src_ip, captype, content,
         _, chksum, pkey) = self.unpack_capsule(response)
         
        src_port = constants.PEER_PORT

        ## It maybe from Test server if None
        if not self.get_peerid_from_ip(src_ip):
            src_port = constants.LOCAL_TEST_PORT
                   
        if captype == constants.PROTO_AACK_TYPE:
            ## Extract peer id
            pid = int(content)
            ## Add peer
            self.add_peer(pid, pkey, src_ip, src_port)
            ## Add peer connection
            self._update_peer_connection_status(src_ip, src_port, False, None)
            ## Connect to peer using normal connection this should refresh
            ## the connection in db to normal client conn from auth conn 
            self.start_connection(pid, src_ip, src_port)
            return True
        
        return False
     

    # ------------------------------------------------
    # Define Client Protocol defined here
    # ------------------------------------------------
    def pass_message(self, pid, msg):
        "Pass message to client. Capsule Type: BULK"

        # Check to see peer connection status
        if not self.get_peer_connection_status(pid):
            return False

        # Assumed Bulk message transfer
        dtype = constants.PROTO_BULK_TYPE

        if msg == constants.LOCAL_TEST_STR:
            dtype = constants.LOCAL_TEST_CAPS_TYPE

        # Send message using send data API
        return self._transfer_data(pid, dtype, msg)
       
    def add_peer_to_swarm(self, pid, host):
        "Adds a new user through auth request chain"
        
        port = constants.PEER_PORT                
        # Assign port based on pid
        if pid == 888:
            port = constants.LOCAL_TEST_PORT

        
        # Check if peer is present
        if self.get_peer(pid):
            self._print(self.peerid, "Peer already in list.")
            return False
        else:
            # Add peer
            #self.add_peer_unauth(pid, host, port)
            pass
        
        # Start a connection with peer
        if not self.start_authentication(pid, host, port):
            return False
        else:
            return True
    # ------------------------------------------------

    # ------------------------------------------------
    # Server Protocols defined here
    # ------------------------------------------------
    def handle_recieved_data(self, serial, connection):

        Logger.debug("Handling Capsule : {}".format(b64encode(serial)))

        # Response
        rsp = serial

        # Unpack capsule
        (cid, dest_ip, src_ip, c_rx_type, msg, _, _, 
            pkey) = self.unpack_capsule(serial)
                
        ## Get stored peer key
        src_pid = self.get_peerid_from_ip(src_ip)
        stored_pkey = self.get_peer_key(src_pid)
        
        ## Check message authenticity
        if (c_rx_type != constants.PROTO_AUTH_TYPE and pkey != stored_pkey):
            Logger.debug("Capsule unauthenticated.")
            return None
                
        if not self.get_peer(src_pid):
            Logger.error("Unknown pid @{} attempting contact.".format(src_ip))

        Logger.debug("Received: {}".format(b64encode(serial)))

        if c_rx_type == "PING":
            rsp = "PONG"  # Legacy

        elif c_rx_type == constants.LOCAL_TEST_CAPS_TYPE:
            self._print(src_ip, msg)
            ## Repack capsule maintaining the same content
            rsp = self.pack_capsule(
                captype=c_rx_type,
                capcontent=msg,
                dest_host=src_ip,
                src_host=dest_ip)
            
        elif c_rx_type == constants.PROTO_BULK_TYPE:

            if msg:  # integrity check
                # Message reciept successful
                self._print(src_ip, msg)
                rsp = self.pack_capsule(
                    captype=constants.PROTO_MACK_TYPE,
                    capcontent='',
                    dest_host=src_ip,
                    src_host=dest_ip)
            else:
                # Request for message again
                Logger.error("Tampered capsule received.")
                pass
            
        elif c_rx_type == constants.PROTO_AUTH_TYPE:
            
            Logger.debug( "Recieved auth request from Peer: {}".format(msg))
                       
            ## Extract peer id
            pid = int(msg) # Need to check if peerid format is followed. TODO
            
            ## Add peer
            self.add_peer(pid=pid, 
                          key=pkey, 
                          host=src_ip, 
                          port=constants.PEER_PORT)
            
            ## Add peer connection and change status
            self._update_peer_connection_status(src_ip, constants.PEER_PORT, True, connection)

            ## Send current peer info
            rsp = self.pack_capsule(
                    captype=constants.PROTO_AACK_TYPE,
                    capcontent=str(self.peerid),
                    dest_host=src_ip,
                    src_host=self.host)

        Logger.debug("Responded: {}".format(b64encode(rsp)))

        return rsp