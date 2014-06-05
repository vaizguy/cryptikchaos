'''
Created on May 31, 2014

@author: vaizguy
'''

from cryptikchaos.libs.crypto.pyDHE import DiffieHellman


class ComSecCore:
    
    def __init__(self):
        
        # Diffie-Hellman core
        self.DHE_core = DiffieHellman()
        
        # Peer Public Key
        self.public_key = self.DHE_core.publicKey
        
    def get_public_key(self):
        
        return self.public_key

    def generate_shared_key(self, received_public_key):
        
        self.DHE_core.genKey(received_public_key)
        
        return self.DHE_core.getKey()
        
        
if __name__ == "__main__":

    csc_1 = CommSecCore()
    csc_2 = CommSecCore()

    csc_1_pkey = csc_1.get_public_key()
    csc_2_pkey = csc_2.get_public_key()
    print "Public key: (1):", csc_1_pkey
    print "Type: ", type(csc_1_pkey)
    print "Length: ", len(str(csc_1_pkey))
    
    csc_1_skey = csc_1.generate_shared_key(csc_2_pkey)
    csc_2_skey = csc_2.generate_shared_key(csc_1_pkey)
    
    import struct
    pstream = struct.pack("!L", csc_1_pkey)
    csc_1_pkey_cpy = struct.unpack("!L", pstream)[0]
    print csc_1_pkey_cpy == csc_1_pkey
    
    if (csc_1_skey == csc_2_skey):
        print "Shared Keys match!"
        print len(csc_1_skey), type(csc_1_skey)
    else:
        print "Shared Keys do not match!"
        print csc_1_skey
        print csc_2_skey

