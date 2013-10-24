'''
Created on Oct 10, 2013

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.3

from cryptikchaos.config.configuration import *

class CapsuleError(Exception):
    pass

class CapsuleOverflowError(CapsuleError):
    """
    If capsule unpack fails.
    """

    def __init__(self, limit=None):
        
        # Size limit
        if limit:
            self.limit = constants.CAPSULE_SIZE
        else:
            self.limit = limit
            
        # Error message
        self.msg = "Exceeded limit of {} Bytes".format(
            self.limit
        )

    def __str__(self):

        return self.msg
    
class CapsuleEmptyError(CapsuleError):
    """
    If capsule is empty.
    """

    def __init__(self):

        pass

    def __str__(self):

        return "Capsule not populated with data."
    

if __name__ == "__main__":

    raise CapsuleOverflowError()