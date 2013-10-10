'''
Created on Oct 10, 2013

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.2

from cryptikchaos.config.configuration import *

class CapsuleError(Exception):
    pass

class CapsuleOverflowError(CapsuleError):
    """
    If capsule unpack fails.
    """
    
    def __init__(self):
        
        pass

    def __str__(self):
        
        return "Capsule chunk should be equal to {} Bytes".format(constants.CAPSULE_SIZE)

if __name__ == "__main__":
    
    raise CapsuleUnpackError()