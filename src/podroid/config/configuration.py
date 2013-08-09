'''
Created on Aug 5, 2013

Contains all unchangable constants used accross application.
Must be changed with care.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.1

import uuid
import hmac
import os

import constants

# ------------------GUI Attribute CONSTANTS-------------------------------####
constants.GUI_WELCOME_MSG = """
  P0DN3T v.1
  ---------------
"""
constants.GUI_LABEL_PROMPT_SYM = ">>"
constants.GUI_LABEL_LEFT_PADDING = "  "
constants.GUI_LABEL_PROMPT = constants.GUI_LABEL_LEFT_PADDING + \
    constants.GUI_LABEL_PROMPT_SYM

# ------------------------------------------------------------------------####

# ------------------Project Path CONSTANTS--------------------------------####
constants.PROJECT_PATH = os.path.dirname(os.path.realpath(__file__)) + "/.."
# ------------------------------------------------------------------------####

# ------------------Protocol Capsule type CONSTANTS-----------------------####
constants.PROTO_BULK_TYPE = "BULK"
constants.PROTO_MACK_TYPE = "MACK"
# ------------------------------------------------------------------------####

# ------------------CAPSULE CONSTANTS-------------------------------------####

# Capsule Content Length
constants.CAPS_CONTENT_LEN = 40
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

# Capsule size
constants.CAPSULE_SIZE = constants.CAPS_CONTENT_LEN + \
    constants.CAPS_TYPE_LEN + \
    constants.CAPS_ID_LEN + \
    constants.CAPS_CHKSUM_LEN + \
    constants.CAPS_CONTENTL_LEN + \
    constants.CAPS_DST_IP_LEN + \
    constants.CAPS_SCR_IP_LEN
# ------------------------------------------------------------------------####

# ------------------TEST CONSTANTS----------------------------------------####

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
# Test ID
constants.LOCAL_TEST_CAPS_ID = str(
    uuid.uuid5(uuid.NAMESPACE_URL,
               constants.LOCAL_TEST_HOST))[0:constants.CAPS_ID_LEN]
# Test chksum
constants.LOCAL_TEST_CAPS_CHKSUM = hmac.new(
    constants.LOCAL_TEST_STR).hexdigest()

# ------------------------------------------------------------------------####

# ---Help documentation printer constants---------------------------------####
constants.DOC_LEADER = ""
constants.DOC_HEADER = "Documented commands (type help <topic>):"
constants.MISC_HEADER = "Miscellaneous help topics:"
constants.UNDOC_HEADER = "Undocumented commands:"
constants.NOHELP = "*** No help on %s"
constants.RULER = '='
# ------------------------------------------------------------------------####
