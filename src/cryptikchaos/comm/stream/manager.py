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
            'STREAM_TYPE' ,
            'STREAM_CONTENT',
            'STREAM_PKEY',
            'STREAM_CHKSUM'
        )
        
        # Create store
        super(StreamManager, self).__init__("StreamStore", self._valid_keys)
        # Peer public key
        self.peer_key = peerkey
        # Peer host
        self.peer_host = peerhost

    def __del__(self):
        
        # Clear stored streams
        if StoreManager:
            StoreManager.__del__(self)
            
    def _gen_hmac(self, flag, stype, content, uid, key):
        "Generate stream hmac."
        
        return hmac.new(str(flag)+stype+content+uid+key).hexdigest()
        
    def _prepare_stream(self, stream_type, stream_content, stream_flag, stream_host, peer_key):
        "Create new stream store."
        
        # Check length of content.
        if len(stream_content) > constants.STREAM_CONTENT_LEN:
            raise StreamOverflowError(constants.STREAM_CONTENT_LEN)

        # Check length of capsule type.
        if len(stream_type) > constants.STREAM_TYPE_LEN:
            raise StreamOverflowError(constants.STREAM_TYPE_LEN)
        
        # Generate uid
        stream_uid = generate_uuid(stream_host)
        # Stream type
        stream_type = stream_type.upper()
        # Stream peer key
        stream_key = None
                
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
            
        # Generate checksum before shuffle
        stream_hmac = self._gen_hmac(
            flag=stream_flag, 
            stype=stream_type,
            content=stream_content,
            uid=stream_uid,
            key=stream_key
        )
                              
        # Shuffle content
        if constants.ENABLE_SHUFFLE:
            Logger.info("Scrambling content.")

            stream_content = shuffler(
                string=stream_content,
                iterations=constants.STREAM_CONT_SHUFF_ITER
            )
        
        dictionary = {
            'STREAM_FLAG'    :stream_flag,
            'STREAM_TYPE'    :stream_type,
            'STREAM_CONTENT' :stream_content,
            'STREAM_PKEY'    :stream_key,
            'STREAM_CHKSUM'  :stream_hmac
        }
                
        # Add stream to store
        self.add_store(stream_uid, dictionary)
        
        return stream_uid

    def pack_stream(self, stream_type, stream_content, stream_host,
            stream_flag=STREAM_TYPES.AUTH, peer_key=None):
        "Pack data into stream."
                
        # Create new stream
        sid = self._prepare_stream(
            stream_type=stream_type, 
            stream_content=stream_content, 
            stream_flag=stream_flag, 
            stream_host=stream_host,
            peer_key=peer_key
        )

        # Pack store into stream
        stream = struct.pack(
            "!I{}s{}s{}s{}s".format(
                constants.STREAM_TYPE_LEN,
                constants.STREAM_CONTENT_LEN,
                constants.STREAM_PKEY_HASH_LEN,
                constants.STREAM_CHKSUM_LEN
            ),
            self.get_store_item(sid, 'STREAM_FLAG'   ),
            self.get_store_item(sid, 'STREAM_TYPE'   ),
            self.get_store_item(sid, 'STREAM_CONTENT'),
            self.get_store_item(sid, 'STREAM_PKEY'   ),
            self.get_store_item(sid, 'STREAM_CHKSUM' )
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
            stream_type,
            stream_content,
            stream_key,
            stream_hmac
        ) = struct.unpack(
                "!I{}s{}s{}s{}s".format(
                constants.STREAM_TYPE_LEN,
                constants.STREAM_CONTENT_LEN,
                constants.STREAM_PKEY_HASH_LEN,
                constants.STREAM_CHKSUM_LEN
            ), stream
        )
        
        # Remove all null characters if present in content
        stream_content = stream_content.rstrip('\0')
        
        # Unshuffle content
        if constants.ENABLE_SHUFFLE:
            
            Logger.info("Unscrambling content.")
            
            stream_content = unshuffler(
                shuffled_string=stream_content,
                iterations=constants.STREAM_CONT_SHUFF_ITER
            )
            
        # Get  uid
        stream_uid = generate_uuid(self.peer_host)
        
        # Verify stream integrity
        if (
            self._gen_hmac(
                flag=stream_flag, 
                stype=stream_type, 
                content=stream_content, 
                uid=stream_uid, 
                key=stream_key
            ) != stream_hmac
        ):
            return [None]*8
        
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
            'STREAM_TYPE'    :stream_type,
            'STREAM_CONTENT' :stream_content,
            'STREAM_CHKSUM'  :stream_hmac,
            'STREAM_PKEY'    :stream_key           
        }
                        
        # Add stream to store
        self.add_store(stream_uid, dictionary)
        
        return self._get_tuple(stream_uid)
            
    def _get_tuple(self, sid):
        "Return stream contents in tuple form."

        return (
            self.get_store_item(sid, "STREAM_TYPE"   ),
            self.get_store_item(sid, "STREAM_CONTENT"),
            self.get_store_item(sid, "STREAM_PKEY"   ).strip('\b')
        )

    def get_stream(self, sid):
        "Return stream data in form of tuple."

        # Return specified stream data
        return self.get_store(sid)


if __name__ == "__main__":
    
    SM = StreamManager(123, "PKEYTEST", "localhost")
    S = SM.pack_stream(
        stream_type="ACKN", 
        stream_content="Hello", 
        stream_host="127.0.0.1",
        peer_key="PKEYTEST"
    ) 
    print S
    print SM.unpack_stream(S)
    
    