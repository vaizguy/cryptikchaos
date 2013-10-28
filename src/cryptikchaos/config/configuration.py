'''
Created on Aug 5, 2013

Contains all unchangable constants used accross application.
Must be changed with care.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.4

import uuid
import hmac
import os
import hashlib
import random
import string

from cryptikchaos.config import constants

from cryptikchaos.libs.utilities import get_time

# ---Application Environment----------------------------------------------####

constants.TIME_FORMAT = "%a, %d %b %Y %H:%M:%S +0000"
# ------------------------------------------------------------------------####

# ---Project Path CONSTANTS-----------------------------------------------####

constants.PROJECT_PATH = "{}/..".format(
    os.path.dirname(os.path.realpath(__file__))
)
# ------------------------------------------------------------------------####

# ---peer attribute constants---------------------------------------------####

constants.PEER_ID = uuid.getnode()
constants.PEER_PORT = 1597
constants.PEER_HOST = "127.0.0.1"
constants.PEER_NAME = "MYPOD"
# ------------------------------------------------------------------------####

# ------------------GUI Attribute CONSTANTS-------------------------------####

constants.GUI_LABEL_LEFT_PADDING = ""
constants.GUI_WELCOME_MSG = """
{}==========================
{}CryptikChaos v.{}
{}==========================
{}[{}]

{}>> Welcome to CryptikChaos P2P Net <<
{}>> Enter "help" for command listing <<
""".format(
    constants.GUI_LABEL_LEFT_PADDING,
    constants.GUI_LABEL_LEFT_PADDING,
    str(__version__),
    constants.GUI_LABEL_LEFT_PADDING,
    constants.GUI_LABEL_LEFT_PADDING,
    get_time(),
    constants.GUI_LABEL_LEFT_PADDING,
    constants.GUI_LABEL_LEFT_PADDING
)

constants.GUI_LABEL_PROMPT_SYM = ">> "
constants.GUI_LABEL_PROMPT = "{}{}".format(
    constants.GUI_LABEL_LEFT_PADDING,
    constants.GUI_LABEL_PROMPT_SYM
)
# ------------------------------------------------------------------------####

# ------------------Protocol Capsule type CONSTANTS-----------------------####

constants.PROTO_BULK_TYPE = "BULK"
constants.PROTO_MACK_TYPE = "MACK"

constants.PROTO_AUTH_TYPE = "AUTH"
constants.PROTO_AACK_TYPE = "AACK"
# ------------------------------------------------------------------------####

# ------------------STREAM CONSTANTS-------------------------------------####

# Capsule Content Length
constants.STREAM_CONTENT_LEN = 128
# Capsule Type length
constants.STREAM_TYPE_LEN = 4
# Capsule ID Length
constants.STREAM_ID_LEN = 8
# Capsule chksum length
constants.STREAM_CHKSUM_LEN = 32
# Capsule content length byte length
constants.STREAM_CONTENTL_LEN = 4
# Capsule IP integer repr length
constants.STREAM_DST_IP_LEN = 4
constants.STREAM_SCR_IP_LEN = 4
# Capsule peer key hash length
constants.STREAM_PKEY_HASH_LEN = 128

# Capsule size
constants.STREAM_SIZE = constants.STREAM_CONTENT_LEN + \
    constants.STREAM_TYPE_LEN + \
    constants.STREAM_ID_LEN + \
    constants.STREAM_CHKSUM_LEN + \
    constants.STREAM_CONTENTL_LEN + \
    constants.STREAM_DST_IP_LEN + \
    constants.STREAM_SCR_IP_LEN + \
    constants.STREAM_PKEY_HASH_LEN

# Capsule shuffle iterations
constants.STREAM_CONT_SHUFF_ITER = 1000
# Capsule line delimiter
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
# Local Test IP
constants.LOCAL_TEST_HOST = "127.0.0.1"
# Local Test Port
constants.LOCAL_TEST_PORT = 8888
# Local Test PEer ID
constants.LOCAL_TEST_PEER_ID = 888
# Local Test keys
constants.LOCAL_TEST_CLIENT_KEY = hashlib.sha512(
    "TEST_CLIENT_KEY{}".format(constants.PEER_ID)
).hexdigest()
constants.LOCAL_TEST_SERVER_KEY = hashlib.sha512(
    "TEST_SERVER_KEY{}".format(constants.PEER_ID)
).hexdigest()
# Test ID
constants.LOCAL_TEST_STREAM_ID = str(
    uuid.uuid5(
        uuid.NAMESPACE_URL,
        constants.LOCAL_TEST_HOST
    )
)[0:constants.STREAM_ID_LEN]
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

# ---Application switches-------------------------------------------------####
constants.ENABLE_TEST_MODE = True
constants.ENABLE_COMPRESSION = True
constants.ENABLE_SHUFFLE = True
# ------------------------------------------------------------------------####
