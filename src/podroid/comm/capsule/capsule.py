'''
Created on Jul 21, 2013

This is the application level packet that is used as a basis for any
communications between server and client and vice-versa.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.1

import struct
import socket

from podroid.config.configuration import *


class Capsule(object):

    "Capsule definition."

    def __init__(self, captype="NULL", content='',
                 dest_host="127.0.0.1", src_host="127.0.0.1"):

        # Check length of content.
        if len(content) > constants.CAPS_CONTENT_LEN:
            raise Exception(
                'OverflowError: Content exceeded capsule limit of 40'
            )

        # Check length of capsule type.
        if len(captype) > constants.CAPS_TYPE_LEN:
            raise Exception(
                'OverflowError: Type exceeded capsule limit of 4'
            )

        # localhost - 127.0.0.1 mapping.
        if dest_host == "localhost":
            dest_host = constants.LOCAL_TEST_HOST
        if src_host == "localhost":
            src_host = constants.LOCAL_TEST_HOST

        self._dictionary = {
            'CAP_ID':
            str(
                uuid.uuid5(
                    uuid.NAMESPACE_URL, dest_host
                )
            )[0:constants.CAPS_ID_LEN],
            'CAP_DSTIP': self._ip_to_uint32(dest_host),
            'CAP_SCRIP': self._ip_to_uint32(src_host),
            'CAP_TYPE': captype.upper(),
            'CAP_CONTENT': content,
            'CAP_LEN': len(content),
            'CAP_CHKSUM': hmac.new(content).hexdigest()}

    def __setitem__(self, key, item):

            if key not in self._dictionary:
                raise KeyError("The key '{}' is not defined.".format(key))

            self._dictionary[key] = item

    def __getitem__(self, key):

        return self._dictionary[key]

    def pack(self):
        "Pack data into capsule. (i.e struct packing)"

        return struct.pack(
            "!8sII4s40sL32s",
            self._dictionary['CAP_ID'],
            self._dictionary['CAP_DSTIP'],
            self._dictionary['CAP_SCRIP'],
            self._dictionary['CAP_TYPE'],
            self._dictionary['CAP_CONTENT'],
            self._dictionary['CAP_LEN'],
            self._dictionary['CAP_CHKSUM']
        )

    def unpack(self, stream):
        "Unpack serial data into capsule."

        (
            self._dictionary['CAP_ID'],
            self._dictionary['CAP_DSTIP'],
            self._dictionary['CAP_SRCIP'],
            self._dictionary['CAP_TYPE'],
            self._dictionary['CAP_CONTENT'],
            self._dictionary['CAP_LEN'],
            self._dictionary['CAP_CHKSUM']
        ) = struct.unpack("!8sII4s40sL32s", stream)

    def __str__(self):
        "String representation of capsule."

        string = ''

        for (k, v) in self._dictionary.iteritems():
            string += str(v) + ':'

        return string.strip(':')

    def getid(self):
        "Return Capsule ID."

        return self._dictionary["CAP_ID"]

    def getdip(self):
        "Return Destination IP."

        return self._uint32_to_ip(self._dictionary["CAP_DSTIP"])

    def getsip(self):
        "Return Destination IP."

        return self._uint32_to_ip(self._dictionary["CAP_SRCIP"])

    def gettype(self):
        "Return Capsule protocol type."

        return self._dictionary["CAP_TYPE"]

    def getcontent(self):
        "Return capsule content if its integrity is maintained."
        if (hmac.new(self._dictionary["CAP_CONTENT"]).hexdigest()
                == self._dictionary["CAP_CHKSUM"]):
            return self._dictionary[
                "CAP_CONTENT"
            ][0:self._dictionary['CAP_LEN']]
        else:
            return None

    def tuple(self):
        "Return capsule in tuple form."

        return (
            self._dictionary['CAP_ID'],
            self.getdip(),
            self.getsip(),
            self._dictionary['CAP_TYPE'],
            self.getcontent(),
            self._dictionary['CAP_LEN'],
            self._dictionary['CAP_CHKSUM']
        )

    def _ip_to_uint32(self, ip):
        "Convert IPv4 Address into 32bit integer."

        t = socket.inet_aton(ip)
        return struct.unpack("!I", t)[0]

    def _uint32_to_ip(self, ipn):
        "Convert 32bit integer into IP Address."

        t = struct.pack("!I", ipn)
        return socket.inet_ntoa(t)


if __name__ == '__main__':

    Ctx = Capsule('TEST', 'This is a capsule test.')
    pkd = Ctx.pack()
    print 'Packed data is :', pkd
    Crx = Capsule()
    Crx.unpack(pkd)
    print "Unpacked data :", Crx.tuple()
