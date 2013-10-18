'''
Created on Aug 4, 2013

Handles packing and unpacking of capsules to be sent
over the air.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.3

from cryptikchaos.comm.capsule.capsule import Capsule


class CapsuleManager:

    "Capsule manager class."

    def __init__(self, peerkey):

        # Dictionary of all packed/unpacked capsules
        self.capsule_dict = {}
        # Peer public key
        self.peer_key = peerkey

    def __del__(self):

        # Clear stored capsules
        del self.capsule_dict

    def pack_capsule(self, captype="NULL", capcontent='',
                     dest_host="127.0.0.1", src_host="127.0.0.1"):
        "Pack data into capsule."

        # Create and populate capsule with specified data
        capsule = Capsule(self.peer_key, captype, capcontent, dest_host, src_host)

        # Store capsule
        self.capsule_dict[capsule.getid()] = capsule

        # Return capsule as packed struct
        return capsule.pack()

    def unpack_capsule(self, serial):
        "Unpack serial data into capsule."

        # Create empty capsule
        capsule = Capsule()

        try:
            # Unpack into capsule
            capsule.unpack(serial)
        except:
            raise
        else:
            # Store unpacked capsule
            self.capsule_dict[capsule.getid()] = capsule
            # Return unpacked data as tuple
            return capsule.tuple()

    def get_capsule(self, cid):
        "Return capsule data in form of tuple."

        # Return specified capsule data as tuple
        return self.capsule_dict[cid].tuple()
