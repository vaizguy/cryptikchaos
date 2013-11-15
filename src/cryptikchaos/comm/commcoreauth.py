'''
Created on Oct 6, 2013

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.5

# install_twisted_rector must be called before importing the reactor
from kivy.support import install_twisted_reactor
install_twisted_reactor()

from cryptikchaos.env.configuration import constants

from kivy.logger import Logger

from twisted.internet import protocol
from twisted.protocols.basic import LineReceiver

import base64


class CommCoreAuthProtocol(LineReceiver):

    """
    Communications core authentication protocol code.
    """

    def __init__(self, factory):

        self._peer_host = None
        self._peer_port = None
        self._peer_repr = None
        self.factory    = factory
        
        # Delimiter for sending line
        self.delimiter = constants.STREAM_LINE_DELIMITER

    def connectionMade(self):
        "Run when connection is established with server."

        self._peer_host = self.transport.getPeer().host
        self._peer_port = self.transport.getPeer().port
        self._peer_repr = self._peer_host + " on " + str(self._peer_port)

        Logger.debug(
            "Attempting handshake with {}".format(self._peer_repr)
        )
                
        self.factory.app.on_server_authentication(self.transport)

    def connectionLost(self, reason):
        "Run when connection is lost with server."

        Logger.warn(
            "Peer Authentication connection terminated : {}".format(self._peer_repr)
        )

        self.factory.app.on_server_auth_close(self.transport)

    def lineReceived(self, line):
        "Run when response is recieved from server."

        Logger.debug("AUTH: Recieved : {}".format(base64.b64encode(line)))
        
        if self.factory.app.handle_auth_response(line, self.transport):
            self.transport.abortConnection()
                
    def lineLengthExceeded(self, line):
        "Run when line length is exceeded."
        
        Logger.error("Recieved line is more than {}".format(self.MAX_LENGTH))

class CommCoreAuthFactory(protocol.Factory):

    protocol = CommCoreAuthProtocol

    def __init__(self, app):

        self.app = app

    def buildProtocol(self, addr):
        "Build protocol on successful connection."

        return self.protocol(self)

    def startedConnecting(self, connector):
        "Run when initiaition of connection takes place."

        Logger.debug("Attempting auth...")

    def clientConnectionLost(self, connector, reason):
        "Run when attempt to connect with server fails."

        Logger.debug("Connection lost. {}".format(reason.getErrorMessage()))

    def clientConnectionFailed(self, connector, reason):
        "Run when attempt to connect with server fails."

        Logger.debug("Connection failed. {}".format(reason.getErrorMessage()))
        
        # Display error on app console
        self.app._print("{}".format(reason.getErrorMessage()))


