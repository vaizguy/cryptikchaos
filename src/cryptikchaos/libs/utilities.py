'''
Created on Oct 17, 2013

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.2

from cryptikchaos.config.configuration import constants

import struct
import socket
import uuid
import hashlib

def ip_to_uint32(ip):
    "Convert IPv4 Address into 32bit integer."

    t = socket.inet_aton(ip)
    return struct.unpack("!I", t)[0]

def uint32_to_ip(ipn):
    "Convert 32bit integer into IP Address."

    t = struct.pack("!I", ipn)
    return socket.inet_ntoa(t)

def generate_uuid(host):
    "Generate UUID from host."

    return str(
        uuid.uuid5(uuid.NAMESPACE_URL, host)
    )[0:constants.CAPS_ID_LEN]

def generate_token(uid, pkey):
    "Generate capsule signature."

    return hashlib.sha512(
        hashlib.sha512(uid).hexdigest() + \
        hashlib.sha512(pkey).hexdigest()
    ).hexdigest()
        