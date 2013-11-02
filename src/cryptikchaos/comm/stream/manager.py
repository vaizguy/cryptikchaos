'''
Created on Aug 4, 2013

Handles packing and unpacking of streams to be sent
over the air.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.5

from kivy import Logger

from cryptikchaos.comm.stream.stream import Stream
from cryptikchaos.exceptions.streamExceptions import \
    StreamOverflowError
    
import traceback
    
class StreamManager:

    "Stream manager class."

    def __init__(self, peerkey):

        # Dictionary of all packed/unpacked streams
        self.stream_dict = {}
        # Peer public key
        self.peer_key = peerkey

    def __del__(self):

        # Clear stored streams
        try:
            del self.stream_dict
        except AttributeError:
            return None
            

    def pack_stream(self, captype="NULL", capcontent='',
                     dest_host="127.0.0.1", src_host="127.0.0.1"):
        "Pack data into stream."

        try:
            # Create and populate stream with specified data
            stream = Stream(self.peer_key, captype, capcontent, dest_host, src_host)
        except StreamOverflowError:
            Logger.error("{}".format(traceback.format_exc()))
            Logger.error("Could not pack stream.")
            return None
        else:
            # Store stream
            self.stream_dict[stream.getid()] = stream
            
            # Return stream as packed struct
            return stream.pack()

    def unpack_stream(self, serial):
        "Unpack serial data into stream."

        # Create empty stream
        stream = Stream()

        try:
            # Unpack into stream
            stream.unpack(serial)
        except StreamOverflowError:
            Logger.error("{}".format(traceback.format_exc()))
            Logger.error("Stream format is invalid, Unpack failed.")
            return tuple([None]*8)
        else:
            # Store unpacked stream
            self.stream_dict[stream.getid()] = stream
            # Return unpacked data as tuple
            return stream.tuple()

    def get_stream(self, cid):
        "Return stream data in form of tuple."

        # Return specified stream data as tuple
        return self.stream_dict[cid].tuple()
