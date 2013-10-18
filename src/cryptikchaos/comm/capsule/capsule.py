'''
Created on Jul 21, 2013

This is the application level packet that is used as a basis for any
communications between server and client and vice-versa.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.2

import struct
import zlib

from cryptikchaos.config.configuration import *
from cryptikchaos.exceptions.capsuleExceptions import *
from cryptikchaos.libs.utilities import *

class Capsule(object):

    "Capsule definition."

    def __init__(self, pkey=None, captype="NULL", content='',
                 dest_host="127.0.0.1", src_host="127.0.0.1"):

        # Check length of content.
        if len(content) > constants.CAPS_CONTENT_LEN:
            raise Exception(
                'OverflowError: Content exceeded capsule limit of 40'
            )

        # Check length of capsule type.
        if len(captype) > constants.CAPS_TYPE_LEN:
            raise Exception(
                'OverflowError: Type exceeded capsule limit of 4'
            )

        # localhost - 127.0.0.1 mapping.
        if dest_host == "localhost":
            dest_host = constants.LOCAL_TEST_HOST
        if src_host == "localhost":
            src_host = constants.LOCAL_TEST_HOST

        # Generate uid
        uid = generate_uuid(dest_host)

        # Populate capsule fields
        self._dictionary = {
            'CAP_ID'     : uid,
            'CAP_DSTIP'  : ip_to_uint32(dest_host),
            'CAP_SCRIP'  : ip_to_uint32(src_host),
            'CAP_TYPE'   : captype.upper(),
            'CAP_CONTENT': content,
            'CAP_LEN'    : len(content),
            'CAP_CHKSUM' : hmac.new(content).hexdigest(),
            'CAP_PKEY'   : pkey
            }

    def __setitem__(self, key, item):

            if key not in self._dictionary:
                raise KeyError("The key '{}' is not defined.".format(key))

            self._dictionary[key] = item

    def __getitem__(self, key):

        return self._dictionary[key]

    def pack(self):
        "Pack data into capsule. (i.e struct packing)"

        # Pack the data into capsule
        stream = struct.pack(
            "!{}sII{}s{}sL{}s{}s".format(
                constants.CAPS_ID_LEN,
                constants.CAPS_TYPE_LEN,
                constants.CAPS_CONTENT_LEN,
                constants.CAPS_CHKSUM_LEN,
                constants.CAPS_PKEY_HASH_LEN
            ),
            self._dictionary['CAP_ID'],
            self._dictionary['CAP_DSTIP'],
            self._dictionary['CAP_SCRIP'],
            self._dictionary['CAP_TYPE'],
            self._dictionary['CAP_CONTENT'],
            self._dictionary['CAP_LEN'],
            self._dictionary['CAP_CHKSUM'],
            self._dictionary['CAP_PKEY']
        )

        # Compress stream
        stream_zip = zlib.compress(stream)

        return stream_zip

    def unpack(self, stream):
        "Unpack serial data into capsule."

        # Decompress data stream
        stream_unzip = zlib.decompress(stream)

        # Check if data is of expected chunk size
        if len(stream_unzip) != constants.CAPSULE_SIZE:
            raise CapsuleOverflowError()

        (
            self._dictionary['CAP_ID'],
            self._dictionary['CAP_DSTIP'],
            self._dictionary['CAP_SRCIP'],
            self._dictionary['CAP_TYPE'],
            self._dictionary['CAP_CONTENT'],
            self._dictionary['CAP_LEN'],
            self._dictionary['CAP_CHKSUM'],
            self._dictionary['CAP_PKEY']
        ) = struct.unpack(
                "!{}sII{}s{}sL{}s{}s".format(
                constants.CAPS_ID_LEN,
                constants.CAPS_TYPE_LEN,
                constants.CAPS_CONTENT_LEN,
                constants.CAPS_CHKSUM_LEN,
                constants.CAPS_PKEY_HASH_LEN
            ), stream_unzip
        )

    def __str__(self):
        "String representation of capsule."

        string = ''

        for (k, v) in self._dictionary.iteritems():
            string += str(v) + ':'

        return string.strip(':')

    def getid(self):
        "Return Capsule ID."

        return self._dictionary["CAP_ID"]

    def getdip(self):
        "Return Destination IP."

        return uint32_to_ip(self._dictionary["CAP_DSTIP"])

    def getsip(self):
        "Return Destination IP."

        return uint32_to_ip(self._dictionary["CAP_SRCIP"])

    def gettype(self):
        "Return Capsule protocol type."

        return self._dictionary["CAP_TYPE"]

    def getcontent(self):
        "Return capsule content if its integrity is maintained."
        if (hmac.new(self._dictionary["CAP_CONTENT"]).hexdigest()
                == self._dictionary["CAP_CHKSUM"]):
            return self._dictionary[
                "CAP_CONTENT"
            ][0:self._dictionary["CAP_LEN"]]
        else:
            return None
        
    def getlen(self):
        "Return the capsule content length"
        
        return self._dictionary["CAP_LEN"]
    
    def getchecksum(self):
        "Return capsule checksum"
        
        return self._dictionary["CAP_CHKSUM"]
    
    def getpkey(self):
        "Return peer's public key"
        
        return self._dictionary["CAP_PKEY"].strip('\b')

    def tuple(self):
        "Return capsule in tuple form."

        return (
            self.getid(),
            self.getdip(),
            self.getsip(),
            self.gettype(),
            self.getcontent(),
            self.getlen(),
            self.getchecksum(),
            self.getpkey()
        )


if __name__ == '__main__':

    Ctx = Capsule('TEST', 'This is a capsule test.')
    pkd = Ctx.pack()
    print 'Packed data is :', pkd
    Crx = Capsule()
    Crx.unpack(pkd)
    print "Unpacked data :", Crx.tuple()
