'''
Created on Jul 21, 2013

Twisted network server core.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"

from cryptikchaos.core.env.configuration import constants

from kivy.logger import Logger
import base64

from twisted.internet import protocol
from twisted.protocols.basic import LineReceiver


class CommCoreServerProtocol(LineReceiver):

    "Server backend to pocess the commands"

    def __init__(self, factory):

        self._peer_host = None
        self._peer_port = None
        self._peer_repr = None
        self.factory = factory

        # Delimiter for sending line
        self.delimiter = constants.STREAM_LINE_DELIMITER

    def connectionMade(self):
        "Run when connection is established with server."

        self._peer_host = self.transport.getPeer().host
        self._peer_port = self.transport.getPeer().port
        self._peer_repr = self._peer_host + " on " + str(self._peer_port)

        Logger.debug(
            "Connection success! Connected to {}".format(self._peer_repr)
        )

        self.factory.app.on_client_connection(self.transport)

    def connectionLost(self, reason):
        "Run when connection is lost with server."

        Logger.warn(
            "Lost connection with peer {}".format(self._peer_repr)
        )

        self.factory.app.on_client_disconnection(self.transport)

    def lineReceived(self, line):
        "Run when response is received from client."

        Logger.debug(
            "SERVER: received : {}, Data Length: {}".format(
                base64.b64encode(line), len(line)
            )
        )

        response = self.factory.app.handle_request_stream(line, self.transport)

        if response:
            self.sendLine(response)

    def lineLengthExceeded(self, line):
        "Run when line length is exceeded."

        Logger.error("received line is more than {}".format(self.MAX_LENGTH))


class CommCoreServerFactory(protocol.Factory):

    protocol = CommCoreServerProtocol

    def __init__(self, app):

        self.app = app

    def buildProtocol(self, addr):
        "Build protocol on successful connection."

        Logger.debug("Connected.")

        return self.protocol(self)
