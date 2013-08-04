'''
Created on Jul 21, 2013

@author: vaizguy
'''

from podroid.comm.commcoreserver import CommCoreServerFactory
from podroid.comm.commcoreclient import CommCoreClientFactory

from podroid.comm.peers.peermanager import PeerManager
from podroid.comm.capsule.capsulemanager import CapsuleManager

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

        if conn:
            conn.transport.write(capsule)
            return True
        else:
            return False
            Logger.error( "Connection to peer failed. Please try later." )
        
        
    def on_client_connection(self, connection): pass
    
    def start_connection(self, pid, host='localhost', port=8000):
        
        Logger.debug( "Connecting to pid: {}".format(pid) )
        return reactor.connectTCP(host, port, CommCoreClientFactory(self))
        
    def on_server_connection(self, connection): 
        
        Logger.debug( "Server Connection success! Connection: {}".format(connection) )
        return connection
        
