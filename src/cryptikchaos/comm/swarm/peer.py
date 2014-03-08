'''
Created on Dec 8, 2013

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"


class Peer:
    
    def __init__(self, pid, key, host, port):
        
        self._pid = pid
        self._key = key
        self._host = host
        self._port = port
        self.dict = {
            "PEER_ID"    : self._pid,
            "PEER_KEY"   : self._key,
            "PEER_IP"    : self._host,
            "PEER_PORT"  : self._port,
            "PEER_STATUS": False,
            "PEER_COLOR" : self._pid
        }

        
        
        
    
    