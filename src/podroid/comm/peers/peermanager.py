'''
Created on Aug 3, 2013

@author: vaizguy
'''
from podroid.comm.peers.peer import Peer
from podroid.config.configuration import *

from kivy.logger import Logger


class PeerManager:
    
    
    def __init__(self):
               
        self._peer_dict = {}
        
        ## Add test server 
        self._peer_dict[constants.LOCAL_TEST_PEER_ID] = Peer(constants.LOCAL_TEST_PEER_ID, 
                                                             constants.LOCAL_TEST_HOST, 
                                                             constants.LOCAL_TEST_PORT)
    
    
    def add_peer(self, pid, host, port):
        
        Logger.debug( "Adding Peer {} , {}@{}".format(pid, host, port) )
        self._peer_dict[pid] = Peer(pid, host, port)
        
        
    def get_peer(self, pid):
        
        if pid in self._peer_dict.keys():
            return self._peer_dict[pid]
        else:
            return None
        
        
    def add_peer_connection(self, pid, conn):
        
        try:
            self._peer_dict[pid].add_connection(conn)
        except KeyError:
            Logger.error( "Invalid Peer ID." )
            return False
        else:
            return True           

        
    def connect_to_peer(self, pid):
        
        try:
            stat = self.get_peer_connection_status(pid)
        except KeyError:
            Logger.error( "Invalid Peer ID." )
            return None
        else:
            if stat:
                return self.get_peer_connection(pid)
            else:
                return None           
        
        
    def update_peer_connection_status(self, pid, status):

        return self._peer_dict[pid].update_connection_status(status)
    
    
    def peer_list(self):
        
        return [(pid, peer.get_host(), peer.get_port(), peer.is_connected()) for (pid, peer) in self._peer_dict.iteritems()]
    
    
    def peer_host(self, pid):
        
        return self._peer_dict[pid].get_host()
    
    
    def get_peerid_from_ip(self, peer_ip):
        
        for (pid, ip, _, _) in self.peer_list():
            if ip == peer_ip:
                return pid
            
    
    def get_peer_connection_status(self, pid):
        
        return self._peer_dict[pid].is_connected()
    
    
    def get_peer_connection(self, pid):
        
        return self._peer_dict[pid].get_connection()

        
        
if __name__ == '__main__':
    pm = PeerManager()
    pm.add_peer(123, 'localhost', 8000)        
    pm.add_peer(234, 'localhost', 8001)        
    pm.add_peer(345, 'localhost', 8002)        
    pm.add_peer(456, 'localhost', 8003)
    print pm.peer_list()
        
        