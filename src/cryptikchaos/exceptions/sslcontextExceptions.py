'''
Created on Nov 17, 2013

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.5

from cryptikchaos.env.configuration import constants


class SSLContextError(Exception):
    pass


class SSLCertReadError(SSLContextError):
    
    def __init__(self):
        
        self.msg = """
            Missing SSL Certificate / Key
            -----------------------------
            
            Please generate a valid SSL certificate in
            {}/certs/{}.crt
            (OR) 
            Change configuration variable constants.ENABLE_TLS* to False.
            
            *TLS mode is still in experimental phase.
        """.format(constants.PROJECT_PATH, constants.PEER_ID)
        
    def __str__(self):
        
        return self.msg
        
class SSLKeyReadError(SSLContextError):
    
    def __init__(self):
        
        self.msg = """
            Missing SSL Certificate / Key
            -----------------------------
            
            Please generate a valid SSL certificate in
            {}/certs/{}.key
            (OR) 
            Change configuration variable constants.ENABLE_TLS* to False.
            
            *TLS mode is still in experimental phase.
        """.format(constants.PROJECT_PATH, constants.PEER_ID)
        
    def __str__(self):
        
        return self.msg        
