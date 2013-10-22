'''
Created on Oct 17, 2013

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.3

from cryptikchaos.config.configuration import constants

from kivy import Logger

import struct
import socket
import uuid
import hashlib
import zlib

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
    )[0:constants.CAPS_ID_LEN]

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

def factor_line(line, cmax=75, delim='\n'):
    """
    Factors a line in to max num of chars seperated
    by delimiter.
    """
    # Get length of line
    length = len(line)
    # Factor line into n number of lines of max chars each
    lines = [ line[i: i+cmax] for i in xrange(0, length/cmax, cmax) ]
    # Append remaining characters if total number of chars is not 
    # a factor of max
    lines.append(line[-(length%cmax):])
    
    return delim.join(lines)
