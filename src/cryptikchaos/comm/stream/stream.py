'''
Created on Jul 21, 2013

This is the application level packet that is used as a basis for any
communications between server and client and vice-versa.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.5

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

from cryptikchaos.libs.customtypes import TransformedDict

import hashlib 


class Stream(TransformedDict):

    "Communication stream definition."

    def __init__(self, pkey=None, captype="NULL", content='',
                 dest_host="127.0.0.1", src_host="127.0.0.1"):

        # Check length of content.
        if len(content) > constants.STREAM_CONTENT_LEN:
            raise StreamOverflowError(constants.STREAM_CONTENT_LEN)

        # Check length of capsule type.
        if len(captype) > constants.STREAM_TYPE_LEN:
            raise StreamOverflowError(constants.STREAM_TYPE_LEN)

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
        # Stream type
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
            
        self._valid_keys = ['CAP_ID', 'CAP_DSTIP', 'CAP_SRCIP', 'CAP_TYPE', \
            'CAP_CONTENT', 'CAP_LEN', 'CAP_CHKSUM', 'CAP_PKEY']

        ## Populate Stream Dict
        super(Stream, self).__init__(
            **{
            'CAP_ID'     : cap_uid,
            'CAP_DSTIP'  : cap_dstip,
            'CAP_SRCIP'  : cap_srcip,
            'CAP_TYPE'   : cap_type,
            'CAP_CONTENT': content,
            'CAP_LEN'    : cap_len,
            'CAP_CHKSUM' : cap_hmac,
            'CAP_PKEY'   : pkey
            }
        )

    def __getitem__(self, key):
        "Get value from dictionary."

        # Get item
        return TransformedDict.__getitem__(self, key)

    def __setitem__(self, key, value):
        "Set key value-pair in dictionary"
        
        if key in self._valid_keys:
            return TransformedDict.__setitem__(self, key, value)
        else:
            print key, self._valid_keys
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
        "Manilpulate key"
        
        return self._hash_key(key)
    
    def _hash_key(self, key):
        "Return md5 hash of key"
        
        return hashlib.md5(key).hexdigest()
    
    def keys(self):
        
        return self._valid_keys
    
    def iteritems(self):
        
        return [(k, TransformedDict.__getitem__(k)) for k in self._valid_keys]
    
    def values(self):
        
        return [TransformedDict.__getitem__(k) for k in self._valid_keys]
    
    def items(self):
        
        return [(k, v) for (k, v) in self.iteritems()]

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
            TransformedDict.__getitem__(self, 'CAP_ID'     ),
            TransformedDict.__getitem__(self, 'CAP_DSTIP'  ),
            TransformedDict.__getitem__(self, 'CAP_SRCIP'  ),
            TransformedDict.__getitem__(self, 'CAP_TYPE'   ),
            TransformedDict.__getitem__(self, 'CAP_CONTENT'),
            TransformedDict.__getitem__(self, 'CAP_LEN'    ),
            TransformedDict.__getitem__(self, 'CAP_CHKSUM' ),
            TransformedDict.__getitem__(self, 'CAP_PKEY'   )

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
            raise StreamOverflowError()

        (
           CAP_ID,
           CAP_DSTIP,
           CAP_SRCIP,
           CAP_TYPE,
           CAP_CONTENT,
           CAP_LEN,
           CAP_CHKSUM,
           CAP_PKEY
        ) = struct.unpack(
                "!{}sII{}s{}sL{}s{}s".format(
                constants.STREAM_ID_LEN,
                constants.STREAM_TYPE_LEN,
                constants.STREAM_CONTENT_LEN,
                constants.STREAM_CHKSUM_LEN,
                constants.STREAM_PKEY_HASH_LEN
            ), stream
        )

        self.__setitem__('CAP_ID'     , CAP_ID     ),
        self.__setitem__('CAP_DSTIP'  , CAP_DSTIP  ),
        self.__setitem__('CAP_SRCIP'  , CAP_SRCIP  ),
        self.__setitem__('CAP_TYPE'   , CAP_TYPE   ),
        self.__setitem__('CAP_CONTENT', CAP_CONTENT),
        self.__setitem__('CAP_LEN'    , CAP_LEN    ),
        self.__setitem__('CAP_CHKSUM' , CAP_CHKSUM ),
        self.__setitem__('CAP_PKEY'   , CAP_PKEY   )

    def __str__(self):
        "String representation of capsule."

        string = ''

        for v in self.store.values():
            string += str(v) + ':'

        return string.strip(':')

    def getid(self):
        "Return Stream ID."

        return TransformedDict.__getitem__(self, "CAP_ID")

    def getdip(self):
        "Return Destination IP."

        return uint32_to_ip(TransformedDict.__getitem__(self, "CAP_DSTIP"))

    def getsip(self):
        "Return Destination IP."

        return uint32_to_ip(TransformedDict.__getitem__(self, "CAP_SRCIP"))

    def gettype(self):
        "Return Stream protocol type."

        return TransformedDict.__getitem__(self, "CAP_TYPE")

    def getcontent(self):
        "Return capsule content if its integrity is maintained."
        
        # Get content
        content = TransformedDict.__getitem__(
            self, "CAP_CONTENT"
        )[0:TransformedDict.__getitem__(self, "CAP_LEN")]
        
        # Unshuffle content
        if constants.ENABLE_SHUFFLE:
            content = unshuffler(
                shuffled_string=content,
                iterations=constants.STREAM_CONT_SHUFF_ITER
            )
        
        # Returns content only if conent integrity is maintained   
        if (hmac.new(content).hexdigest() == TransformedDict.__getitem__(self, "CAP_CHKSUM")):
            return content
        else:
            return None
        
    def getlen(self):
        "Return the capsule content length"
        
        return TransformedDict.__getitem__(self, "CAP_LEN")
    
    def getchecksum(self):
        "Return capsule checksum"
        
        return TransformedDict.__getitem__(self, "CAP_CHKSUM")
    
    def getpkey(self):
        "Return peer's public key"
        
        return TransformedDict.__getitem__(self, "CAP_PKEY").strip('\b')

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
