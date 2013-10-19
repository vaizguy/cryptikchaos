'''
Created on Aug 5, 2013

Contains all unchangable constants used accross application.
Must be changed with care.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.3

import uuid
import hmac
import os
import hashlib
import constants


# ---peer attribute constants---------------------------------------------####

constants.PEER_ID = uuid.getnode()
constants.PEER_PORT = 1597
constants.PEER_HOST = "127.0.0.1"
constants.PEER_NAME = "MYPOD"
# ------------------------------------------------------------------------####

# ------------------GUI Attribute CONSTANTS-------------------------------####

constants.GUI_LABEL_LEFT_PADDING = ""
constants.GUI_WELCOME_MSG = """
""" + constants.GUI_LABEL_LEFT_PADDING + """CryptikChaos v.""" + str(__version__) + """
----------------------
  
""" + constants.GUI_LABEL_LEFT_PADDING + """>> Welcome to CryptikChaos P2P Net <<
""" + constants.GUI_LABEL_LEFT_PADDING + """>> Enter "help" for command listing <<\n"""

constants.GUI_LABEL_PROMPT_SYM = ">> "
constants.GUI_LABEL_PROMPT = constants.GUI_LABEL_LEFT_PADDING + \
    constants.GUI_LABEL_PROMPT_SYM
# ------------------------------------------------------------------------####

# ------------------Project Path CONSTANTS--------------------------------####

constants.PROJECT_PATH = os.path.dirname(os.path.realpath(__file__)) + "/.."
# ------------------------------------------------------------------------####

# ------------------Protocol Capsule type CONSTANTS-----------------------####

constants.PROTO_BULK_TYPE = "BULK"
constants.PROTO_MACK_TYPE = "MACK"

constants.PROTO_AUTH_TYPE = "AUTH"
constants.PROTO_AACK_TYPE = "AACK"
# ------------------------------------------------------------------------####

# ------------------CAPSULE CONSTANTS-------------------------------------####

# Capsule Content Length
constants.CAPS_CONTENT_LEN = 64
# Capsule Type length
constants.CAPS_TYPE_LEN = 4
# Capsule ID Length
constants.CAPS_ID_LEN = 8
# Capsule chksum length
constants.CAPS_CHKSUM_LEN = 32
# Capsule content length byte length
constants.CAPS_CONTENTL_LEN = 4
# Capsule IP integer repr length
constants.CAPS_DST_IP_LEN = 4
constants.CAPS_SCR_IP_LEN = 4
# Capsule peer key hash length
constants.CAPS_PKEY_HASH_LEN = 128

# Capsule size
constants.CAPSULE_SIZE = constants.CAPS_CONTENT_LEN + \
    constants.CAPS_TYPE_LEN + \
    constants.CAPS_ID_LEN + \
    constants.CAPS_CHKSUM_LEN + \
    constants.CAPS_CONTENTL_LEN + \
    constants.CAPS_DST_IP_LEN + \
    constants.CAPS_SCR_IP_LEN + \
    constants.CAPS_PKEY_HASH_LEN
# ------------------------------------------------------------------------####

# ------------------TEST CONSTANTS----------------------------------------####
# Test server name
constants.LOCAL_TEST_PEER_NAME = "TSERVER"
# Test string message
constants.LOCAL_TEST_STR = "Hello World!"
# Test capsule type
constants.LOCAL_TEST_CAPS_TYPE = "TEST"
# Local Test IP
constants.LOCAL_TEST_HOST = "127.0.0.1"
# Local Test Port
constants.LOCAL_TEST_PORT = 8888
# Local Test PEer ID
constants.LOCAL_TEST_PEER_ID = 888
# Local Test keys
constants.LOCAL_TEST_CLIENT_KEY = hashlib.sha512(
                                      "TEST_CLIENT_KEY" + \
                                      str(constants.PEER_ID)
                                  ).hexdigest()
constants.LOCAL_TEST_SERVER_KEY = hashlib.sha512(
                                      "TEST_SERVER_KEY" + \
                                      str(constants.PEER_ID)
                                  ).hexdigest()
# Test ID
constants.LOCAL_TEST_CAPS_ID = str(
    uuid.uuid5(uuid.NAMESPACE_URL,
               constants.LOCAL_TEST_HOST))[0:constants.CAPS_ID_LEN]
# Test chksum
constants.LOCAL_TEST_CAPS_CHKSUM = hmac.new(
    constants.LOCAL_TEST_STR
).hexdigest()
# ------------------------------------------------------------------------####

# ---Help documentation printer constants---------------------------------####

constants.DOC_LEADER = ""
constants.DOC_HEADER = "Documented commands (type help <command>):"
constants.MISC_HEADER = "Miscellaneous help topics:"
constants.UNDOC_HEADER = "Undocumented commands:"
constants.NOHELP = "*** No help on %s"
constants.RULER = '='
# ------------------------------------------------------------------------####

# ---Application switches-------------------------------------------------####
constants.ENABLE_TEST_MODE = True
constants.ENABLE_COMPRESSION = False
# ------------------------------------------------------------------------####

if __name__ == "__main__":
    print dir(constants)