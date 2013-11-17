'''
Created on Nov 16, 2013

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.5

from twisted.internet import ssl
from OpenSSL import SSL
from kivy import Logger

from cryptikchaos.exceptions.sslcontextExceptions import \
    SSLCertReadError, SSLKeyReadError


class TLSCtxFactory(ssl.ClientContextFactory):
    "Twisted SSL Context Factory."
    
    def __init__(self, crt, key):
        "Initializing SSL context"
  
        self.crt = crt
        self.key = key
    
    def getContext(self):
        "Get SSL context."
        
        # Selecting Transport Layer Security v1
        self.method = SSL.TLSv1_METHOD
        
        # Get the client context factory
        ctx = ssl.ClientContextFactory.getContext(self)
        
        # Load certificate
        try:
            ctx.use_certificate_file(self.crt)
            
        except SSL.Error as e:
            Logger.error(e.message[0][2])
            raise SSLCertReadError()
            
        else:
            Logger.info("Loaded Peer SSL Certificate.")

        # Load private key  
        try:
            ctx.use_privatekey_file(self.key)
            
        except SSL.Error as e:
            Logger.error(e.message[0][2])
            raise SSLKeyReadError()
            
        else:
            Logger.info("Loaded Peer SSL key.")  
                                  
        return ctx