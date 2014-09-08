'''
Created on Oct 6, 2013

This file is part of CryptikChaos.

CryptikChaos is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CryptikChaos is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CryptikChaos. If not, see <http://www.gnu.org/licenses/>.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6.1"

from cryptikchaos.core.env.configuration import constants

from kivy.logger import Logger

from twisted.internet import protocol
from twisted.protocols.basic import LineReceiver

from base64 import b64encode


class CommCoreAuthProtocol(LineReceiver):

    """
    Communications core authentication protocol code.
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

        self._peer_host = self.transport.getPeer().host
        self._peer_port = self.transport.getPeer().port
        self._peer_repr = self._peer_host + " on " + str(self._peer_port)

        Logger.debug(
            "AUTH: Attempting handshake with {}".format(self._peer_repr)
        )

        self.factory.app.on_server_auth_open(self.transport)

    def connectionLost(self, reason):
        "Run when connection is lost with server."

        Logger.warn(
            "AUTH: Peer Authentication connection terminated : {}".format(
                self._peer_repr)
        )

        self.factory.app.on_server_auth_close(self.transport)

    def lineReceived(self, line):
        "Run when response is recieved from server."

        Logger.debug("AUTH: Recieved : {}".format(b64encode(line)))

        dcon_rsp = self.factory.app.handle_auth_response_stream(
            line, self.transport)

        if dcon_rsp:
            self.sendLine(dcon_rsp)

    def lineLengthExceeded(self, line):
        "Run when line length is exceeded."

        Logger.error("AUTH: Recieved line is more than {}".format(self.MAX_LENGTH))


class CommCoreAuthFactory(protocol.Factory):

    protocol = CommCoreAuthProtocol

    def __init__(self, app):

        self.app = app

    def buildProtocol(self, addr):
        "Build protocol on successful connection."

        return self.protocol(self)

    def startedConnecting(self, connector):
        "Run when initiaition of connection takes place."

        Logger.debug("AUTH: Attempting auth...")

    def clientConnectionLost(self, connector, reason):
        "Run when attempt to connect with server fails."

        Logger.debug("AUTH: Connection lost. {}".format(reason.getErrorMessage()))

    def clientConnectionFailed(self, connector, reason):
        "Run when attempt to connect with server fails."

        Logger.debug("AUTH: Connection failed. {}".format(reason.getErrorMessage()))

        # Display error on app console
        self.app._print("{}".format(reason.getErrorMessage()))
