'''
Created on Aug 9, 2014

@author: vaizguy
'''

from base64 import b64encode
import random
import string
import pythonpath
pythonpath.AddSysPath('../../../../src')

from twisted.trial import unittest
from twisted.test import proto_helpers

from cryptikchaos.core.env.configuration import constants
from cryptikchaos.core.comm.commcoreserver import CommCoreServerFactory
from cryptikchaos.core.comm.service import CommService
from cryptikchaos.core.comm.stream.manager import STREAM_TYPES
from cryptikchaos.libs.utilities import generate_auth_token
from cryptikchaos.libs.utilities import md5hash

def print_message(msg, peerid="[TESTPRINT]", intermediate=False, *args):

    print "[TRIAL             ] {} {}\n".format(peerid, msg)
    
def log_stream(stype, content, skey, l, sim=None):
    
    if sim:
        logger = "SIM"
    else:
        logger = "EXPECTED"
        
    if not type(skey) == long:
        skey = b64encode(skey)        

    print_message("""{}_{} Stream breakup,
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
              
        # Communications service, contains both client & server
        self.comm_service = CommService(
            peerid=self.server_peer_id,
            host=self.peer_ip,
            port=self.peer_port,
            printer=print_message
        )
        
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
        
        ## In order of stream packing for single transaction
        
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
        
        #BULK MESSAGE
        shared_key = self.comm_service.comsec_core.generate_shared_key(self.comm_service.peerkey)
        # Pack data into stream
        fake_stream = self.comm_service.stream_manager.pack_stream(
            stream_type=constants.PROTO_BULK_TYPE, 
            stream_content=random_stream(), 
            stream_host=self.peer_ip, 
            shared_key=md5hash(shared_key)
        )
        
        #BULK MESSAGE ACK
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
        (auth_stream, aack_stream, dcon_stream) = self._get_auth_transaction()
        
        # send simulated auth request from virtual client
        self.proto.dataReceived('{}\r\n'.format(auth_stream))
        
        # Get auth response from sim
        aack_response = self.tr.value().rstrip('\r\n')
                
        # Check if ack is expected
        self.assertEqual(len(aack_response), len(aack_stream), "Responses of different length")
        self.assertEqual(aack_response, aack_stream)
        
        # Unpack sim ack from auth req
        (_, _, pkey) = self.unpack_stream(stream=aack_response)
        
        # Get shared key from recieved key
        shared_key = self.comm_service.comsec_core.generate_shared_key(pkey)
        
        # Add the peer in to the swarm
        self.comm_service.swarm_manager.add_peer(
            self.server_peer_id, 
            shared_key, 
            self.peer_ip, 
            self.peer_port
        )
        
        # remove connection
        self.comm_service._update_peer_connection_status(
            self.peer_ip,
            self.peer_port,
            False,
            None
        )
        
        # send sim disconnect
        self.proto.dataReceived('{}\r\n'.format(dcon_stream))
                
        # check if request id is still valid
        self.assertFalse(
            self.request_transaction_id in self.comm_service.valid_auth_req_tokens,
            msg='Transaction ID was not deleted from memory at the server side on DCON.')

        # DCON success, Del transaction id
        self.request_transaction_id = None
        
        # Run transactions
        for i in range(1, transactions+1):
            
            print_message("Bulk Message Test Iteration : {}".format(i))
            
            (bulk_stream, mack_stream) = self._get_bulk_transaction()
                   
            # Reset connection 
            self.tr.loseConnection()
            self.tr = proto_helpers.StringTransport()
            self.proto.makeConnection(self.tr)
    
            # send simulated bulk msg from virtual client
            self.proto.dataReceived('{}\r\n'.format(bulk_stream))
            
            # Get msg ack response from sim
            mack_response = self.tr.value().rstrip('\r\n')
            
            # Unpack sim mack from msg txn
            self.unpack_stream(stream=mack_response, shared_key=shared_key)
            
            # Check if mack is expected
            self.assertEqual(len(mack_response), len(mack_stream), "Responses of different length")
            self.assertEqual(mack_response, mack_stream)
            
            # Reset connection to clear test transport buffer
            self.tr.loseConnection()
            self.tr = proto_helpers.StringTransport()
            self.proto.makeConnection(self.tr)
            
            #Check for invalid bulk msg stream
            (fake_stream, fmack_stream) = self._get_fake_transaction()
            
            self.proto.dataReceived('{}\r\n'.format(fake_stream))
            fmack_response = self.tr.value().rstrip('\r\n')
            fmack_response = self.tr.value().rstrip('\r\n')

            self.assertNotEqual(fmack_response, fmack_stream, "Fake request got a valid mack.")
    
    def test_transaction(self):
        
        # Test the auth transaction
        self._start_transaction(1)       
