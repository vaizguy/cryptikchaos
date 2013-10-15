'''
Created on Aug 4, 2013

Handles packing and unpacking of capsules to be sent
over the air.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.2

from cryptikchaos.comm.capsule.capsule import Capsule


class CapsuleManager:

    "Capsule manager class."

    def __init__(self, peerkey):

        self.capsule_dict = {}
        self.peer_key = peerkey

    def __del__(self):

        del self.capsule_dict

    def pack_capsule(self, captype="NULL", capcontent='',
                     dest_host="127.0.0.1", src_host="127.0.0.1"):
        "Pack data into capsule."

        capsule = Capsule(self.peer_key, captype, capcontent, dest_host, src_host)

        self.capsule_dict[capsule.getid()] = capsule

        return capsule.pack()

    def unpack_capsule(self, serial):
        "Unpack serial data into capsule."

        capsule = Capsule()

        try:
            capsule.unpack(serial)
        except:
            raise
        else:
            self.capsule_dict[capsule.getid()] = capsule
            return capsule.tuple()

    def get_capsule(self, cid):
        "Return capsule data in form of tuple."

        return self.capsule_dict[cid].tuple()
