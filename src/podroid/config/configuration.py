'''
Created on Aug 5, 2013

@author: vaizguy
'''
import uuid, hmac
import constants

####------------------CAPSULE CONSTANTS-----------------------------------------------------------------------------####

## Capsule Content Length 
constants.CAPS_CONTENT_LEN = 40
## Capsule Type length
constants.CAPS_TYPE_LEN = 4
## Capsule ID Length
constants.CAPS_ID_LEN = 8
## Capsule chksum length
constants.CAPS_CHKSUM_LEN = 32
## Capsule content length byte length
constants.CAPS_CONTENTL_LEN = 4
## Capsule IP integer repr length
constants.CAPS_DESTIP_LEN = 4
## Capsule size
constants.CAPSULE_SIZE = constants.CAPS_CONTENT_LEN + \
                         constants.CAPS_TYPE_LEN + \
                         constants.CAPS_ID_LEN + \
                         constants.CAPS_CHKSUM_LEN + \
                         constants.CAPS_CONTENTL_LEN + \
                         constants.CAPS_DESTIP_LEN
####-----------------------------------------------------------------------------------------------------------------####

####------------------TEST CONSTANTS---------------------------------------------------------------------------------####

## Test string message
constants.LOCAL_TEST_STR = "Hello World!"
## Test capsule type
constants.LOCAL_TEST_CAPS_TYPE = "TEST"
## Local Test IP
constants.LOCAL_TEST_HOST = "127.0.0.1"
## Local Test Port
constants.LOCAL_TEST_PORT = 8888
## Local Test PEer ID
constants.LOCAL_TEST_PEER_ID = 888
## Test ID
constants.LOCAL_TEST_CAPS_ID = str( uuid.uuid5(uuid.NAMESPACE_URL, constants.LOCAL_TEST_HOST) )[0:constants.CAPS_ID_LEN]
## Test chksum
constants.LOCAL_TEST_CAPS_CHKSUM = hmac.new(constants.LOCAL_TEST_STR).hexdigest()

####-----------------------------------------------------------------------------------------------------------------####