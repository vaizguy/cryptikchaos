'''
Created on Jul 21, 2013

Twisted network service.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.5

from cryptikchaos.comm.commcoreserver import CommCoreServerFactory
from cryptikchaos.comm.commcoreclient import CommCoreClientFactory
from cryptikchaos.comm.commcoreauth   import CommCoreAuthFactory

from cryptikchaos.comm.swarm.manager import SwarmManager
from cryptikchaos.comm.stream.manager import StreamManager
from cryptikchaos.comm.stream.manager import STREAM_TYPES

from cryptikchaos.env.configuration import constants

from twisted.internet import reactor

from kivy.logger import Logger

from base64 import b64encode

import traceback


class CommService:

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
        self.swarm_manager = SwarmManager(peerid, peerkey)
        # Initialize capsule manager
        self.stream_manager = StreamManager(peerid, peerkey, host)

        self._printer = printer

        # Start the listener
        if serverinit:
            self._start_server()

        # Start peer connections
        if clientinit:
            self._start_peer_connections()

    def __del__(self):

        Logger.info("Closing managers.")
        
        # Close swarm handler
        self.swarm_manager.__del__()
        # Close capsule manager
        self.stream_manager.__del__()
        
    def _start_server(self):
        "Start twisted server listener."

        reactor.listenTCP(self.port, CommCoreServerFactory(self))

    def _start_peer_connections(self):
        "Start peer connections on start."

        # Connect to all peers
        for (pid, _, h, p, cs, ) in self.swarm_manager.list_peers():

            # Check conn status
            if not cs:
                self.start_connection(pid, h, p)
            else:
                pass

    def _update_peer_connection_status(self, peer_ip, peer_port, status, 
            conn):
        "Change peer conn status based on connection/disconnection."

        # Assuming Peer ID <-> Peer IP one to one relation
        pid = self.swarm_manager.get_peerid_from_ip(
            peer_ip,
            peer_port
        )

        # Add the peer connection if it doesnt exist
        if status:
            self.swarm_manager.add_peer_connection(pid, conn)

        if pid:
            return self.swarm_manager.update_peer_connection_status(
                pid, 
                status
            )
        else:
            return None

    def _sendLine(self, conn, line):
        "Implementing sendLine method locally."
        
        # If capsule packing fails line=None
        if not line:
            Logger.error("No stream to send.")
            return None

        try:
            conn.sendLine(line)
        except:
            conn.write(line + constants.STREAM_LINE_DELIMITER)
        finally:
            return True

    def _write_into_connection(self, conn, stream):
        "Write into twisted connection transport."

        try:
            if not self._sendLine(conn, stream):
                return False
        except:
            Logger.error("Connection to peer failed. Please try later.")
            print traceback.format_exc()
            return False
        else:
            return True

    def _router(self, pid):
        "Router decides best route to peer."

        return pid

    def _transfer_data(self, pid, data_class, data_content, 
            desthost=None):
        "Transfer data to client with peer id."

        # Get peer route.
        peer_route = self._router(pid)

        # Get peer connection
        conn = self.swarm_manager.connect_to_peer(peer_route)

        if not desthost:
            desthost = self.swarm_manager.peer_host(pid)
            
        # Get peer key
        peer_key = self.swarm_manager.get_peer_key(pid)
        
        if not peer_key:
            raise Exception("No valid peer key could be found.")

        # Pack data into capsule
        stream = self.stream_manager.pack_stream(
            stype=data_class,
            content=data_content,
            dest_host=desthost,
            src_host=self.host, 
            peer_key=peer_key
        )

        # Send data over connection
        return self._write_into_connection(conn, stream)
    
    def _get_source_from_connection(self, connection):
        "Return the sender peer's key"
        
        ## Get the sender peer's information from connection
        # Get host
        host = connection.getPeer().host
        # Get port
        port = constants.PEER_PORT
        
        # Test mode check if current service is handling
        # response or recieved data, maybe a peer client or 
        # test server
        if constants.ENABLE_TEST_MODE and self.peerid == constants.PEER_ID:
            port = constants.LOCAL_TEST_PORT
            
        # Get peer ID of stream source
        pid  = self.swarm_manager.get_peerid_from_ip(
            host, 
            port
        )
        # Get the stream source's key
        key = None
        if pid:
            key  = self.swarm_manager.get_peer_key(pid)
            
        return (pid, key)

    def _print(self, msg, dip=constants.PEER_HOST, 
            port=constants.PEER_PORT):
        "Print message on console with peer id."

        # Get peer ID
        peer_id = self.swarm_manager.get_peerid_from_ip(dip, port)

        # Pack the message
        if not peer_id:
            peer_id = self.peerid
        # Print the message
        if self._printer:
            self._printer(msg, peer_id)
        else:
            Logger.info(msg)
            
    def _print_test(self, ctype, content):
        "Print test message."
        
        self._print(
            "<TEST TYPE:{}>{}<TEST>".format(ctype, content),
            dip=constants.LOCAL_TEST_HOST,
            port=constants.LOCAL_TEST_PORT
        )

    def start_connection(self, pid, host='localhost', 
        port=constants.PEER_PORT):
        "Start connection with server."

        Logger.debug("Connecting to pid: {}".format(pid))

        #return reactor.connectTCP(host, port, CommCoreClientFactory(self))
        if reactor.connectTCP(host, port, CommCoreClientFactory(self)):
            return True
        else:
            return False

    def start_authentication(self, pid, host='localhost', 
            port=constants.PEER_PORT):
        "Start connection with server."

        Logger.debug(
            "Attempting connection to pid: {} for authentication.".format(
                pid
            )
        )

        if reactor.connectTCP(host, port, CommCoreAuthFactory(self)):
            return True
        else:
            return False

    def on_server_connection(self, connection):
        "Executed on successful server connection."

        peer_ip = connection.getPeer().host
        peer_port = connection.getPeer().port
        peer_id = self.swarm_manager.get_peerid_from_ip(
            peer_ip, 
            peer_port
        )

        # Announce successful server connection
        self._print(
            "Connected to PID:{}--{}@{}".format(
                peer_id, peer_ip, peer_port
            ),
            peer_ip,
            peer_port
        )

        # Update peer connection status to CONNECTED
        self._update_peer_connection_status(
            peer_ip, 
            peer_port, 
            True, 
            connection
        )

    def on_server_disconnection(self, connection):
        "Executed on successful server disconnection."

        peer_ip = connection.getPeer().host
        peer_port = connection.getPeer().port
        peer_id = self.swarm_manager.get_peerid_from_ip(
            peer_ip, 
            peer_port
        )

        # Announce successful server disconnection
        self._print(
            "Disconnected from PID:{}--{}@{}".format(
                peer_id, peer_ip, peer_port
            ),
            peer_ip,
            peer_port
        )
        
        # Update peer connection status to DISCONNECTED
        self._update_peer_connection_status(peer_ip, peer_port, False, 
            None)

    def on_server_authentication(self, connection):
        "Used to handle server auth requests."

        peer_ip = connection.getPeer().host
        peer_port = connection.getPeer().port

        # Authenticate server connection
        self._print(
            "Authenticating connection to {}@{}".format(
                peer_ip, peer_port
            ),
            peer_ip,
            peer_port
        )
        
        # Pack data into capsule
        stream = self.stream_manager.pack_stream(
            stype=constants.PROTO_AUTH_TYPE,
            content=self.peerid,
            dest_host=peer_ip,
            src_host=self.host,
            flag=STREAM_TYPES.UNAUTH
        )

        return self._write_into_connection(connection, stream)

    def on_server_auth_close(self, connection):
        "Executed on successful closure of authentication connection."

        peer_ip = connection.getPeer().host
        peer_port = connection.getPeer().port

        self._print(
            "Authentication successful to {}@{}".format(peer_ip, peer_port)
        )

    def on_client_connection(self, connection):
        "Execued on successful client connection."

        peer_ip = connection.getPeer().host
        peer_port = connection.getPeer().port

        self._print("Client {}@{} connected.".format(peer_ip, peer_port))
        
    def on_client_disconnection(self, connection):
        "Executed on successful client disconnection."

        peer_ip = connection.getPeer().host
        peer_port = connection.getPeer().port

        self._print(
            "Client {}@{} disconnected.".format(peer_ip, peer_port)
        )

    def handle_response(self, response, connection):
        "Handle response from server."
        
        # Default value of response at server side is None
        # hence we add a check for this at the client side.
        if not response:
            self._print("Error processing response. Got None!")
            return None
        
        ## Get the sender peer's information from connection
        (_, src_key) = self._get_source_from_connection(connection)

        # Repsonse handling architecture should be placed here.
        # Unpack received stream
        try:
            (cid, dest_ip, src_ip, c_rsp_type, content,
                 _, chksum, pkey) = self.stream_manager.unpack_stream(
                response,
                src_key
            )
        except:
            raise
            return None
        else:
            ## Check if stream ID is valid 
            if not cid:
                return None
                                
        # Currently the test case is inbuilt into the pod.
        # MSG TEST BEGIN #
        if c_rsp_type == constants.LOCAL_TEST_STREAM_TYPE:

            if (cid == constants.LOCAL_TEST_STREAM_ID and
               chksum == constants.LOCAL_TEST_STREAM_CHKSUM and
               content == constants.LOCAL_TEST_STR and
               dest_ip == constants.LOCAL_TEST_HOST and
               src_ip == constants.LOCAL_TEST_HOST):
                Logger.debug("Simple Message Transfer Test Passed.")
                self._print(
                    "Simple Message Transfer Test Passed.",
                     src_ip,
                     constants.LOCAL_TEST_PORT
                )
            else:       
                Logger.debug("""
                Sending Message Test Fail.
                For test to pass,
                1. Test server must be running.
                2. Add test server using 'addtest' command.
                3. Begin test with 'sendtest' command.
                """)
                self._print(
                   "Simple Message Transfer Test Failed.",
                   src_ip
                )

        elif c_rsp_type == constants.PROTO_MACK_TYPE:
            Logger.debug("Message ACK recieved from {}".format(src_ip))

    def handle_auth_response(self, response):
        "Handle authentication response to add peer."

        # Repsonse handling architecture should be placed here.
        (cid, dest_ip, src_ip, c_rsp_auth_type, content,
         _, chksum, pkey) = self.stream_manager.unpack_stream(
            response
        )

        src_port = constants.PEER_PORT

        ## It maybe from Test server if None
        if not self.swarm_manager.get_peerid_from_ip(src_ip):
            src_port = constants.LOCAL_TEST_PORT

        if c_rsp_auth_type == constants.PROTO_AACK_TYPE:
            ## Extract peer id
            pid = content
            ## Add peer
            self.swarm_manager.add_peer(pid, pkey, src_ip, src_port)
            ## Add peer connection
            self._update_peer_connection_status(
                src_ip, 
                src_port, 
                False, 
                None
            )
            ## Connect to peer using normal connection this should refresh
            ## the connection in db to normal client conn from auth conn
            self.start_connection(pid, src_ip, src_port)
            return True

        return False

    # ------------------------------------------------
    # Client Protocol Method defined here
    # ------------------------------------------------
    def pass_message(self, pid, msg):
        "Pass message to client. Capsule Type: BULK"

        # Check to see peer connection status
        if not self.swarm_manager.get_peer_connection_status(pid):
            Logger.warn("Peer is offline.")
            self._print("Peer is offline.")
            return False

        # Assumed Bulk message transfer
        dtype = constants.PROTO_BULK_TYPE

        if msg == constants.LOCAL_TEST_STR:
            dtype = constants.LOCAL_TEST_STREAM_TYPE

        # Send message using send data API
        return self._transfer_data(pid, dtype, msg)

    def add_peer_to_swarm(self, pid, host):
        "Adds a new user through auth request chain."

        port = constants.PEER_PORT
        # Assign port based on pid
        if pid == constants.LOCAL_TEST_PEER_ID:
            port = constants.LOCAL_TEST_PORT

        # Check if peer is present
        if self.swarm_manager.get_peer(pid):
            self._print(
                "Peer already in list."
            )
            return False
        else:
            pass

        # Start a connection with peer
        if not self.start_authentication(pid, host, port):
            return False
        else:
            return True
    # ------------------------------------------------

    # ------------------------------------------------
    # Server Protocol Method defined here
    # ------------------------------------------------
    def handle_recieved_data(self, serial, connection):

        Logger.debug("Handling Capsule : {}".format(b64encode(serial)))
        
        ## Get the sender peer's information from connection
        (src_pid, src_key) = self._get_source_from_connection(connection)

        # Response (default = None)
        rsp = None

        # Unpack capsule
        (cid, dest_ip, src_ip, c_rx_type, content, _, _,
            pkey) = self.stream_manager.unpack_stream(serial, src_key)
        
        # Print test message if test server
        if self.peerid == constants.LOCAL_TEST_PEER_ID and \
           c_rx_type in (constants.LOCAL_TEST_STREAM_TYPE):
            self._print_test(c_rx_type, content)
          
        ## ------------------------------------------------------------      
        ## Check if the request is an AUTH request and 
        ## handle it accordingly, this requires no capsule challenge
        ## ------------------------------------------------------------          
        if c_rx_type == constants.PROTO_AUTH_TYPE:

            Logger.debug(
                "Recieved auth request from Peer: {}".format(content)
            )

            ## Extract peer id
            pid = content

            ## Add peer
            self.swarm_manager.add_peer(
                pid=pid,
                key=pkey,
                host=src_ip,
                port=constants.PEER_PORT
            )

            ## Add peer connection and change status
            self._update_peer_connection_status(
                peer_ip=src_ip, 
                peer_port=constants.PEER_PORT, 
                status=True, 
                conn=connection
            )

            ## Send current peer info
            rsp = self.stream_manager.pack_stream(
                stype=constants.PROTO_AACK_TYPE,
                content=self.peerid,
                dest_host=src_ip,
                src_host=self.host,
                flag=STREAM_TYPES.UNAUTH
            )
        
            Logger.debug("Auth Response: {}".format(b64encode(rsp)))

            # Send Auth response
            return rsp
    
        # Check if stream ID is valid 
        if not cid:
            Logger.error("Invalid stream id received from unpacking stream.")
            return rsp

        # Check if connection is recognized
        if not self.swarm_manager.get_peer(src_pid):
            Logger.warn(
                "Unknown pid @{} attempting contact.".format(src_ip)
            )

        Logger.debug("Received: {}".format(b64encode(serial)))

        if c_rx_type == "PING":
            rsp = "PONG"  # Legacy

        elif c_rx_type == constants.LOCAL_TEST_STREAM_TYPE:
                        
            ## Repack capsule maintaining the same content
            rsp = self.stream_manager.pack_stream(
                stype=c_rx_type,
                content=content,
                dest_host=src_ip,
                src_host=dest_ip,
                peer_key=src_key
            )

        elif c_rx_type == constants.PROTO_BULK_TYPE:

            # Message receipt successful
            self._print(content, src_ip)
            # Generate response
            rsp = self.stream_manager.pack_stream(
                stype=constants.PROTO_MACK_TYPE,
                content='',
                dest_host=src_ip,
                src_host=dest_ip,
                peer_key=src_key
            )
        
        if rsp:
            Logger.debug("Responded: {}".format(b64encode(rsp)))

        return rsp