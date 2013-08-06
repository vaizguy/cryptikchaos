#install_twisted_rector must be called before importing the reactor
from kivy.support import install_twisted_reactor
install_twisted_reactor()

from kivy.logger import Logger
import base64
# connection to command server
from twisted.internet import protocol

class CommCoreClient(protocol.Protocol):
    
    def connectionMade(self):
        
        self.factory.app.on_server_connection(self.transport)

    def dataReceived(self, data):
        
        response = self.factory.app.handle_response(data)
        
        if response:
            print response
                     
        
        Logger.debug( "Recieved : {}".format(base64.b64encode(data)) )

class CommCoreClientFactory(protocol.ReconnectingClientFactory):
    
    protocol = CommCoreClient
    
    def __init__(self, app):
        
        self.app = app


    def startedConnecting(self, connector):
        
        Logger.debug( "Attempting connection..." )


    def buildProtocol(self, addr):
        
        Logger.debug ( "Connected." )
        Logger.debug ( "Resetting reconnection delay" )
        ## Reset the delay on connection success
        self.resetDelay()
        ## Overridden build protocol
        client_protocol = self.protocol()
        client_protocol.factory = self
        
        return client_protocol
    
    
    def clientConnectionLost(self, connector, reason):
        
        #self.app.print_message("connection lost")
        Logger.debug( "Lost connection.  Reason: {}".format(reason) )
        protocol.ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        
        #self.app.print_message("connection failed")
        Logger.debug( "Connection failed. Reason:".format(reason) )
        protocol.ReconnectingClientFactory.clientConnectionFailed(self, connector,  reason)

