'''
Created on Aug 3, 2013

@author: vaizguy
'''
from podroid.comm.peers.peer import Peer
from podroid.config.configuration import *

from kivy.logger import Logger

import shelve
        

class PeerManager:
    
    
    def __init__(self, peerfile=constants.PROJECT_PATH + "/db/peers_db"):
        
        self._peer_dict =  shelve.open(peerfile, flag='c', protocol=None, writeback=True)
        
        ## Add test server 
        self._peer_dict[str(constants.LOCAL_TEST_PEER_ID)] = Peer({
                                                             "PEER_ID"          : constants.LOCAL_TEST_PEER_ID, 
                                                             "PEER_IP"          : constants.LOCAL_TEST_HOST, 
                                                             "PEER_PORT"        : constants.LOCAL_TEST_PORT,
                                                             "PEER_CONN_STATUS" : False,
                                                             })
        
        self.peer_connections = {}
    
    def __del__(self):
        
        
        self._peer_dict.close()
        
        
    def add_peer(self, pid, host, port):
        
        Logger.debug( "Adding Peer {} , {}@{}".format(pid, host, port) )
        
        ## Peer dictionary structure defined here
        self._peer_dict[str(pid)] = Peer({
                                    "PEER_ID"         : pid, 
                                    "PEER_IP"         : host,
                                    "PEER_PORT"       : port,
                                    "PEER_CONN_STATUS": False,
                                    })
        
        ## Sync DB
        self._peer_dict.sync()

        
    def get_peer(self, pid):
        
        if str(pid) in self._peer_dict.keys():
            return self._peer_dict[str(pid)]
        else:
            return None
        
        
    def add_peer_connection(self, pid, conn):
        
        try:
            self.peer_connections[pid] = conn
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

        if status in (True, False):
            ## Set new connection status
            self._peer_dict[str(pid)]["PEER_CONN_STATUS"] = status
            ## Sync DB
            self._peer_dict.sync()
        else:
            raise Exception("Invalid Peer Connection Status, must be True or False.")
        
    
    
    def list_peers(self):
        
        peerlist = []
        
        for k in self._peer_dict.keys():
            ## Get peer attributes/
            p_info = self._peer_dict[k]
            ## Append as tuples (peer id, peer host, peer port, peer status)
            peerlist.append((p_info["PEER_ID"], p_info["PEER_IP"], p_info["PEER_PORT"], p_info["PEER_CONN_STATUS"]))
            
        return peerlist
               
    
    def peer_host(self, pid):
        
        return self._peer_dict[str(pid)]["PEER_IP"]
    
    
    def get_peerid_from_ip(self, peer_ip):

        for (pid, ip, _, _) in self.list_peers():
            if ip == peer_ip:
                return int(pid)
            
        return None ## Add relevent catch
            
    
    def get_peer_connection_status(self, pid):
        
        return self._peer_dict[str(pid)]["PEER_CONN_STATUS"]
    
    
    def get_peer_connection(self, pid):
        
        return self.peer_connections[pid]

        
        
if __name__ == '__main__':
    pm = PeerManager(constants.PROJECT_PATH + "/db/test_peerlist_db")
    pm.add_peer(123, 'localhost', 8000)        
    pm.add_peer(234, 'localhost', 8001)        
    pm.add_peer(345, 'localhost', 8002)        
    pm.add_peer(456, 'localhost', 8003)
    print pm.list_peers()
        
        