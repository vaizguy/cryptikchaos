'''
Created on Jul 21, 2013

@author: vaizguy
'''

from podroid.comm.commcoreserver import CommCoreServerFactory
from podroid.comm.commcoreclient import CommCoreClientFactory

from podroid.comm.peers.peermanager import PeerManager

from twisted.internet import reactor

class CommService(PeerManager):
    
    def __init__(self, peerid, host, port):
        
        ## Initialize peer manager
        PeerManager.__init__(self)
                
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
                conn = self.start_connection(h, p)
                self.add_peer_connection(pid, conn)
            else:
                pass
        
    def send_data(self, pid, data_class, data_content):

        conn = self.connect_to_peer(pid)

        if conn:
            conn.transport.write(data_class + ':' + data_content)
        else:
            print 'Connection failed.'
        
        
    def on_client_connection(self, connection): pass
    
    def start_connection(self, host='localhost', port=8001):
        print 'starting conn'
        return reactor.connectTCP(host, port, CommCoreClientFactory(self))
        
    def on_server_connection(self, connection): 
        print 'Server Connection success!'
        return connection
        
        
        
    

    
        