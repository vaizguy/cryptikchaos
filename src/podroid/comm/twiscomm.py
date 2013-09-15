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

from twisted.internet import reactor, defer

from kivy.logger import Logger

from base64 import b64encode


class CommService(PeerManager, CapsuleManager):

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
        PeerManager.__init__(self, peerid, self.peerkey)
        # Initialize capsule manager
        CapsuleManager.__init__(self, self.peerkey)

        self._printer = printer

        # Start the listener
        if serverinit:
            self._start_server()

        # Start peer connections
        if clientinit:
            self._start_peer_connections()

    def _start_server(self):
        "Start twisted server listener."

        reactor.listenTCP(self.port, CommCoreServerFactory(self))

    def _start_peer_connections(self):
        "Start peer connections on start."

        # Connect to all peers
        for (pid, _, h, p, cs, ) in self.list_peers():

            # Check conn status
            if not cs:
                # Start a connection with peer
                conn = self.start_connection(pid, h, p)
                # Save the connection
                self.add_peer_connection(pid, conn)
            else:
                pass

    def _update_peer_connection_status(self, peer_ip, peer_port, status):
        "Change peer conn status based on connection/disconnection"

        # Assuming Peer ID <-> Peer IP one to one relation
        pid = self.get_peerid_from_ip(peer_ip, peer_port)

        if pid:
            return self.update_peer_connection_status(pid, status)
        else:
            return None

    def _sendLine(self, conn, line):
        "Implementing sendLine method locally."

        return conn.transport.write(line + '\r\n')

    def _write_into_connection(self, conn, stream):
        "Write into twisted connection transport."
        
        try:
            self._sendLine(conn, stream)
        except:
            Logger.error("Connection to peer failed. Please try later.")
            return False
        else:
            return True
        
    def _router(self, pid):
        "Router decides bes route to peer"
        
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

    def _print(self, dip, msg):

        peer_id = str(self.get_peerid_from_ip(dip, constants.PEER_PORT))

        print_string = constants.GUI_LABEL_PROMPT + peer_id + " : " + msg

        if self._printer:
            self._printer(print_string)
        else:
            Logger.info(print_string)

    def start_connection(self, pid, host='localhost', port=constants.PEER_PORT):
        "Start connection with server."

        Logger.debug("Connecting to pid: {}".format(pid))

        return reactor.connectTCP(host, port, CommCoreClientFactory(self))

    def on_server_connection(self, connection):
        "Executed on successful server connection."

        peer_ip = connection.getPeer().host
        peer_port = connection.getPeer().port

        # Update peer connection status to CONNECTED
        self._update_peer_connection_status(peer_ip, peer_port, True)

    def on_server_disconnection(self, connection):
        "Executed on successful server disconnection."

        peer_ip = connection.getPeer().host
        peer_port = connection.getPeer().port

        # Update peer connection status to DISCONNECTED
        self._update_peer_connection_status(peer_ip, peer_port, False)

    def handle_response(self, response):
        "Handle response from server"

        if len(response) != constants.CAPSULE_SIZE:
            raise Exception(
                'Capsule chunk should be equal to ' + str(
                    constants.CAPSULE_SIZE) + 'B')
            return None

        # Repsonse handling architecture should be placed here.
        (cid, dest_ip, src_ip, captype, content,
         _, chksum, pkey) = self.unpack_capsule(response)
         
        ## Get stored peer key
        src_pid = self.get_peerid_from_ip(src_ip)
        ## It maybe from Test server if None
        if not src_pid:
            src_pid = self.get_peerid_from_ip(src_ip, 8888)
            
        stored_pkey = self.get_peer_key(src_pid)
        
        ## Check message authenticity
        if (pkey != stored_pkey):
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
                self._print(src_pid, 
                    "Simple Message Transfer Test Passed.")
            else:
                Logger.debug("""
                Sending Message Test Fail.
                For test to pass,
                1. Test server must be running.
                2. Command is 'send 888 Hello World!'
                """)
                self._print(src_pid, 
                   "Simple Message Transfer Test Failed.")
               
        elif captype == constants.PROTO_MACK_TYPE:
            Logger.debug("Message ACK recieved from {}".format(src_ip))

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
        
        # Check if peer is present
        if self.get_peer(pid):
            self._print(self.peerid, "Peer already in list.")
            return False
        
        # Start a connection with peer
        conn = self.start_connection(pid, host, 8888)

        # Save the connection
        self.add_peer_connection(pid, conn)

        Logger.debug("Sending auth.")
        
        # Pack data into capsule
        stream = self.pack_capsule(
            "AUTH",
            str(self.peerid),
            host,
            self.host)
        
        print dir(conn)
        # Send message using send data API
        return self._write_into_connection(conn, stream)
                
    # ------------------------------------------------

    # ------------------------------------------------
    # Server Protocols defined here
    # ------------------------------------------------

    def on_client_connection(self, connection):
        pass


    def handle_recieved_data(self, serial):

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
        if (pkey != stored_pkey):
            Logger.debug("Capsule unauthenticated.")
            return None

                
        if not self.get_peer(src_pid):
            Logger.error("Got message from unknown pid, {}".format(src_pid))

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
            
        elif c_rx_type == "AUTH":
            
            Logger.debug( "Recieved auth request. {}".format(msg))

        Logger.debug("Responded: {}".format(b64encode(rsp)))

        return rsp