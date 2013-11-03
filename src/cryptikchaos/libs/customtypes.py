'''
Created on Nov 2, 2013

@author: Jochen Ritzel
'''
import collections

# Taken from http://goo.gl/mRJseB
# Jochen Ritzel 's solution for custom dictionary.


class TransformedDict(collections.MutableMapping):
    """Represents the Peer attributes"""

    def __init__(self, *args, **kwargs):
        
        self.store = dict()
        self.update(dict(*args, **kwargs))  # use the free update to set keys
        
    def __str__(self):
        
        return self.store.__str__()
    
    def __repr__(self):
        
        return self.store.__repr__()

    def __getitem__(self, key):
        
        return self.store[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        
        self.store[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        
        del self.store[self.__keytransform__(key)]

    def __iter__(self):
        
        return iter(self.store)

    def __len__(self):
        
        return len(self.store)

    def __keytransform__(self, key):
        
        return key
