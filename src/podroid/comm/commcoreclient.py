#install_twisted_rector must be called before importing the reactor
from kivy.support import install_twisted_reactor
install_twisted_reactor()


# connection to command server
from twisted.internet import protocol


class CommCoreClient(protocol.Protocol):
    
    def connectionMade(self):
        print 'conn made'
        self.factory.app.on_server_connection(self.transport)

    def dataReceived(self, data):
        
        print(data)

class CommCoreClientFactory(protocol.ReconnectingClientFactory):
    
    protocol = CommCoreClient
    
    def __init__(self, app):
        self.app = app

    def clientConnectionLost(self, connector, reason):
        #self.app.print_message("connection lost")
        print 'Lost connection.  Reason:', reason
        protocol.ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        #self.app.print_message("connection failed")
        print 'Connection failed. Reason:', reason
        protocol.ReconnectingClientFactory.clientConnectionFailed(self, connector,  reason)
