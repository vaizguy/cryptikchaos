'''
Created on Aug 3, 2013

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.1

import collections

# Taken from
# http://goo.gl/mRJseB
# Jochen Ritzel 's solution.


class TransformedDict(collections.MutableMapping):

    """Represents the Peer attributes"""

    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))  # use the free update to set keys

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


class Peer(TransformedDict):

    "Peer dictionary, holds the peer attributes."

    def __getitem__(self, key):

        if key in ("PEER_ID", "PEER_KEY", "PEER_IP", "PEER_PORT", "PEER_CONN_STATUS"):
            return TransformedDict.__getitem__(self, key)
        else:
            raise Exception("Invalid peer attribute.")


if __name__ == "__main__":

    peer = Peer({
                "PEER_ID": 888,
                "PEER_IP": "127.0.0.1",
                "PEER_PORT": 8888,
                "PEER_CONN_STATUS": False,
                })

    print peer

    import cPickle
    print cPickle.loads(cPickle.dumps(peer)) == peer
