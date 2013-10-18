'''
Created on Jul 21, 2013

Twisted network server core. TODO

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.3

# install_twisted_rector must be called before importing 
# and using the reactor
from kivy.support import install_twisted_reactor
install_twisted_reactor()

from kivy.logger import Logger

from twisted.internet import protocol
from twisted.protocols.basic import LineReceiver


class CommCoreServerProtocol(LineReceiver):

    "Server backend to pocess the commands"

    def __init__(self):

        self._peer_host = None
        self._peer_port = None
        self._peer_repr = None

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

        response = self.factory.app.handle_recieved_data(line, self.transport)

        if response:
            self.sendLine(response)


class CommCoreServerFactory(protocol.Factory):

    protocol = CommCoreServerProtocol

    def __init__(self, app):

        self.app = app
