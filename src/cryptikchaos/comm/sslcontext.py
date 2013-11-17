'''
Created on Nov 16, 2013

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.5

from twisted.internet import ssl
from OpenSSL import SSL
from kivy import Logger

from cryptikchaos.env.configuration import constants


class TLSCtxFactory(ssl.ClientContextFactory):
    
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
        
        # Alpha testing crt/key message
        missing_cert_key_exception_msg = """
            Missing SSL Certificate / Key
            -----------------------------
            
            Please generate a valid SSL certificate in
            {}/certs/{}.{}
            (OR) 
            Change configuration variable constants.ENABLE_TLS* to False.
            
            *TLS mode is still in experimental phase.
        """

        
        # Load certificate
        try:
            ctx.use_certificate_file(self.crt)
            
        except SSL.Error as e:
            Logger.error(e.message[0][2])
            raise Exception(
                missing_cert_key_exception_msg.format(
                    constants.PROJECT_PATH,
                    constants.PEER_ID,
                    "crt"
                )
            )
            
        else:
            Logger.info("Loaded Peer SSL Certificate.")

        # Load private key  
        try:
            ctx.use_privatekey_file(self.key)
            
        except SSL.Error as e:
            Logger.error(e.message[0][2])
            raise Exception(
                missing_cert_key_exception_msg.format(
                    constants.PROJECT_PATH,
                    constants.PEER_ID, 
                    "key"
                )
            )
            
        else:
            Logger.info("Loaded Peer SSL key.")  
                                  
        return ctx