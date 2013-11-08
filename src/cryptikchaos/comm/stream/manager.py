'''
Created on Aug 4, 2013

Handles packing and unpacking of streams to be sent
over the air.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.5

from kivy import Logger

from cryptikchaos.libs.Storage.manager import StoreManager

from cryptikchaos.env.configuration import constants

from cryptikchaos.libs.utilities import ip_to_uint32
from cryptikchaos.libs.utilities import uint32_to_ip
from cryptikchaos.libs.utilities import generate_uuid
from cryptikchaos.libs.utilities import compress
from cryptikchaos.libs.utilities import decompress

from cryptikchaos.libs.obscure import shuffler
from cryptikchaos.libs.obscure import unshuffler

from cryptikchaos.exceptions.streamExceptions import \
    StreamOverflowError
    
import struct
import hmac


class StreamManager(StoreManager):
    "Stream manager class."

    def __init__(self, peerid, peerkey):
        
        # Authorized keys
        self._valid_keys = (
            'STREAM_ID',
            'STREAM_DSTIP',
            'STREAM_SRCIP',
            'STREAM_TYPE' ,
            'STREAM_CONTENT',
            'STREAM_LEN',
            'STREAM_CHKSUM',
            'STREAM_PKEY'
        )
        # Create store
        super(StreamManager, self).__init__("StreamStore", self._valid_keys)
        # Peer public key
        self.peer_key = peerkey

    def __del__(self):
        
        # Clear stored streams
        StoreManager.__del__(self)

        
    def _prepare_stream(self, dest_host, src_host, stype, content):
        "Create new stream store."
        
        # Check length of content.
        if len(content) > constants.STREAM_CONTENT_LEN:
            raise StreamOverflowError(constants.STREAM_CONTENT_LEN)

        # Check length of capsule type.
        if len(stype) > constants.STREAM_TYPE_LEN:
            raise StreamOverflowError(constants.STREAM_TYPE_LEN)
        
        # localhost - 127.0.0.1 mapping.
        if dest_host == "localhost":
            dest_host = constants.LOCAL_TEST_HOST
        if src_host == "localhost":
            src_host = constants.LOCAL_TEST_HOST
        
        # Generate uid
        stream_uid = generate_uuid(dest_host)
        # Calc capsule destination IP integer
        stream_dstip = ip_to_uint32(dest_host)
        # Calc capsule source IP 
        stream_srcip = ip_to_uint32(src_host)
        # Stream type
        stream_type = stype.upper()
        # Generate checksum before shuffle
        stream_hmac = hmac.new(content).hexdigest()
        # Calculate content length
        stream_len = len(content)
        # Stream peer key
        stream_pkey = self.peer_key
        
        # Shuffle content
        if constants.ENABLE_SHUFFLE:
            Logger.info("Scrambling content.")

            stream_content = shuffler(
                string=content,
                iterations=constants.STREAM_CONT_SHUFF_ITER
            )
        else:
            stream_content = content
        
        dictionary = {
            'STREAM_ID'      :stream_uid,
            'STREAM_DSTIP'   :stream_dstip,
            'STREAM_SRCIP'   :stream_srcip,
            'STREAM_TYPE'    :stream_type,
            'STREAM_CONTENT' :stream_content,
            'STREAM_LEN'     :stream_len,
            'STREAM_CHKSUM'  :stream_hmac,
            'STREAM_PKEY'    :stream_pkey           
        }
        
        # Add stream to store
        self.add_store(stream_uid, dictionary)
        
        return stream_uid

    def pack_stream(self, captype="NULL", capcontent='',
            dest_host="127.0.0.1", src_host="127.0.0.1"):
        "Pack data into stream."
                
        # Create new stream
        sid = self._prepare_stream(dest_host, src_host, captype, capcontent)
        
        # Pack store into stream
        stream = struct.pack(
            "!{}sII{}s{}sL{}s{}s".format(
                constants.STREAM_ID_LEN,
                constants.STREAM_TYPE_LEN,
                constants.STREAM_CONTENT_LEN,
                constants.STREAM_CHKSUM_LEN,
                constants.STREAM_PKEY_HASH_LEN
            ),
            self.get_store_item(sid, 'STREAM_ID'     ),
            self.get_store_item(sid, 'STREAM_DSTIP'  ),
            self.get_store_item(sid, 'STREAM_SRCIP'  ),
            self.get_store_item(sid, 'STREAM_TYPE'   ),
            self.get_store_item(sid, 'STREAM_CONTENT'),
            self.get_store_item(sid, 'STREAM_LEN'    ),
            self.get_store_item(sid, 'STREAM_CHKSUM' ),
            self.get_store_item(sid, 'STREAM_PKEY'   )
        )

        # Compress stream
        if constants.ENABLE_COMPRESSION:

            stream = compress(stream)
        
        return stream

    def unpack_stream(self, stream):
        "Unpack serial data into stream."
        
        # Decompress data stream
        if constants.ENABLE_COMPRESSION:
            stream = decompress(stream)
        
        # Check if data is of expected chunk size
        if len(stream) != constants.STREAM_SIZE:
            raise StreamOverflowError()
            
        # Unpack stream to variables
        (
            stream_uid,
            stream_dstip,
            stream_srcip,
            stream_type,
            stream_content,
            stream_len,
            stream_hmac,
            stream_pkey   
        ) = struct.unpack(
                "!{}sII{}s{}sL{}s{}s".format(
                constants.STREAM_ID_LEN,
                constants.STREAM_TYPE_LEN,
                constants.STREAM_CONTENT_LEN,
                constants.STREAM_CHKSUM_LEN,
                constants.STREAM_PKEY_HASH_LEN
            ), stream
        )
        
        dictionary = {
            'STREAM_ID'      :stream_uid,
            'STREAM_DSTIP'   :stream_dstip,
            'STREAM_SRCIP'   :stream_srcip,
            'STREAM_TYPE'    :stream_type,
            'STREAM_CONTENT' :stream_content,
            'STREAM_LEN'     :stream_len,
            'STREAM_CHKSUM'  :stream_hmac,
            'STREAM_PKEY'    :stream_pkey           
        }
        
        # Add stream to store
        self.add_store(stream_uid, dictionary)
        
        return self.get_tuple(stream_uid)
    
    def get_content(self, sid):
        
        # Get content
        content = self.get_store_item(
            sid, 
            "STREAM_CONTENT"
        )[0:self.get_store_item(sid, "STREAM_LEN")]
        
        # Unshuffle content
        if constants.ENABLE_SHUFFLE:
            
            Logger.info("Unscrambling content.")
            
            content = unshuffler(
                shuffled_string=content,
                iterations=constants.STREAM_CONT_SHUFF_ITER
            )
        
        # Returns content only if conent integrity is maintained   
        if (hmac.new(content).hexdigest() == self.get_store_item(sid, "STREAM_CHKSUM")):
            return content
        else:
            Logger.warn("Checksum mismatch.")
            return None
        
    def get_destination_ip(self, sid):
        
        i = self.get_store_item(sid, "STREAM_DSTIP")
        return uint32_to_ip(i)

    def get_source_ip(self, sid):

        i = self.get_store_item(sid, "STREAM_SRCIP")
        return uint32_to_ip(i)
        
    def get_tuple(self, sid):
        "Return stream contents in tuple form."

        return (
            self.get_store_item(sid, "STREAM_ID"),
            self.get_destination_ip(sid),
            self.get_source_ip(sid),
            self.get_store_item(sid, "STREAM_TYPE"),
            self.get_content(sid),
            self.get_store_item(
                sid, 
                "STREAM_CONTENT"
            )[0:self.get_store_item(sid, "STREAM_LEN")],
            self.get_store_item(sid, "STREAM_CHKSUM"),
            self.get_store_item(sid, "STREAM_PKEY").strip('\b')
        )       

    def get_stream(self, cid):
        "Return stream data in form of tuple."

        # Return specified stream data as tuple
        return self.stream_dict[cid].tuple()

if __name__ == "__main__":
    
    sm = StreamManager(123, "PKEYTEST")
    stream = sm.pack_stream(captype="ACKN", capcontent="Hello", dest_host="127.0.0.1", src_host="127.0.0.1")
    print stream
    print sm.unpack_stream(stream)
    
    