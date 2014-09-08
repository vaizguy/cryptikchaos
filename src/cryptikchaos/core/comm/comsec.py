'''
Created on May 31, 2014

This file is part of CryptikChaos.

CryptikChaos is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CryptikChaos is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CryptikChaos. If not, see <http://www.gnu.org/licenses/>.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6.1"

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

    csc_1 = ComSecCore()
    csc_2 = ComSecCore()

    csc_1_pkey = csc_1.get_public_key()
    csc_2_pkey = csc_2.get_public_key()
    print "Public key: (1):", csc_1_pkey
    print "Type: ", type(csc_1_pkey)
    print "Length: ", len(str(csc_1_pkey))

    csc_1_skey = csc_1.generate_shared_key(csc_2_pkey)
    csc_2_skey = csc_2.generate_shared_key(csc_1_pkey)

    if (csc_1_skey == csc_2_skey):
        print "Shared Keys match!"
        print len(csc_1_skey), type(csc_1_skey)
    else:
        print "Shared Keys do not match!"
        print csc_1_skey
        print csc_2_skey
