# install_twisted_rector must be called before importing  and using the reactor
from kivy.support import install_twisted_reactor
install_twisted_reactor()

from twisted.internet import protocol

## Server backend to pocess the commands
class CommCoreServer(protocol.Protocol):
    def dataReceived(self, data):
        response = self.factory.app.handle_command(data)
        if response:
            self.transport.write(response)

class CommCoreServerFactory(protocol.Factory):
    protocol = CommCoreServer

    def __init__(self, app):
        self.app = app


