'''
Created on Nov 17, 2013

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"


class SSLContextError(Exception):
    pass


class SSLCertReadError(SSLContextError):

    def __init__(self, path):

        self.msg = """
            Missing SSL Certificate / Key
            -----------------------------

            Please place a valid SSL certificate in
            {}
            (OR)
            Change configuration variable constants.ENABLE_TLS* to False.

            *TLS mode is still in experimental phase.
        """.format(path)

    def __str__(self):

        return self.msg


class SSLKeyReadError(SSLContextError):

    def __init__(self, path):

        self.msg = """
            Missing SSL Certificate / Key
            -----------------------------

            Please generate a valid SSL certificate in
            {}
            (OR)
            Change configuration variable constants.ENABLE_TLS* to False.

            *TLS mode is still in experimental phase.
        """.format(path)

    def __str__(self):

        return self.msg
