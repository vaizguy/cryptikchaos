'''
Created on Jul 21, 2013

Twisted network service.

This file is part of CryptikChaos.

CryptikChaos is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CryptikChaos is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CryptikChaos. If not, see <http://www.gnu.org/licenses/>.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6.1"

# install_twisted_rector must be called before importing
# and using the reactor
from kivy.support import install_twisted_reactor
install_twisted_reactor()

from kivy.logger import Logger

from cryptikchaos.core.env.configuration import constants
from cryptikchaos.core.comm.commcoreserver import CommCoreServerFactory
from cryptikchaos.core.comm.commcoreclient import CommCoreClientFactory
from cryptikchaos.core.comm.commcoreauth import CommCoreAuthFactory
from cryptikchaos.core.comm.swarm.manager import SwarmManager
from cryptikchaos.core.comm.stream.manager import StreamManager
from cryptikchaos.core.comm.stream.manager import STREAM_TYPES
from cryptikchaos.core.comm.comsec import ComSecCore
if constants.ENABLE_TLS:
    from cryptikchaos.core.comm.sslcontext import TLSCtxFactory
from cryptikchaos.exceptions.streamExceptions import StreamOverflowError
from cryptikchaos.libs.utilities import generate_auth_token

from twisted.internet import reactor


from base64 import b64encode

import traceback


class CommService(object):

    """
    Twisted communications service.
    Contains both server and client code.
    """

    def __init__(self, peerid, host, port,
                 serverinit=True, clientinit=True, printer=None):
        "Initialize communication layer."

        # Initialize Communications security core
        self.comsec_core = ComSecCore()

        # peer client attributes
        self.peerid = peerid
        self.host = host
        self.port = port
        
        # Get device service link
        self._device = None

        # peer key
        self.peerkey = self.comsec_core.get_public_key()

        # TLS variables
        if constants.ENABLE_TLS:
            # SSL cert, key path
            self.sslcrt = "{}/certs/{}.crt".format(
                constants.PROJECT_PATH,
                self.peerid
            )
            self.sslkey = "{}/certs/{}.key".format(
                constants.PROJECT_PATH,
                self.peerid
            )
            self.ssca = "{}/certs/demoCA/cacert.pem".format(
                constants.PROJECT_PATH
            )

        # Initialize peer manager
        self.swarm_manager = SwarmManager(peerid, self.peerkey)
        # Initialize stream manager
        self.stream_manager = StreamManager(peerid, self.peerkey, host)

        # Alias print method
        self._printer = printer

        # Auth request token dictionary, stores all auth request tokens
        # such that all acks can be validated.
        self.valid_auth_req_tokens = {}

        # Start the listener
        if serverinit:
            self.listener = self._start_listener()

        # Start peer connections
        if clientinit:
            self._start_connections()

    def __del__(self):

        # Close swarm handler
        self.swarm_manager.__del__()
        # Close stream manager
        self.stream_manager.__del__()
        # Close twisted listener
        self._stop_listener()
        
    def register_device_service(self, device):
        "Must be called after init."
        
        # Register device service, cannot rebind
        if not self._device:
            self._device = device

    def _start_listener(self):
        "Start twisted server listener."

        if constants.ENABLE_TLS:
            return reactor.listenSSL(
                self.port,
                CommCoreServerFactory(self),
                TLSCtxFactory(
                    self.sslcrt, self.sslkey, self.ssca, self.on_ssl_verification)
            )
        else:
            return reactor.listenTCP(self.port, CommCoreServerFactory(self))       
        
    def _stop_listener(self):
        "Stop twisted server listener"
        
        self.listener.stopListening()        
        Logger.info('COMM: Ended twisted communications!')

    def _start_connections(self):
        "Start peer connections on start."

        # Connect to all peers
        for (pid, _, host, port, cstatus, ) in self.swarm_manager.list_peers():

            # Check conn status
            if not cstatus:
                self.start_connection(pid, host, port)
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

        # If stream packing fails line=None
        if not line:
            Logger.error("COMM: No stream to send.")
            return None

        try:
            conn.sendLine(line)
        except:
            conn.write("{}{}".format(line, constants.STREAM_LINE_DELIMITER))
        finally:
            return True

    def _write_into_connection(self, conn, stream):
        "Write into twisted connection transport."

        try:
            if not self._sendLine(conn, stream):
                return False
        except:
            Logger.error("COMM: Connection to peer failed. Please try later.")
            print traceback.format_exc()
            return False
        else:
            return True

    def _router(self, pid):
        "Router decides best route to peer."

        return pid

    def _pack_auth_content(self, peer_id, request_id):
        "Pack peer ID and request token in to string"
        
        return peer_id + request_id

    def _unpack_auth_content(self, content):
        "Split peer ID and request token from string"
        
        INDX = constants.PEER_ID_LEN
        return (content[:INDX], content[INDX:])

    def _transfer_data(self, pid, data_class, data_content,
                       desthost=None):
        "Transfer data to client with peer id."

        # Get peer route.
        peer_route = self._router(pid)

        # Get peer connection
        conn = self.swarm_manager.connect_to_peer(peer_route)

        # Set destination host IP
        if not desthost:
            desthost = self.swarm_manager.peer_host(pid)

        # Get peer key
        shared_key = self.swarm_manager.get_peer_key(pid)

        if not shared_key:
            raise Exception("No valid peer key could be found.")

        # Content length enforcement.
        try:
            # Pack data into stream
            stream = self.stream_manager.pack_stream(
                stream_type=data_class,
                stream_content=data_content,
                stream_host=desthost,
                shared_key=shared_key
            )

        except StreamOverflowError as SOError:
            self._printer(SOError.info, self.peerid)
            Logger.warn("COMM: " + SOError.info)
            return False

        else:
            # Send data over connection
            return self._write_into_connection(conn, stream)

    def _get_source_from_connection(self, connection):
        "Return the sender peer's key"

        # Get the sender peer's information from connection
        # Get host
        host = connection.getPeer().host
        # Get port
        port = constants.PEER_PORT

        # Test mode check if current service is handling
        # response or received data, maybe a peer client or
        # test server
        if constants.ENABLE_TEST_MODE and \
                self.peerid == constants.PEER_ID:
                port = constants.LOCAL_TEST_PORT

        # Get peer ID of stream source
        pid = self.swarm_manager.get_peerid_from_ip(
            host,
            port
        )

        Logger.debug("COMM: IP: {} Port: {} ".format(host, port))

        # Get the stream source's key
        shared_key = None
        if pid:
            shared_key = self.swarm_manager.get_peer_key(pid)

        return (pid, shared_key, host, port)

    def _print(self, msg, dip=constants.PEER_HOST,
               port=constants.PEER_PORT, notify=False):
        "Print message on console with peer id."
        
        # Get peer ID
        peer_id = self.swarm_manager.get_peerid_from_ip(dip, port)

        # Print with local peer id
        if not peer_id:
            peer_id = self.peerid
        else:
            notify = constants.ENABLE_NOTIFICATIONS

        # Print the message
        if self._printer:
            self._printer(msg, peer_id)
        # Display device notifications
        if self._device:
            if notify:
                self._device.vibrate_cb()
                self._device.notify_cb(
                    title="ID: {}".format(peer_id), 
                    message=msg, 
                    timeout=1
                )
        else:
            Logger.warn("COMM: No device service registered.")
        
        # Log message
        Logger.info("COMM: {} : {}".format(peer_id, msg))

    def _print_test(self, ctype, content):
        "Print test message."

        self._print(
            "<TEST TYPE:{}>{}<TEST>".format(ctype, content),
            dip=constants.LOCAL_TEST_HOST,
            port=constants.LOCAL_TEST_PORT
        )

    def display_peer_host(self, peer_id):
        "Gets the peer IP address."

        peer_ip = self.swarm_manager.peer_host(peer_id)

        if peer_ip:
            self._print("Peer {}--{}".format(peer_id, peer_ip))
        else:
            self._print("Peer not present in swarm.")

    def start_connection(self, pid, host='localhost',
                         port=constants.PEER_PORT):
        "Start connection with server."

        Logger.debug("COMM: Connecting to pid: {}".format(pid))

        # Check if TLS is enable
        if constants.ENABLE_TLS and reactor.connectSSL(
            host,
            port,
            CommCoreClientFactory(self),
            TLSCtxFactory(
                self.sslcrt,
                self.sslkey,
                self.ssca,
                self.on_ssl_verification
            )
        ):
            return True

        # Use normal TCP connection
        elif not constants.ENABLE_TLS and reactor.connectTCP(
            host,
            port,
            CommCoreClientFactory(self)
        ):
            return True

        # Could not establish connection
        else:
            return False

    def start_authentication(self, pid, host='localhost',
                             port=constants.LOCAL_TEST_PORT):
        "Start connection with specified host server."

        Logger.debug(
            "COMM: Initiating authenticated connection with pid: {}.".format(
                pid
            )
        )

        # Save authentication request to map with authentication ack
        self.valid_auth_req_tokens[host] = generate_auth_token()

        # Check if TLS is enabled
        if constants.ENABLE_TLS and reactor.connectSSL(
            host,
            port,
            CommCoreAuthFactory(self),
            TLSCtxFactory(
                self.sslcrt,
                self.sslkey,
                self.ssca,
                self.on_ssl_verification
            )
        ):
            return True

        # Use normal TCP connection
        elif not constants.ENABLE_TLS and reactor.connectTCP(
            host,
            port,
            CommCoreAuthFactory(self)
        ):
            return True

        # Could not establish connection
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

        if peer_id:
            # Announce successful server connection
            self._print(
                constants.GUI_PEER_REPR.format(
                    peer_id, peer_ip, peer_port
                ) + " has entered the swarm.",
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

        # If peer id is valid
        if peer_id:
            # Announce successful server disconnection
            self._print(
                constants.GUI_PEER_REPR.format(
                    peer_id, peer_ip, peer_port
                ) + " has left the swarm.",
                peer_ip,
                peer_port
            )

            # Update peer connection status to DISCONNECTED
            self._update_peer_connection_status(peer_ip, peer_port, False,
                                                None)

            # Delete peer from swarm store
            self.swarm_manager.delete_peer(peer_id)

    def on_server_auth_open(self, connection):
        "Used to handle server auth requests."

        peer_ip = connection.getPeer().host
        peer_port = connection.getPeer().port

        # Authenticate server connection
        self._print(
            "Authenticating connection to {}:{}".format(
                peer_ip, peer_port
            ),
            peer_ip,
            peer_port
        )

        # Get request ID
        request_id = self.valid_auth_req_tokens[peer_ip]
        
        # Pack auth content
        content = self._pack_auth_content(self.peerid, request_id)

        # Pack authentication data into stream
        stream = self.stream_manager.pack_stream(
            stream_type=constants.PROTO_AUTH_TYPE,
            stream_content=content,
            stream_flag=STREAM_TYPES.UNAUTH,
            stream_host=peer_ip
        )

        return self._write_into_connection(connection, stream)

    def on_server_auth_close(self, connection):
        "Executed on successful closure of authentication connection."

        peer_ip = connection.getPeer().host
        peer_port = connection.getPeer().port

        # delete auth request id
        del self.valid_auth_req_tokens[peer_ip]

        self._print(
            "Authentication successful to {}:{}".format(
                peer_ip,
                peer_port
            )
        )

    def on_client_connection(self, connection):
        "Executed on successful client connection."

        peer_ip = connection.getPeer().host
        peer_port = connection.getPeer().port

        self._print("Client {}:{} connected.".format(peer_ip, peer_port))

    def on_client_disconnection(self, connection):
        "Executed on successful client disconnection."

        peer_ip = connection.getPeer().host
        peer_port = connection.getPeer().port

        self._print(
            "Client {}:{} disconnected.".format(peer_ip, peer_port)
        )

    if constants.ENABLE_TLS:
        def on_ssl_verification(self, connection, x509):
            "post ssl verification hook"

            # TODO
            # Add post TLS verification func here
            Logger.info("COMM: TLS Verification is SUCCESSFUL!")

    def handle_response_stream(self, response, connection):
        "Handle response from server."

        # Default value of response at server side is None
        # hence we add a check for this at the client side.
        if not response:
            self._print("Error processing response. Got None!")
            return None

        # Get the sender peer's information from connection
        (_, shared_key, src_ip, _) = self._get_source_from_connection(
            connection
        )

        # Response handling architecture should be placed here.
        # Unpack received stream
        try:
            (
                c_rsp_type,
                content,
                _
            ) = self.stream_manager.unpack_stream(
                stream=response,
                shared_key=shared_key
            )
        except:
            raise
            return None
        else:
            # Check if stream ID is valid
            if not c_rsp_type:
                return None

        # Currently the test case is inbuilt into the pod.
        # MSG TEST BEGIN #
        if c_rsp_type == constants.LOCAL_TEST_STREAM_TYPE:

            if (
                content == constants.LOCAL_TEST_STR and
                src_ip == constants.LOCAL_TEST_HOST
            ):
                Logger.debug("COMM: Simple Message Transfer Test Passed.")
                self._print(
                    "Simple Message Transfer Test Passed.",
                    src_ip,
                    constants.LOCAL_TEST_PORT
                )
            else:
                Logger.debug("""COMM:
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
            Logger.debug("COMM: Message ACK received from {}".format(src_ip))

    def handle_auth_response_stream(self, response, connection):
        "Handle authentication response to add peer."

        # Get the sender peer's information from connection
        (_, _,
         src_ip,
         src_port
         ) = self._get_source_from_connection(connection)

        # Response handling architecture should be placed here.
        (header, content, pkey) = self.stream_manager.unpack_stream(
            stream=response
        )

        if (header == constants.PROTO_AACK_TYPE):
            # Extract peer ID, request ID
            (pid, request_id) = self._unpack_auth_content(content)

            # Check if request ACK ID is valid
            try:
                if self.valid_auth_req_tokens[src_ip] != request_id:
                    Logger.debug(
                        "COMM: Received Invalid Request ACK ID [{}].".format(
                            request_id
                        )
                    )
                    return None

            except KeyError:
                Logger.debug(
                    "COMM: Received Invalid host '{}' request ACK.".format(
                        src_ip
                    )
                )
                return None

            else:
                Logger.debug("COMM: Received valid request ACK.")

            # Generate shared key
            shared_key = self.comsec_core.generate_shared_key(pkey)
            Logger.debug("COMM: Shared Key: {}".format(b64encode(shared_key)))

            # Add peer
            self.swarm_manager.add_peer(pid, shared_key, src_ip, src_port)

            # Add peer connection
            self._update_peer_connection_status(
                src_ip,
                src_port,
                False,
                None
            )

            # Connect to peer using normal connection this should refresh
            # the connection in db to normal client conn from auth conn
            self.start_connection(pid, src_ip, src_port)
            
            # pack auth content
            content = self._pack_auth_content(self.peerid, request_id)

            # Send disconnect response for AUTH channel
            dcon_rsp = self.stream_manager.pack_stream(
                stream_type=constants.PROTO_DCON_TYPE,
                stream_content=content,
                stream_flag=STREAM_TYPES.UNAUTH,
                stream_host=src_ip
            )

            return dcon_rsp

        return None

    # ------------------------------------------------
    # Client Protocol Method defined here
    # ------------------------------------------------
    def pass_message(self, pid, msg):
        "Pass message to client. Stream Type: BULK"
        
        # Check if peer is valid
        if not self.swarm_manager.is_peer(pid):
            Logger.warn(
                "COMM: Peer {} is not in swarm. Add peer using addpeer cmd.".format(pid))
            self._print(
                "COMM: Peer {} is not in swarm. Add peer using addpeer cmd.".format(pid))
            return False            

        # Check to see peer connection status
        if not self.swarm_manager.get_peer_connection_status(pid):
            Logger.warn("COMM: Peer {} is offline.".format(pid))
            self._print("Peer {} is offline.".format(pid))
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
            self._print("Peer already in swarm.")
            return False

        # Start a connection with peer
        return self.start_authentication(pid, host, port)

    # ------------------------------------------------

    # ------------------------------------------------
    # Server Protocol Method defined here
    # ------------------------------------------------
    def handle_request_stream(self, stream, connection):

        # Get the sender peer's information from connection
        (src_pid, shared_key, src_ip, _
         ) = self._get_source_from_connection(connection)

        # Response (default = None)
        rsp = None

        # Unpack stream
        (header, content, pkey) = self.stream_manager.unpack_stream(
            stream=stream,
            shared_key=shared_key
        )
        
        # Check if stream type is valid
        if not header:
            Logger.error("COMM: Invalid Stream checksum received.")
            return rsp

        # Print test message if test server
        if self.peerid == constants.LOCAL_TEST_PEER_ID and \
           header in (constants.LOCAL_TEST_STREAM_TYPE):
            self._print_test(header, content)

        # ------------------------------------------------------------
        # Check if the request is an AUTH request and
        # handle it accordingly, this requires no stream challenge
        # ------------------------------------------------------------
        if header == constants.PROTO_AUTH_TYPE:
            # Extract peer id
            (pid, request_id) = self._unpack_auth_content(content)

            Logger.debug("COMM: Received auth request from Peer: {}".format(pid))

            # Add check for repeat additions
            if self.swarm_manager.is_peer(pid):
                Logger.debug(
                    "COMM: Received REPEAT auth request from Peer: {}, Ignoring Request.".format(pid))
                # Close twisted connection
                connection.loseConnection()
                return None

            # Add peer
            # Generate shared key
            shared_key = self.comsec_core.generate_shared_key(pkey)
            Logger.debug("COMM: Shared Key: {}".format(b64encode(shared_key)))

            # A GUI hook could be placed here to check for
            # user approval before addition of the peer.
            self.swarm_manager.add_peer(
                pid=pid,
                key=shared_key,
                host=src_ip,
                port=constants.PEER_PORT
            )

            # Add peer connection and change status
            self._update_peer_connection_status(
                peer_ip=src_ip,
                peer_port=constants.PEER_PORT,
                status=True,
                conn=connection
            )
            
            # Get content
            content = self._pack_auth_content(self.peerid, request_id)

            # Send current peer info
            rsp = self.stream_manager.pack_stream(
                stream_type=constants.PROTO_AACK_TYPE,
                stream_content=content,
                stream_flag=STREAM_TYPES.UNAUTH,
                stream_host=src_ip
            )

            Logger.debug(
                "COMM: Auth Response: {} Stream Length: {}".format(b64encode(rsp), len(rsp)))

            # Send Auth response
            return rsp

        # Check if stream type is valid
        if not header:
            Logger.error(
                "COMM: Invalid stream ID received from unpacking stream."
            )
            return rsp

        # Check if connection is recognized
        if not self.swarm_manager.get_peer(src_pid):
            Logger.warn(
                "COMM: Unknown pid @{} attempting contact.".format(src_ip)
            )

        Logger.debug("COMM: Received: {}".format(b64encode(stream)))

        if header == constants.PROTO_DCON_TYPE:
            Logger.debug("COMM: Received Disconnect ACK, AUTH Success!")

            # Extract peer id
            (pid, _) = self._unpack_auth_content(content)

            if self.swarm_manager.is_peer(pid) and \
                self.comsec_core.generate_shared_key(pkey) == \
                    self.swarm_manager.get_peer_key(pid):

                Logger.debug("COMM: Peer {} AUTH Done!".format(pid))
                # Close connection
                connection.loseConnection()

            rsp = None

        elif header == constants.LOCAL_TEST_STREAM_TYPE:
            
            # Message receipt successful
            self._print(content, src_ip)
            
            # Repack stream maintaining the same content
            rsp = self.stream_manager.pack_stream(
                stream_type=header,
                stream_content=content,
                stream_host=src_ip,
                shared_key=shared_key
            )

        elif header == constants.PROTO_BULK_TYPE:
            
            # Message receipt successful
            self._print(content, src_ip)

            # Generate response
            rsp = self.stream_manager.pack_stream(
                stream_type=constants.PROTO_MACK_TYPE,
                stream_content='',
                stream_host=src_ip,
                shared_key=shared_key
            )

        return rsp

    def send_pending_streams(self, peer_id):
        "Send unsent streams."

        # Check stream buffer for pending streams
        streambuffer = self.swarm_manager.get_stream_buffer(peer_id)

        if streambuffer:
            for sid in streambuffer:
                # Get stream
                stream = self.stream_manager.get_stream(sid)
                # Get connection
                connection = self.swarm_manager.get_peer_connection(peer_id)
                # Send stream
                self._write_into_connection(connection, stream)
