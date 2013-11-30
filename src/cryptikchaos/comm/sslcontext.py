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
    
    def __init__(self, crt, key, ca):
        "Initializing SSL context"
  
        self.crt = crt
        self.key = key
        self.ca = ca
    
    def getContext(self):
        "Get SSL context."
        
        # Selecting Transport Layer Security v1
        self.method = SSL.TLSv1_METHOD
        
        # Get the client context factory
        ctx = ssl.ClientContextFactory.getContext(self)
        
        # Load certificate
        try:
            ctx.use_certificate_file(self.crt)
            
        except SSL.Error as exception:
            Logger.error(exception.message[0][2])
            raise SSLCertReadError(self.crt)
            
        else:
            Logger.info("Loaded Peer SSL Certificate.")

        # Load private key  
        try:
            ctx.use_privatekey_file(self.key)
            
        except SSL.Error as exception:
            Logger.error(exception.message[0][2])
            raise SSLKeyReadError(self.key)
            
        else:
            Logger.info("Loaded Peer SSL key.")  
        
        # Set verify mode and verify callback chain.
        ctx.set_verify(
            SSL.VERIFY_PEER | SSL.VERIFY_FAIL_IF_NO_PEER_CERT, 
            self.verifyCallback
        )
        
        # Since we have self-signed certs we have to explicitly
        # tell the server to trust them.
        ctx.load_verify_locations(self.ca)
                         
        return ctx
    
    def verifyCallback(self, connection, x509, errno, depth, preverifyOK):
        
        if not preverifyOK:
            self.logger.debug("Certificate verification failed, {}".format(x509.get_subject()))
        else:
            # Add post verification callback here.
            pass
            
        return preverifyOK