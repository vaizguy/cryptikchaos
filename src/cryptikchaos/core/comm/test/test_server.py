'''
Created on Aug 9, 2014

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

from base64 import b64encode
import random
import string
from kivy import Logger
import pythonpath
pythonpath.AddSysPath('../../../../src')

from twisted.trial import unittest
from twisted.test import proto_helpers

from cryptikchaos.core.env.configuration import constants
from cryptikchaos.core.device.service import DeviceService
from cryptikchaos.core.comm.service import CommService
from cryptikchaos.core.comm.commcoreserver import CommCoreServerFactory
from cryptikchaos.core.comm.stream.manager import STREAM_TYPES
from cryptikchaos.libs.utilities import generate_auth_token
from cryptikchaos.libs.utilities import md5hash

def test_logger(msg, peerid=None, intermediate=False, *args):
    start_color = '\033[94m'
    end_color = '\033[0m'
    if peerid:
        Logger.info("TRIAL: {}{} {}{}".format(start_color, peerid, msg, end_color))
    else:
        Logger.info("TRIAL: {}{}{}".format(start_color, msg, end_color))   
    
def log_stream(stype, content, skey, l, sim=None):
    
    if sim:
        logger = "SIM"
    else:
        logger = "EXPECTED"
        
    if not type(skey) == long:
        skey = b64encode(skey)        

    test_logger("""{}_{} Stream breakup,
        TYPE   : {}
        CONTENT: {} 
        KEY    : {}
    """.format(
        logger,
        stype, 
        stype, 
        content, 
        skey
    ))
    
def random_stream(l=constants.STREAM_CONTENT_LEN):
    return ''.join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(
            l
        )
    )
                          
class OuroborosTestCase(unittest.TestCase):
    """
    Cyclical testing with the client talking to server 
    through `proto_helpers.StringTransport`."""
    
    client_peer_id = "V_CLIENT"
    server_peer_id = "V_SERVER"
    peer_ip = "192.168.1.1"
    peer_port = 1597
    
    def setUp(self):
        
        # Start device service
        self.device_service = DeviceService()
        
        # Communications service, contains both client & server
        self.comm_service = CommService(
            peerid=self.server_peer_id,
            host=self.peer_ip,
            port=self.peer_port,
            printer=test_logger
        )
        
        # Register device service
        self.comm_service.register_device_service(self.device_service)
        
        # Start server protocol factory
        self.factory = CommCoreServerFactory(self.comm_service)
        self.proto = self.factory.buildProtocol((self.peer_ip, self.peer_port))
        self.tr = proto_helpers.StringTransport()
        self.proto.makeConnection(self.tr)
        
        # Test streams
        self.auth_stream = None
        self.aack_stream = None
        self.dcon_stream = None
        self.bulk_stream = None
        self.mack_stream = None
        
        # Get auth request ID
        self.request_transaction_id = None
        
    def tearDown(self):
           
        # Stop listener
        self.comm_service._stop_listener() 
        
    def _get_auth_transaction(self):
        
        # Get auth request ID
        self.request_transaction_id = generate_auth_token()
        
        #REQUEST
        # Pack auth content
        auth_content = self.comm_service._pack_auth_content(
                            self.client_peer_id, self.request_transaction_id)

        # Pack authentication data into stream
        auth_stream = self.comm_service.stream_manager.pack_stream(
            stream_type=constants.PROTO_AUTH_TYPE,
            stream_content=auth_content,
            stream_flag=STREAM_TYPES.UNAUTH,
            stream_host=self.peer_ip
        )
        
        #ACKNOWLEDGE
        # Get ack content 
        aack_content = self.comm_service._pack_auth_content(
                          self.server_peer_id, self.request_transaction_id)
        
        # Send current peer info
        aack_stream = self.comm_service.stream_manager.pack_stream(
            stream_type=constants.PROTO_AACK_TYPE,
            stream_content=aack_content,
            stream_flag=STREAM_TYPES.UNAUTH,
            stream_host=self.peer_ip
        )
        
        log_stream(
            constants.PROTO_AACK_TYPE, 
            aack_content, 
            self.comm_service.peerkey,
            len(aack_stream)
        )
        
        #DISCONNECT  
        dcon_content = self.comm_service._pack_auth_content(
                                self.client_peer_id, self.request_transaction_id)
        
        dcon_stream = self.comm_service.stream_manager.pack_stream(
            stream_type=constants.PROTO_DCON_TYPE,
            stream_content=dcon_content,
            stream_flag=STREAM_TYPES.UNAUTH,
            stream_host=self.peer_ip
        )
        
        return (auth_stream, aack_stream, dcon_stream)
        
    def _get_bulk_transaction(self):
        
        ## stream packing for single transaction
        
        #BULK MESSAGE
        shared_key = self.comm_service.comsec_core.generate_shared_key(self.comm_service.peerkey)
        # Pack data into stream
        bulk_stream = self.comm_service.stream_manager.pack_stream(
            stream_type=constants.PROTO_BULK_TYPE,
            stream_content=random_stream(),
            stream_host=self.peer_ip,
            shared_key=shared_key
        )
        
        #BULK MESSAGE ACK
        mack_stream = self.comm_service.stream_manager.pack_stream(
            stream_type=constants.PROTO_MACK_TYPE,
            stream_content='',
            stream_host=self.peer_ip,
            shared_key=shared_key
        )
        
        return (bulk_stream, mack_stream)
    
    def _get_fake_transaction(self):
        
        #INVALID BULK MESSAGE
        shared_key = self.comm_service.comsec_core.generate_shared_key(self.comm_service.peerkey)
        # Pack data into stream
        fake_stream = self.comm_service.stream_manager.pack_stream(
            stream_type=constants.PROTO_BULK_TYPE, 
            stream_content=random_stream(), 
            stream_host=self.peer_ip, 
            shared_key=md5hash("INVALID KEY!!!")
        )
        
        #INVALID MESSAGE ACK
        fmack_stream = self.comm_service.stream_manager.pack_stream(
            stream_type=constants.PROTO_MACK_TYPE,
            stream_content='',
            stream_host=self.peer_ip,
            shared_key=shared_key
        )      
        
        return (fake_stream, fmack_stream)
    
    def unpack_stream(self, stream, shared_key=None):
        
        (header, content, pkey) = self.comm_service.stream_manager.unpack_stream(
           stream=stream, 
           shared_key=shared_key
        )
        
        log_stream(header, content, pkey, len(stream), True)  
        
        return (header, content, pkey)
        
    def _start_transaction(self, transactions=1):
        
        # Get auth transaction
        test_logger("AUTHENTICATION TEST.")
        test_logger("====================")
        (auth_stream, aack_stream, dcon_stream) = self._get_auth_transaction()
        
        test_logger("CLIENT ----[AUTH]----> SERVER")
        # send simulated auth request from virtual client
        self.proto.dataReceived('{}\r\n'.format(auth_stream))
        
        test_logger("CLIENT <----[AACK]---- SERVER")
        # Get auth response from sim
        aack_response = self.tr.value().rstrip('\r\n')
                
        # Check if ack is expected
        test_logger("Match received AACK with expected AACK.")        
        self.assertEqual(len(aack_response), len(aack_stream), "Responses of different length")
        self.assertEqual(aack_response, aack_stream)
        test_logger("RECEIVED AACK == EXPECTED AACK.")        

        # Unpack sim ack from auth req
        test_logger("Extrack SERVER public key from AACK.")        
        (_, _, pkey) = self.unpack_stream(stream=aack_response)
        
        # Get shared key from recieved public key
        test_logger("Generate Shared Secret from SERVER's Public Key.")        
        shared_key = self.comm_service.comsec_core.generate_shared_key(pkey)
        
        # Add the peer in to the swarm
        test_logger("Add SERVER into CLIENT Swarm.")        
        self.comm_service.swarm_manager.add_peer(
            self.server_peer_id, 
            shared_key, 
            self.peer_ip, 
            self.peer_port
        )
        
        # remove connection
        test_logger("Update SERVER connection status.")        
        self.comm_service._update_peer_connection_status(
            self.peer_ip,
            self.peer_port,
            False,
            None
        )
        
        # send sim disconnect
        test_logger("CLIENT ----[DCON]----> SERVER")
        test_logger("For disconnection of AUTH connection.")
        self.proto.dataReceived('{}\r\n'.format(dcon_stream))
                
        # check if request id is still valid
        test_logger("Checking if Request ID for AUTH Transaction is invalidated.")
        self.assertFalse(
            self.request_transaction_id in self.comm_service.valid_auth_req_tokens,
            msg='Transaction ID was not deleted from memory at the server side on DCON.')

        # DCON success, Del transaction id
        test_logger("Reset Client Side Request token.")
        self.request_transaction_id = None
        
        # Reset connection 
        test_logger("Reset connection after AUTH.")
        self.tr.loseConnection()
        self.tr = proto_helpers.StringTransport()
        self.proto.makeConnection(self.tr)
        
        # Run transactions
        for i in range(1, transactions+1):
            
            test_logger("Bulk Message Test Iteration : {}".format(i))
            test_logger("BULK STREAM TEST FOR VALID STREAM.")
            test_logger("==================================")
            (bulk_stream, mack_stream) = self._get_bulk_transaction()

            # send simulated bulk msg from virtual client
            test_logger("CLIENT ----[BULK]----> SERVER")
            self.proto.dataReceived('{}\r\n'.format(bulk_stream))
            
            # Get msg ack response from sim
            test_logger("CLIENT <----[MACK]---- SERVER")
            mack_response = self.tr.value().rstrip('\r\n')
            
            # Unpack sim mack from msg txn
            test_logger("Unpack MACK response from SERVER with shared key.")
            self.unpack_stream(stream=mack_response, shared_key=shared_key)
            
            # Check if mack is expected
            test_logger("Match received MACK with expected MACK.")
            self.assertEqual(len(mack_response), len(mack_stream), "Responses of different length")
            self.assertEqual(mack_response, mack_stream)
            test_logger("RECEIVED MACK == EXPECTED MACK.")        
            
            # Reset connection to clear test transport buffer
            test_logger("Reset connection after BULK.")
            self.tr.loseConnection()
            self.tr = proto_helpers.StringTransport()
            self.proto.makeConnection(self.tr)
            
            #Check for invalid bulk msg stream
            test_logger("BULK STREAM TEST FOR INVALID STREAM.")
            test_logger("====================================")
            (fake_stream, fmack_stream) = self._get_fake_transaction()
            
            # Send fake stream to server
            test_logger("CLIENT ----[INVALID BULK STREAM]----> SERVER")
            self.proto.dataReceived('{}\r\n'.format(fake_stream))
            
            test_logger("CLIENT <----[INVALID MACK RESPONSE]---- SERVER")
            fmack_response = self.tr.value().rstrip('\r\n')

            test_logger("Match received invalid MACK with expected MACK.")
            self.assertNotEqual(fmack_response, fmack_stream, "Fake request got a valid mack.")
            test_logger("RECEIVED MACK != EXPECTED MACK.")        
            test_logger("Invalid BULK Stream was rejected.")
    
    def test_transaction(self):
        
        # Test the auth transaction
        self._start_transaction(1)       
