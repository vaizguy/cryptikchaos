'''
Created on Jul 21, 2013

@author: vaizguy
'''

from podroid.comm.commcoreserver import CommCoreServerFactory
from podroid.comm.commcoreclient import CommCoreClientFactory

from podroid.comm.peers.peermanager import PeerManager
from podroid.comm.capsule.capsulemanager import CapsuleManager

from podroid.config.configuration import *

from twisted.internet import reactor

from kivy.logger import Logger

class CommService(PeerManager, CapsuleManager):
    
    def __init__(self, peerid, host, port):
               
        ## Initialize peer manager
        PeerManager.__init__(self)
        ## Initialize capsule manager
        CapsuleManager.__init__(self)
                
        self.peerid = peerid
        self.host   = host
        self.port   = port
                 
        ## Start the listener
        self._start_server()
        
        ## Start peer connections
        self._start_peer_connectors()
               
    def _start_server(self):
        
        reactor.listenTCP(self.port, CommCoreServerFactory(self))
        
    def _start_peer_connectors(self):
        
        ## Connect to all peers
        for (pid, h, p, cs) in self.peer_list():
            
            ## Check conn status
            if not cs:
                conn = self.start_connection(pid, h, p)
                self.add_peer_connection(pid, conn)
            else:
                pass
        
    def send_data(self, pid, data_class, data_content):

        conn = self.connect_to_peer(pid)
        
        capsule = self.pack_capsule(data_class, data_content, self.peer_host(pid))
        
        try:
            conn.transport.write(capsule)
        except:
            Logger.error( "Connection to peer failed. Please try later." )
            return False
        else:
            return True
        
        
    def on_client_connection(self, connection): pass
    
    def start_connection(self, pid, host='localhost', port=8000):
        
        Logger.debug( "Connecting to pid: {}".format(pid) )
        return reactor.connectTCP(host, port, CommCoreClientFactory(self))
        
    def on_server_connection(self, connection): 
        
        Logger.debug( "Server Connection success! Connection: {}".format(connection) )
        return connection
        
    def handle_response(self, response):
        
        if len(response) != constants.CAPSULE_SIZE:
            raise Exception('Capsule chunk should be equal to '+str(constants.CAPSULE_SIZE)+'B')
        
        ## Repsonse handling architecture should be placed here.
        (cid, dest_ip, captype, content, _, chksum) = self.unpack_capsule(response)

        ## Currently the test case is inbuilt into the pod. --## TEST BEGIN ##       
        if captype == constants.LOCAL_TEST_CAPS_TYPE and \
            cid == constants.LOCAL_TEST_CAPS_ID and \
         chksum == constants.LOCAL_TEST_CAPS_CHKSUM and \
        content == constants.LOCAL_TEST_STR and \
        dest_ip == constants.LOCAL_TEST_HOST:
            Logger.debug( 'Sending Message Test Pass.' )
        else:
            Logger.debug( """
                Sending Message Test Fail.
                For test to pass, 
                1. Test server must be running.
                2. Command is 'send 888 Hello World!'
            """ )
        ## ----------------------------------------------------## TEST END ##