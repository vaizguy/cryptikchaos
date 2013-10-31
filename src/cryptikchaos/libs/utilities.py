'''
Created on Oct 17, 2013

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.4

from cryptikchaos.config.configuration import constants

from kivy import Logger

from time import gmtime, strftime

import struct
import socket
import uuid
import hashlib
import zlib
import json
import base64
import random
import re
import os

def ip_to_uint32(ip):
    """
    Convert IPv4 Address into 32bit integer.
    """

    t = socket.inet_aton(ip)
    return struct.unpack("!I", t)[0]

def uint32_to_ip(ipn):
    """
    Convert 32bit integer into IP Address.
    """

    t = struct.pack("!I", ipn)
    return socket.inet_ntoa(t)

def generate_uuid(host):
    """
    Generate capsule UID for particular destination host.
    """

    return str(
        uuid.uuid5(uuid.NAMESPACE_URL, host)
    )[0:constants.STREAM_ID_LEN]

def generate_token(uid, pkey):
    """
    Generate capsule signature from capsule destination uid and
    peer public key.
    """

    return hashlib.sha512(
        hashlib.sha512(uid).hexdigest() + \
        hashlib.sha512(pkey).hexdigest()
    ).hexdigest()
    
def get_my_ip():
    """
    Attempt to connect to an Internet host in order to determine the
    local machine's IP address.
    """
    
    s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    host = 'localhost'
    try:
        s.connect( ( "www.google.com", 80 ) )
    except:
        Logger.debug('No active internet connection.')
        return host
    else:
        host = s.getsockname()[0]
        s.close()
        return host 
    
def compress(stream):
    """
    Compress stream using zlib lib.
    """
    
    return zlib.compress(stream)

def decompress(stream):
    """
    Decompress stream using zlib.
    """
    
    return zlib.decompress(stream)

def wrap_line(line, cmax=100, delim='\n'):
    """
    Factors a line in to max num of chars seperated
    by delimiter.
    """
    
    # check if factoring required
    if len(line) <= cmax:
        return line
    
    # Remove any newline characters in the line
    line = re.sub(r"\r\n", " ", line)
    # Get length of line
    length = len(line)
    # Factor line into n number of lines of max chars each
    lines = [ line[i: i+cmax] for i in xrange(0, length, cmax) ]
    
    return "{}".format(delim.join(lines))

def get_time():
    """
    Get the time as a string.
    """
    
    return strftime(constants.TIME_FORMAT, gmtime())

def serialize(dictionary):
    """
    Converts dictionary into network tx friendly string,
    returns string
    """
    
    return base64.b64encode(
        zlib.compress(
            json.dumps(
                dictionary
            )
        )
    )
    
def deserialize(serialstr):
    """
    Deserializes network serialized dictionary, returns dict
    """
    
    return json.loads(
        zlib.decompress(
            base64.b64decode(
                serialstr
            )
        )
    )
    
def criptiklogo():
    """
    Read the logo and return it as string.
    """
    
    logofile = "{}/db/logo".format(
        constants.PROJECT_PATH
    )
    
    try:
        # Open and read logo file
        with open(logofile, 'r') as f:
            logo = "".join(f.readlines())
    except IOError:
        # No logo present
        Logger.error("Failed to read cryptikchaos logo.")
        return None
    else:
        # Return logo if success
        return logo.format(
            os.getenv("USER"),
            __version__
       )

def random_color_code():
    
    r = lambda: random.randint(0,255)
    
    while True:
        # Get Random color code
        rcc ='#{:02X}{:02X}{:02X}'.format(r(),r(),r())
        # Filter App b/w text colors
        if (rcc != "#000000" or rcc != "#FFFFFF"):
            break
        
    return rcc


if __name__ == "__main__":
    ## Test for factor_line
    import string, random
       
    s = "".join(random.choice(string.ascii_uppercase + string.digits) for x in range(512))
    
    print "line", factor_line(s)
            