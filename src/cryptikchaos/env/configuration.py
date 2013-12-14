'''
Created on Aug 5, 2013

Contains all unchangable constants used accross application.
Must be changed with care.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.5

import uuid
import hmac
import os
import random
import string

from cryptikchaos.env import constants

from cryptikchaos.libs.utilities import get_time
from cryptikchaos.libs.utilities import criptiklogo
from cryptikchaos.libs.utilities import get_my_ip
from cryptikchaos.libs.utilities import generate_key
from cryptikchaos.libs.utilities import md5hash

try:
    import pympler
except ImportError:
    constants.PYMPLER = False
else:
    constants.PYMPLER = True

try:
    import networkx
    import matplotlib.pyplot
except ImportError:
    constants.NETWORKX = False
else:
    constants.NETWORKX = True
    
# ---Application switches-------------------------------------------------####

constants.ENABLE_TEST_MODE   = True
constants.ENABLE_COMPRESSION = True
constants.ENABLE_SHUFFLE     = True
constants.ENABLE_TLS         = True
# ------------------------------------------------------------------------####

# ---Application Environment----------------------------------------------####

constants.TIME_FORMAT = "%a, %d %b %Y %H:%M:%S +0000"
constants.REBIND_CHECK = True
# ------------------------------------------------------------------------####

# ---Project Path CONSTANTS-----------------------------------------------####

constants.PROJECT_PATH = "{}/..".format(
    os.path.dirname(os.path.realpath(__file__))
)
constants.KIVY_RESOURCE_PATH = "{}/fonts".format(constants.PROJECT_PATH)
# ------------------------------------------------------------------------####

# ---peer attribute constants---------------------------------------------####

constants.PEER_ID = md5hash(str(uuid.getnode()))[0:8]
constants.PEER_PORT = 1597
constants.PEER_HOST = get_my_ip()
constants.PEER_NAME = "MYPOD"
# ------------------------------------------------------------------------####

# ------------------GUI Attribute CONSTANTS-------------------------------####

constants.GUI_FONT_TYPE = "DroidSansMono.ttf"
constants.GUI_FONT_SIZE = 14
constants.GUI_LABEL_LEFT_PADDING = ""
constants.GUI_LOGO = criptiklogo()
constants.GUI_WELCOME_MSG = """
{}
{}[{}]

{}>> Welcome to CryptikChaos P2P Net <<
{}>> Drag left edge for navigation <<
{}>> Enter "help" for command listing <<
""".format(
    constants.GUI_LOGO,
    constants.GUI_LABEL_LEFT_PADDING,
    get_time(),
    constants.GUI_LABEL_LEFT_PADDING,
    constants.GUI_LABEL_LEFT_PADDING,
    constants.GUI_LABEL_LEFT_PADDING
)

constants.GUI_LABEL_PROMPT_SYM = ">> "
constants.GUI_LABEL_PROMPT = "{}{}".format(
    constants.GUI_LABEL_LEFT_PADDING,
    constants.GUI_LABEL_PROMPT_SYM
)
constants.GUI_PEER_REPR = "PID:{}--{}:{}"
# ------------------------------------------------------------------------####

# ------------------Protocol Stream type CONSTANTS-----------------------####

constants.PROTO_BULK_TYPE = "BULK"
constants.PROTO_MACK_TYPE = "MACK"

constants.PROTO_AUTH_TYPE = "AUTH"
constants.PROTO_AACK_TYPE = "AACK"
# ------------------------------------------------------------------------####

# ------------------STREAM CONSTANTS-------------------------------------####

# Stream Content Length
constants.STREAM_CONTENT_LEN = 128
# Stream Type length
constants.STREAM_TYPE_LEN = 4
# Stream flag Length
constants.STREAM_FLAG_LEN = 4
# Stream id length
constants.STREAM_ID_LEN = 8
# Stream chksum length
constants.STREAM_CHKSUM_LEN = 32
# Stream peer key hash length
constants.STREAM_PKEY_HASH_LEN = 64

# Stream size
constants.STREAM_SIZE = constants.STREAM_CONTENT_LEN + \
    constants.STREAM_TYPE_LEN + \
    constants.STREAM_FLAG_LEN + \
    constants.STREAM_CHKSUM_LEN + \
    constants.STREAM_PKEY_HASH_LEN

# Stream shuffle iterations
constants.STREAM_CONT_SHUFF_ITER = 1000
# Stream line delimiter
constants.STREAM_LINE_DELIMITER = '\r\n'
# ------------------------------------------------------------------------####

# ------------------TEST CONSTANTS----------------------------------------####
# Test server name
constants.LOCAL_TEST_PEER_NAME = "TSERVER"
# Test string message
constants.LOCAL_TEST_STR = ''.join(
    random.choice(string.ascii_uppercase + string.digits) for x in range(
        constants.STREAM_CONTENT_LEN
    )
)
# Test capsule type
constants.LOCAL_TEST_STREAM_TYPE = "MTST"
# If not in test mode get LAN IP
# Local Test IP
constants.LOCAL_TEST_HOST = "127.0.0.1"
# Local Test Port
constants.LOCAL_TEST_PORT = 8888
# Local Test PEer ID
constants.LOCAL_TEST_PEER_ID = md5hash(
    constants.LOCAL_TEST_PEER_NAME
)[0:8]
# Test ID
constants.LOCAL_TEST_STREAM_ID = str(
    uuid.uuid5(
        uuid.NAMESPACE_URL,
        constants.LOCAL_TEST_HOST
    )
)[0:constants.STREAM_ID_LEN]
# Local Test keys
constants.LOCAL_TEST_CLIENT_KEY = generate_key(constants.LOCAL_TEST_STREAM_ID)
constants.LOCAL_TEST_SERVER_KEY = generate_key(constants.LOCAL_TEST_PEER_ID)
# Test chksum
constants.LOCAL_TEST_STREAM_CHKSUM = hmac.new(
    constants.LOCAL_TEST_STR
).hexdigest()
# ------------------------------------------------------------------------####

# ---Help documentation printer constants---------------------------------####

constants.DOC_LEADER = ""
constants.DOC_HEADER = "Documented commands (type help <command>):"
constants.MISC_HEADER = "Miscellaneous help topics:"
constants.UNDOC_HEADER = "Undocumented commands:"
constants.NOHELP = "*** No help on %s"
constants.RULER = '-'
# ------------------------------------------------------------------------####

# ---SSL Field requirements constants-------------------------------------####
constants.SSL_CERT_FIELDS = ('C', 'CN', 'O', 'ST', 'emailAddress', 'OU')
constants.SSL_POST_VERIF_VALUES = {
    1:["cryptikchaosCA", "cryptikchaos", "criptikchaostest"], 
    4:["cryptikchaos@googlegroups.com"]
}
# ------------------------------------------------------------------------####

