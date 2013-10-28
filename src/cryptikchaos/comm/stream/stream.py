'''
Created on Jul 21, 2013

This is the application level packet that is used as a basis for any
communications between server and client and vice-versa.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.4

import struct
import hmac

from cryptikchaos.config.configuration import constants

from cryptikchaos.exceptions.streamExceptions import \
    StreamOverflowError

from cryptikchaos.libs.utilities import ip_to_uint32
from cryptikchaos.libs.utilities import uint32_to_ip
from cryptikchaos.libs.utilities import generate_uuid
from cryptikchaos.libs.utilities import compress
from cryptikchaos.libs.utilities import decompress

from cryptikchaos.libs.obscure import shuffler
from cryptikchaos.libs.obscure import unshuffler


class Stream(object):

    "Communication stream definition."

    def __init__(self, pkey=None, captype="NULL", content='',
                 dest_host="127.0.0.1", src_host="127.0.0.1"):

        # Check length of content.
        if len(content) > constants.STREAM_CONTENT_LEN:
            raise CapsuleOverflowError(constants.STREAM_CONTENT_LEN)

        # Check length of capsule type.
        if len(captype) > constants.STREAM_TYPE_LEN:
            raise CapsuleOverflowError(constants.STREAM_TYPE_LEN)

        # localhost - 127.0.0.1 mapping.
        if dest_host == "localhost":
            dest_host = constants.LOCAL_TEST_HOST
        if src_host == "localhost":
            src_host = constants.LOCAL_TEST_HOST

        ## Calculate all capsule values here using 
        ## original inputs.
        
        # Generate uid
        cap_uid = generate_uuid(dest_host)
        # Generate checksum before shuffle
        cap_hmac = hmac.new(content).hexdigest()
        # Calc capsule destination IP integer
        cap_dstip = ip_to_uint32(dest_host)
        # Calc capsule source IP 
        cap_srcip = ip_to_uint32(src_host)
        # Capsule type
        cap_type = captype.upper()
        # Calculate content length
        cap_len = len(content)
        
        ## All compression/obfuscation performed now.
        
        # Shuffle content
        if constants.ENABLE_SHUFFLE:
            content = shuffler(
                string=content, 
                iterations=constants.STREAM_CONT_SHUFF_ITER
            )

        ## Populate capsule fields
        self._dictionary = {
            'CAP_ID'     : cap_uid,
            'CAP_DSTIP'  : cap_dstip,
            'CAP_SCRIP'  : cap_srcip,
            'CAP_TYPE'   : cap_type,
            'CAP_CONTENT': content,
            'CAP_LEN'    : cap_len,
            'CAP_CHKSUM' : cap_hmac,
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
                constants.STREAM_ID_LEN,
                constants.STREAM_TYPE_LEN,
                constants.STREAM_CONTENT_LEN,
                constants.STREAM_CHKSUM_LEN,
                constants.STREAM_PKEY_HASH_LEN
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
        if constants.ENABLE_COMPRESSION:
            stream = compress(stream)

        return stream

    def unpack(self, stream):
        "Unpack serial data into capsule."

        # Decompress data stream
        if constants.ENABLE_COMPRESSION:
            stream = decompress(stream)

        # Check if data is of expected chunk size
        if len(stream) != constants.STREAM_SIZE:
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
                constants.STREAM_ID_LEN,
                constants.STREAM_TYPE_LEN,
                constants.STREAM_CONTENT_LEN,
                constants.STREAM_CHKSUM_LEN,
                constants.STREAM_PKEY_HASH_LEN
            ), stream
        )

    def __str__(self):
        "String representation of capsule."

        string = ''

        for v in self._dictionary.values():
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
        
        # Get content
        content = self._dictionary[
            "CAP_CONTENT"
        ][0:self._dictionary["CAP_LEN"]]
        
        # Unshuffle content
        if constants.ENABLE_SHUFFLE:
            content = unshuffler(
                shuffled_string=content,
                iterations=constants.STREAM_CONT_SHUFF_ITER
            )
        
        # Returns content only if conent integrity is maintained   
        if (hmac.new(content).hexdigest() == self._dictionary["CAP_CHKSUM"]):
            return content
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

    Ctx = Stream(pkey="123", captype="TEST", content='Hello',
                 dest_host="127.0.0.1", src_host="127.0.0.1")
    pkd = Ctx.pack()
    print 'Packed data is :', pkd
    Crx = Stream()
    Crx.unpack(pkd)
    print "Unpacked data :", Crx.tuple()
