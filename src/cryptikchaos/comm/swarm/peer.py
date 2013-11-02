'''
Created on Aug 3, 2013

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.5

from cryptikchaos.libs.customtypes import TransformedDict

import hashlib

class Peer(TransformedDict):
    "Peer dictionary, holds the peer attributes."
        
    # authorized keys
    _valid_keys = (
        "PEER_ID", "PEER_KEY", "PEER_IP", "PEER_PORT", \
        "PEER_CONN_STATUS", "PEER_ID_COLOR"
    )
        
    def __init__(self, *args, **kwargs):
        "Initialize dictionary."
        
        # Init parent
        super(Peer, self).__init__(*args, **kwargs)
                
    def __getitem__(self, key):
        "Get value from dictionary."

        # Get item
        return TransformedDict.__getitem__(self, key)

        
    def __setitem__(self, key, value):
        "Set key value-pair in dictionary"
        
        if key in self._valid_keys:
            return TransformedDict.__setitem__(self, key, value)
        else:
            raise Exception("Error: Invalid peer attribute.")   
        
    def __delitem__(self, key):
        "Reset key's value."
        
        if key in self._valid_keys:
            # Delete the item
            TransformedDict.__delitem__(self, key)
            # Re-create key with no value
            return TransformedDict.__setitem__(self, key, None)
        else:
            # Delete unauth key
            return TransformedDict.__delitem__(self, key)
        
    def __keytransform__(self, key):
        "Manipulate key"
        
        return self._hash_key(key)
            
    def _hash_key(self, key):
        "Return md5 hash of key"
        
        return hashlib.md5(key).hexdigest()
    
    def keys(self):
        
        return self._valid_keys
    
    def iteritems(self):
        
        return [(k, self.__getitem__(k)) for k in self._valid_keys]
    
    def values(self):
        
        return [self.__getitem__(k) for k in self._valid_keys]
    
    def items(self):
        
        return [(k, v) for (k, v) in self.iteritems()]
    

if __name__ == "__main__":

    peer = Peer({
                "PEER_ID": 888,
                "PEER_KEY": "KEY!",
                "PEER_IP": "127.0.0.1",
                "PEER_PORT": 8888,
                "PEER_CONN_STATUS": False,
                "PEER_ID_COLOR": "#000000"
                })
    
    print peer.store
    
    # Try invalid load
    try:
        peer["PEER_ATTR"] = None
    except:
        print "Invalid __setitem__ caught."

    print peer

    import cPickle
    print cPickle.loads(cPickle.dumps(peer)) == peer
