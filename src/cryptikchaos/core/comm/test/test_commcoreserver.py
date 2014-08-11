'''
Created on Aug 9, 2014

@author: vaizguy
'''

import pythonpath
pythonpath.AddSysPath('../../../../src')

from cryptikchaos.core.env.configuration import constants
from cryptikchaos.core.comm.commcoreserver import CommCoreServerFactory
from cryptikchaos.core.comm.service import CommService
from cryptikchaos.core.comm.stream.manager import STREAM_TYPES
from cryptikchaos.libs.utilities import generate_auth_token

from twisted.trial import unittest
from twisted.test import proto_helpers

  
def print_message(msg, peerid="", intermediate=False, *args):

    print "[TRIAL             ] {}: {}\n".format(peerid, msg)
    
def log_stream(stype, content, skey):

    print_message('EXPECTED_{} Stream breakup,\nCONTENT: {} \nKEY: {}'.format(
        stype, 
        content, 
        skey
    ))
                          
        
class AuthenticateTestCase(unittest.TestCase):
    
    client_peer_id = "V_CLIENT"
    server_peer_id = "V_SERVER"
    peer_ip = constants.PEER_HOST
    
    def setUp(self):
        
        self.comm_service = CommService(
            peerid=self.server_peer_id,
            host=self.peer_ip,
            port=constants.PEER_PORT,
            printer=print_message
        )
        
        factory = CommCoreServerFactory(self.comm_service)
        self.proto = factory.buildProtocol(('127.0.0.1', 0))
        self.tr = proto_helpers.StringTransport()
        self.proto.makeConnection(self.tr)
        
        # Test streams
        self.auth_stream = None
        self.aack_stream = None
        self.dcon_stream = None
        
    def tearDown(self):
           
        # Stop listener
        self.comm_service._stop_listener()        
        
    def _prepare_auth_transaction(self):
        
        ## AUTH Request
        # Get auth request ID
        request_transaction_id = generate_auth_token()
        
        #REQUEST
        # Pack auth content
        auth_content = self.comm_service._pack_auth_content(
                            self.client_peer_id, request_transaction_id)

        # Pack authentication data into stream
        self.auth_stream = self.comm_service.stream_manager.pack_stream(
            stream_type=constants.PROTO_AUTH_TYPE,
            stream_content=auth_content,
            stream_flag=STREAM_TYPES.UNAUTH,
            stream_host=self.peer_ip
        )
        
        #ACKNOWLEDGE
        # Get ack content 
        ack_content = self.comm_service._pack_auth_content(
                          self.server_peer_id, request_transaction_id)
        
        # Send current peer info
        self.aack_stream = self.comm_service.stream_manager.pack_stream(
            stream_type=constants.PROTO_AACK_TYPE,
            stream_content=ack_content,
            stream_flag=STREAM_TYPES.UNAUTH,
            stream_host=self.peer_ip
        )
        
        log_stream(
            constants.PROTO_AACK_TYPE, 
            ack_content, 
            self.comm_service.peerkey
        )
        
        #DISCONNECT  
        dcon_content = self.comm_service._pack_auth_content(
                                self.client_peer_id, request_transaction_id)
        
        self.dcon_stream = self.comm_service.stream_manager.pack_stream(
            stream_type=constants.PROTO_DCON_TYPE,
            stream_content=dcon_content,
            stream_flag=STREAM_TYPES.UNAUTH,
            stream_host=self.peer_ip
        )

    def _start_auth_transaction(self):
        
        # send simulated auth request from virtual client
        self.proto.dataReceived('{}\r\n'.format(self.auth_stream))
        
        # Get auth response from sim
        ack_response = self.tr.value().rstrip('\r\n')
        
        # Unpack sim ack from auth req
        (header, content, pkey) = self.comm_service.stream_manager.unpack_stream(
            stream=ack_response)
        
        log_stream(header, content, pkey)
        
        # Check if ack is expected
        self.assertEqual(ack_response, self.aack_stream)
        
        # send sim disconnect
        self.proto.dataReceived('{}\r\n'.format(self.dcon_stream))
    
    def test_handle_auth_request_stream(self):
        
        # Prepare stream
        self._prepare_auth_transaction()
                
        # Test the auth transaction
        self._start_auth_transaction()
        