'''
Created on Oct 17, 2013

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"

from kivy import Logger

from time import gmtime, strftime
from struct import pack, unpack
from socket import inet_aton, inet_ntoa, socket, AF_INET, SOCK_STREAM, SOCK_DGRAM, error
from uuid import uuid4, uuid5, NAMESPACE_URL, getnode
from hashlib import sha512, sha256, md5
from zlib    import compress as zlib_compress, \
    decompress as zlib_decompress
from json import dumps, loads
from base64 import b64encode, b64decode
from random import choice
from re import sub
from urllib2 import urlopen, URLError
from os.path import dirname, realpath


def md5hash(string, hexdigest=True):
    "Generate md5 hash from string."

    if hexdigest:
        return md5(string).hexdigest()
    else:
        return md5(string).digest()


def ip_to_uint32(ip):
    """
    Convert IPv4 Address into 32bit integer.
    """

    t = inet_aton(ip)
    return unpack("!I", t)[0]


def uint32_to_ip(ipn):
    """
    Convert 32bit integer into IP Address.
    """

    t = pack("!I", ipn)
    return inet_ntoa(t)


def generate_uuid(host=None):
    """
    Generate capsule UID for particular host.
    """

    return str(
        uuid5(NAMESPACE_URL, host)
    )[0:8]


def generate_auth_token():

    return uuid4().hex


def generate_token(uid, pkey):
    """
    Generate capsule signature from capsule destination uid and
    peer public key.
    """

    return sha256(
        "{}{}".format(
            sha512(uid).digest(),
            sha512(pkey).digest()
        )
    ).digest()


def ip_address_is_valid(address):
    "Check for valid IP address format"

    try:
        inet_aton(address)
    except error:
        return False
    else:
        return True


def get_nat_ip():
    "Get IP of NAT."

    s = socket(AF_INET, SOCK_STREAM)
    host = '127.0.0.1'
    try:
        s.connect(("www.google.com", 80))
    except error:
        Logger.debug('No active NAT connection.')
        return host
    else:
        host = s.getsockname()[0]
        s.close()
        return host


def get_my_ip():
    "Get my public IP address or if offline get my NAT IP."

    try:
        # Get IP from curlmyip.com which gives the raw ip address
        my_ip = urlopen('http://curlmyip.com').read().strip()

        # Check for portal redirects if offline
        if not ip_address_is_valid(my_ip):
            my_ip = get_local_ip()

    except URLError:
        Logger.debug('No active internet connection.')
        # If offline return host
        my_ip = get_local_ip()

    return my_ip


def get_local_ip():

    try:
        my_ip = [(s.connect(('8.8.8.8', 80)), s.getsockname()[0],
                  s.close()) for s in [socket(AF_INET, SOCK_DGRAM)]][0][1]
    except error:
        return "127.0.0.1"
    else:
        return my_ip


def compress(stream):
    """
    Compress stream using zlib lib.
    """

    return zlib_compress(stream)


def decompress(stream):
    """
    Decompress stream using zlib.
    """

    return zlib_decompress(stream)


def wrap_line(line, cmax=100, delim='\n'):
    """
    Factors a line in to max num of chars seperated
    by delimiter.
    """

    # Convert cmax to int
    if isinstance(cmax, float):
        cmax = int(cmax)

    # check if factoring required
    if len(line) <= cmax:
        return line

    # Remove any newline characters in the line
    line = sub(r"\r\n", " ", line)
    # Get length of line
    length = len(line)
    # Factor line into n number of lines of max chars each
    lines = [line[i: i + cmax] for i in xrange(0, length, cmax)]

    return "{}".format(delim.join(lines))


def get_time():
    """
    Get the time as a string.
    """

    return strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())


def serialize(dictionary):
    """
    Converts dictionary into network tx friendly string,
    returns string.
    """

    return b64encode(
        compress(
            dumps(
                dictionary
            )
        )
    )


def deserialize(serialstr):
    """
    Deserializes network serialized dictionary, returns dict.
    """

    return loads(
        decompress(
            b64decode(
                serialstr
            )
        )
    )


def criptiklogo():
    """
    Read the logo and return it as string.
    """

    logofile = "{}/../data/logo".format(
        dirname(realpath(__file__))
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
            md5hash(str(getnode()))[0:8],
            __version__
        )


def enum(**enums):

    return type('Enum', (), enums)


def num_to_bytes(num):

    num = hex(num)[2:].rstrip('L')
    if len(num) % 2:
        return ('0%s' % num).decode('hex')
    return num.decode('hex')


def bytes_to_num(bytes_repr):

    return int(bytes_repr.encode('hex'), 16)


def long2hex(self, long_num):

    return hex(long_num).rstrip("L").lstrip("0x") or "0"


if __name__ == "__main__":
    # Test for factor_line
    import string

    s = "".join(choice(string.ascii_uppercase + string.digits)
                for x in range(512))

    print "line", wrap_line(s)
