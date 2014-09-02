'''
Created on Jul 21, 2013

Twisted network client core.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6.1"

from kivy.logger import Logger
from base64 import b64encode

# connection to command server
from twisted.internet import protocol
from twisted.protocols.basic import LineReceiver

from cryptikchaos.core.env.configuration import constants


class CommCoreClientProtocol(LineReceiver):

    """
    Communications core client protocol code.
    """

    def __init__(self, factory):

        self._peer_host = None
        self._peer_port = None
        self._peer_repr = None
        self.factory = factory

        # Delimiter for sending line
        self.delimiter = constants.STREAM_LINE_DELIMITER

    def connectionMade(self):
        "Run when connection is established with server."
        # maintain the TCP connection
        self.transport.setTcpKeepAlive(True)
        # allow Nagle algorithm
        self.transport.setTcpNoDelay(False)

        self._peer_host = self.transport.getPeer().host
        self._peer_port = self.transport.getPeer().port
        self._peer_repr = self._peer_host + " on " + str(self._peer_port)

        Logger.debug(
            "CLIENT: Connection success! Connected to {}".format(self._peer_repr))

        self.factory.app.on_server_connection(self.transport)

    def connectionLost(self, reason):
        "Run when connection is lost with server."

        Logger.warn("CLIENT: Lost connection with peer {}".format(
            self._peer_repr
            )
        )

        self.factory.app._print(
            "Lost connection with peer {}".format(self._peer_repr)
        )

        self.factory.app.on_server_disconnection(self.transport)

    def lineReceived(self, line):
        "Run when response is received from server."

        Logger.debug(
            "CLIENT: received : {}, Data Length: {}".format(
                b64encode(line), len(line)
            )
        )

        response = self.factory.app.handle_response_stream(
            line, self.transport)

        if response:
            print response

    def lineLengthExceeded(self, line):
        "Run when line length is exceeded."

        Logger.error("CLIENT: received line is more than {}".format(self.MAX_LENGTH))


class CommCoreClientFactory(protocol.Factory):

    protocol = CommCoreClientProtocol

    def __init__(self, app):

        self.app = app

    def startedConnecting(self, connector):
        "Run when initiaition of connection takes place."

        Logger.debug("CLIENT: Attempting connection...")

    def buildProtocol(self, addr):
        "Build protocol on successful connection."

        Logger.debug("CLIENT: Connected.")

        return self.protocol(self)

    def clientConnectionLost(self, connector, reason):
        "Run when connection with server is lost."

        Logger.debug("CLIENT: Lost connection: {}".format(reason.getErrorMessage()))

    def clientConnectionFailed(self, connector, reason):
        "Run when attempt to connect with server fails."

        Logger.debug("CLIENT: Connection failed. {}".format(reason.getErrorMessage()))
