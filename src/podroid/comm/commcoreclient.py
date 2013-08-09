'''
Created on Jul 21, 2013

Twisted network client core.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.1

# install_twisted_rector must be called before importing the reactor
from kivy.support import install_twisted_reactor
install_twisted_reactor()

from kivy.logger import Logger
import base64
# connection to command server
from twisted.internet import protocol


class CommCoreClient(protocol.Protocol):

    """
    Communications core client protocol code.
    """

    _peer_host = None
    _peer_port = None
    _peer_repr = None

    def connectionMade(self):
        "Run when connection is established with server."

        self._peer_host = self.transport.getPeer().host
        self._peer_port = self.transport.getPeer().port
        self._peer_repr = self._peer_host + " on " + str(self._peer_port)

        Logger.debug(
            "Connection success! Connected to {}".format(self._peer_repr))

        self.factory.app.on_server_connection(self.transport)

    def connectionLost(self, reason):
        "Run when connection is lost with server."

        Logger.warn("Lost connection with peer {}".format(self._peer_repr))

        self.factory.app.on_server_disconnection(self.transport)

    def dataReceived(self, data):
        "Run when response is recieved from server."

        response = self.factory.app.handle_response(data)

        if response:
            print response

        Logger.debug("Recieved : {}".format(base64.b64encode(data)))


class CommCoreClientFactory(protocol.ReconnectingClientFactory):

    protocol = CommCoreClient

    def __init__(self, app):

        self.app = app

    def startedConnecting(self, connector):
        "Run when initiaition of connection takes place."

        Logger.debug("Attempting connection...")

    def buildProtocol(self, addr):
        "Build protocol on successful connection."

        Logger.debug("Connected.")
        Logger.debug("Resetting reconnection delay.")

        # Reset the delay on connection success
        self.resetDelay()

        # Overridden build protocol
        client_protocol = self.protocol()
        client_protocol.factory = self

        return client_protocol

    def clientConnectionLost(self, connector, reason):
        "Run when connection with server is lost."

        #self.app.print_message("connection lost")
        Logger.debug("Lost connection")

        return protocol.ReconnectingClientFactory.clientConnectionLost(
            self, connector, reason
        )

    def clientConnectionFailed(self, connector, reason):
        "Run when attempt to connect with server fails."

        #self.app.print_message("connection failed")
        Logger.debug("Connection failed. ")

        return protocol.ReconnectingClientFactory.clientConnectionFailed(
            self, connector, reason
        )
