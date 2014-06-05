'''
Created on Aug 4, 2013

Handles packing and unpacking of streams to be sent
over the air.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"

from kivy import Logger

from cryptikchaos.env.configuration import constants

from cryptikchaos.libs.Storage.manager import StoreManager

from cryptikchaos.libs.utilities import generate_uuid
from cryptikchaos.libs.utilities import generate_token
from cryptikchaos.libs.utilities import compress
from cryptikchaos.libs.utilities import decompress
from cryptikchaos.libs.utilities import enum
from cryptikchaos.libs.utilities import num_to_bytes
from cryptikchaos.libs.utilities import bytes_to_num
from cryptikchaos.libs.utilities import md5hash

from cryptikchaos.libs.obscure import shuffler
from cryptikchaos.libs.obscure import unshuffler

from cryptikchaos.exceptions.streamExceptions import \
    StreamOverflowError

from cryptikchaos.comm.stream.stream import Stream

if constants.AES_AVAILABLE:
    Logger.info("AES Crypto available.")
    from Crypto.Cipher import AES
else:
    Logger.warn("AES Crypto unavailable.")

import struct

STREAM_TYPES = enum(UNAUTH=0, AUTH=1)


class StreamManager(StoreManager):
    "Stream manager class."

    def __init__(self, peerid, peerkey, peerhost):
        
        # Authorized keys
        self._valid_keys = (
            'STREAM_FLAG',
            'STREAM_TYPE' ,
            'STREAM_CONTENT',
            'STREAM_PKEY'
        )
        
        # Create store
        super(StreamManager, self).__init__("StreamStore", self._valid_keys)
        # Peer public key
        self.public_key = peerkey
        # Peer host
        self.peer_host = peerhost

    def __del__(self):
        
        # Clear stored streams
        if super(StreamManager, self):
            super(StreamManager, self).__del__()
                   
    def pack_stream(self, stream_type, stream_content, stream_host,
            stream_flag=STREAM_TYPES.AUTH, shared_key=None):
        "Pack data into stream."
                       
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
        stream_token = None
                
        # Check stream signing mode
        if stream_flag == STREAM_TYPES.UNAUTH:
            # Stream key is peer key
            ## NOTE peer public key is sent during 
            ## authentication.
            stream_token = num_to_bytes(self.public_key)
            
        elif stream_flag == STREAM_TYPES.AUTH:
            # Generate token at source side
            stream_token = generate_token(stream_uid, shared_key)
                                 
        # Shuffle content
        if constants.ENABLE_SHUFFLE:
            Logger.info("Scrambling content.")

            stream_content = shuffler(
                string=stream_content,
                iterations=constants.STREAM_CONT_SHUFF_ITER
            )
        
        # AES Encryption
        if constants.AES_AVAILABLE and stream_flag == STREAM_TYPES.AUTH:
            # AES Encrypt content in stream
            iv = md5hash(stream_token, hexdigest=False)
            AES_obj = AES.new(shared_key, AES.MODE_CBC, iv)
            stream_content = self.pad(stream_content)
            print stream_content, len(stream_content)
            stream_content = AES_obj.encrypt(stream_content)
            
        # Create stream object
        stream_obj = Stream(
            stream_uid, 
            stream_flag,
            stream_type,
            stream_content,
            stream_token,
        )
                
        # Add stream to store
        self.add_store(
            stream_uid, stream_obj.dict
        )

        if stream_flag == STREAM_TYPES.UNAUTH:
            Logger.debug("Packing Authentication Block.")

            # Pack store into authentication stream
            stream = struct.pack(
                "!I{}s{}s{}s{}s".format(
                    constants.STREAM_TYPE_LEN,
                    constants.STREAM_CONTENT_LEN,
                    constants.STREAM_PEER_KEY_LEN,
                    constants.STREAM_CHKSUM_LEN
                ),
                self.get_store_item(stream_uid, 'STREAM_FLAG'   ),
                self.get_store_item(stream_uid, 'STREAM_TYPE'   ),
                self.get_store_item(stream_uid, 'STREAM_CONTENT'),
                self.get_store_item(stream_uid, 'STREAM_PKEY'   ),
                stream_obj.gen_hmac()
            )
            
        elif stream_flag == STREAM_TYPES.AUTH:
            Logger.debug("Packing Message Block.")

            # Pack store into message block stream
            stream = struct.pack(
                "!I{}s{}s{}s{}s".format(
                    constants.STREAM_TYPE_LEN,
                    constants.STREAM_CONTENT_LEN,
                    constants.STREAM_TOKEN_LEN,
                    constants.STREAM_CHKSUM_LEN
                ),
                self.get_store_item(stream_uid, 'STREAM_FLAG'   ),
                self.get_store_item(stream_uid, 'STREAM_TYPE'   ),
                self.get_store_item(stream_uid, 'STREAM_CONTENT'),
                self.get_store_item(stream_uid, 'STREAM_PKEY'   ),
                stream_obj.gen_hmac()
            )
            
        else:
            Logger.error("Invalid Stream Flag received.")
            return None

        # Compress stream
        if constants.ENABLE_COMPRESSION:
            stream = compress(stream)
        
        return stream

    def unpack_stream(self, stream, shared_key=None):
        "Unpack serial data into stream."
        
        # Decompress data stream
        if constants.ENABLE_COMPRESSION:
            stream = decompress(stream)
        
        # Check if data is of expected chunk size
        if len(stream) != constants.STREAM_SIZE_AUTH_BLOCK and \
           len(stream) != constants.STREAM_SIZE_MSG_BLOCK:
            raise StreamOverflowError()
        
        if len(stream) == constants.STREAM_SIZE_AUTH_BLOCK:
            Logger.debug("Unpacking Authentication Block.")
            
            # Unpack auth stream to variables
            (     
                stream_flag,
                stream_type,
                stream_content,
                stream_token,
                stream_hmac
            ) = struct.unpack(
                "!I{}s{}s{}s{}s".format(
                    constants.STREAM_TYPE_LEN,
                    constants.STREAM_CONTENT_LEN,
                    constants.STREAM_PEER_KEY_LEN,
                    constants.STREAM_CHKSUM_LEN
                ), stream
            )
            
        elif len(stream) == constants.STREAM_SIZE_MSG_BLOCK:
            Logger.debug("Unpacking Message Block.")

            # Unpack msg block stream to variables
            (     
                stream_flag,
                stream_type,
                stream_content,
                stream_token,
                stream_hmac
            ) = struct.unpack(
                "!I{}s{}s{}s{}s".format(
                    constants.STREAM_TYPE_LEN,
                    constants.STREAM_CONTENT_LEN,
                    constants.STREAM_TOKEN_LEN,
                    constants.STREAM_CHKSUM_LEN
                ), stream
            )
            
        else:
            Logger.error("Invalid Stream Length received.")
            return [None]*3
                       
        # Remove all null characters if present
        stream_content = stream_content.rstrip('\0')
        stream_token =  stream_token.rstrip('\0')
        
        # Get  uid
        stream_uid = generate_uuid(self.peer_host)
                                               
        # Get stream object
        stream_obj = Stream(
                     stream_uid, 
                     stream_flag,
                     stream_type,
                     stream_content,
                     stream_token,
                )

        # Verify stream integrity
        if not stream_obj.check_hmac(stream_hmac):
            Logger.error("Stream Checksum mismatch.")
            return [None]*3
        
        # Check stream signing mode
        if stream_flag == STREAM_TYPES.UNAUTH:
            # Stream key is peer public key
            # Convert public key bytes to number
            stream_obj.update_token(bytes_to_num(stream_token))
                        
        elif stream_flag == STREAM_TYPES.AUTH:            
            # Generate token at destination side
            stream_challenge_token = generate_token(
                stream_uid,
                shared_key,
            )
                      
            # Perform key challenge
            if stream_challenge_token != stream_token:
                Logger.error("Token challenge Fail")
                return [None]*3
            else:
                Logger.info("Token challenge Pass")
            
        # AES Decryption
        if constants.AES_AVAILABLE and stream_flag == STREAM_TYPES.AUTH:            
            # Decrypt stream content
            iv = md5hash(stream_token, hexdigest=False)
            AES_obj = AES.new(shared_key, AES.MODE_CBC, iv)
            stream_content = AES_obj.decrypt(stream_content)
            stream_content = self.unpad(stream_content)
            print stream_content, len(stream_content)
        
        # Unshuffle content
        if constants.ENABLE_SHUFFLE:
            
            Logger.info("Unscrambling content.")
            
            stream_obj.update_content (
                unshuffler(
                    shuffled_string=stream_content,
                    iterations=constants.STREAM_CONT_SHUFF_ITER
                )
            )
        
        # Add stream to store
        self.add_store(stream_uid, stream_obj.dict)
        
        return self._get_tuple(stream_uid)
            
    def _get_tuple(self, sid):
        "Return stream contents in tuple form."

        return (
            self.get_store_item(sid, "STREAM_TYPE"   ),
            self.get_store_item(sid, "STREAM_CONTENT"),
            self.get_store_item(sid, "STREAM_PKEY"   )
        )

    def get_stream(self, sid):
        "Return stream data in form of tuple."

        # Return specified stream data
        return self.get_store(sid)

    if constants.AES_AVAILABLE:
        def pad (self, s, BS=16):
        
            if len(s) % 16 == 0:
                return s
            else:
                return s + '\0' * (constants.STREAM_CONTENT_LEN-len(s))
    
        def unpad (self, s):
        
            return s.rstrip('\0')

if __name__ == "__main__":
    
    SM = StreamManager(123, "PKEYTEST", "localhost")
    S = SM.pack_stream(
        stream_type="ACKN", 
        stream_content="Hello", 
        stream_host="127.0.0.1",
        public_key="PKEYTEST"
    ) 
    print S
    print SM.unpack_stream(S)
    
    