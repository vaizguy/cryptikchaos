'''
Created on Aug 4, 2013

Handles packing and unpacking of streams to be sent
over the air.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.5

from kivy import Logger

from cryptikchaos.env.configuration import constants

from cryptikchaos.libs.Storage.manager import StoreManager

from cryptikchaos.libs.utilities import ip_to_uint32
from cryptikchaos.libs.utilities import uint32_to_ip
from cryptikchaos.libs.utilities import generate_uuid
from cryptikchaos.libs.utilities import generate_token
from cryptikchaos.libs.utilities import compress
from cryptikchaos.libs.utilities import decompress
from cryptikchaos.libs.utilities import enum

from cryptikchaos.libs.obscure import shuffler
from cryptikchaos.libs.obscure import unshuffler

from cryptikchaos.exceptions.streamExceptions import \
    StreamOverflowError
    
import struct
import hmac

STREAM_TYPES = enum(UNAUTH=0, AUTH=1)

class StreamManager(StoreManager):
    "Stream manager class."

    def __init__(self, peerid, peerkey, peerhost):
        
        # Authorized keys
        self._valid_keys = (
            'STREAM_FLAG',
            'STREAM_DSTIP',
            'STREAM_SRCIP',
            'STREAM_TYPE' ,
            'STREAM_CONTENT',
            'STREAM_CHKSUM',
            'STREAM_PKEY'
        )
        
        # Create store
        super(StreamManager, self).__init__("StreamStore", self._valid_keys)
        # Peer public key
        self.peer_key = peerkey
        # Peer host
        self.peer_host = peerhost

    def __del__(self):
        
        # Clear stored streams
        StoreManager.__del__(self)

        
    def _prepare_stream(self, dest_host, src_host, stype, content,
        flag, peer_key):
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
        # Stream peer key
        stream_key = None
        # Stream flag
        stream_flag = flag
        
        # Check stream signing mode
        if stream_flag == STREAM_TYPES.UNAUTH:
            # Stream key is peer key
            stream_key = self.peer_key
            
        elif stream_flag == STREAM_TYPES.AUTH:
            # Generate token at source side
            stream_key = generate_token(
                stream_uid,
                self.peer_key,
                peer_key
            )
                              
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
            'STREAM_FLAG'    :stream_flag,
            'STREAM_DSTIP'   :stream_dstip,
            'STREAM_SRCIP'   :stream_srcip,
            'STREAM_TYPE'    :stream_type,
            'STREAM_CONTENT' :stream_content,
            'STREAM_CHKSUM'  :stream_hmac,
            'STREAM_PKEY'    :stream_key
        }
                
        # Add stream to store
        self.add_store(stream_uid, dictionary)
        
        return stream_uid

    def pack_stream(self, stype, content, dest_host, src_host, 
            flag=STREAM_TYPES.AUTH, peer_key=None):
        "Pack data into stream."
                
        # Create new stream
        sid = self._prepare_stream(
            dest_host=dest_host, 
            src_host=src_host, 
            stype=stype, 
            content=content, 
            flag=flag, 
            peer_key=peer_key
        )

        # Pack store into stream
        stream = struct.pack(
            "!III{}s{}s{}s{}s".format(
                constants.STREAM_TYPE_LEN,
                constants.STREAM_CONTENT_LEN,
                constants.STREAM_CHKSUM_LEN,
                constants.STREAM_PKEY_HASH_LEN
            ),
            self.get_store_item(sid, 'STREAM_FLAG'     ),
            self.get_store_item(sid, 'STREAM_DSTIP'  ),
            self.get_store_item(sid, 'STREAM_SRCIP'  ),
            self.get_store_item(sid, 'STREAM_TYPE'   ),
            self.get_store_item(sid, 'STREAM_CONTENT'),
            self.get_store_item(sid, 'STREAM_CHKSUM' ),
            self.get_store_item(sid, 'STREAM_PKEY'   )
        )

        # Compress stream
        if constants.ENABLE_COMPRESSION:

            stream = compress(stream)
        
        return stream

    def unpack_stream(self, stream, peer_key=None):
        "Unpack serial data into stream."
        
        # Decompress data stream
        if constants.ENABLE_COMPRESSION:
            stream = decompress(stream)
        
        # Check if data is of expected chunk size
        if len(stream) != constants.STREAM_SIZE:
            raise StreamOverflowError()
            
        # Unpack stream to variables
        (
            stream_flag,
            stream_dstip,
            stream_srcip,
            stream_type,
            stream_content,
            stream_hmac,
            stream_key   
        ) = struct.unpack(
                "!III{}s{}s{}s{}s".format(
                constants.STREAM_TYPE_LEN,
                constants.STREAM_CONTENT_LEN,
                constants.STREAM_CHKSUM_LEN,
                constants.STREAM_PKEY_HASH_LEN
            ), stream
        )
        
        # Remove all null characters if present in content
        stream_content = stream_content.rstrip('\0')

        # Get  uid
        stream_uid = generate_uuid(self.peer_host)
        
        # Check stream signing mode
        if stream_flag == STREAM_TYPES.UNAUTH:
            # Stream key is peer key
            pass
            
        elif stream_flag == STREAM_TYPES.AUTH:    
            # Generate token at destination side
            stream_challenge_key = generate_token(
                stream_uid,
                peer_key,
                self.peer_key
            )
                                      
            # Perform key challenge
            if stream_challenge_key != stream_key:
                Logger.error("Token challenge Fail")
                return [None]*8
            else:
                Logger.info("Token challenge Pass")
        
        dictionary = {
            'STREAM_FLAG'    :stream_flag,
            'STREAM_DSTIP'   :stream_dstip,
            'STREAM_SRCIP'   :stream_srcip,
            'STREAM_TYPE'    :stream_type,
            'STREAM_CONTENT' :stream_content,
            'STREAM_CHKSUM'  :stream_hmac,
            'STREAM_PKEY'    :stream_key           
        }
                        
        # Add stream to store
        self.add_store(stream_uid, dictionary)
        
        return self._get_tuple(stream_uid)
    
    def _get_content(self, sid):
        
        # Get content
        content = self.get_store_item(
            sid, 
            "STREAM_CONTENT"
        )
        
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
            Logger.warn("Stream content checksum mismatch.")
            return None
        
    def _get_destination_ip(self, sid):
        
        i = self.get_store_item(sid, "STREAM_DSTIP")
        return uint32_to_ip(i)

    def _get_source_ip(self, sid):

        i = self.get_store_item(sid, "STREAM_SRCIP")
        return uint32_to_ip(i)
        
    def _get_tuple(self, sid):
        "Return stream contents in tuple form."

        return (
            sid,
            self._get_destination_ip(sid),
            self._get_source_ip(sid),
            self.get_store_item(sid, "STREAM_TYPE"),
            self._get_content(sid),
            self.get_store_item(sid, "STREAM_CONTENT"),
            self.get_store_item(sid, "STREAM_CHKSUM"),
            self.get_store_item(sid, "STREAM_PKEY").strip('\b')
        )       

    def get_stream(self, sid):
        "Return stream data in form of tuple."

        # Return specified stream data as tuple
        return self.stream_dict[sid].tuple()

if __name__ == "__main__":
    
    sm = StreamManager(123, "PKEYTEST", "localhost")
    stream = sm.pack_stream(stype="ACKN", content="Hello", dest_host="127.0.0.1", src_host="127.0.0.1", peer_key="PKEYTEST")
    print stream
    print sm.unpack_stream(stream)
    
    