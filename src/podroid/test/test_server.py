# install_twisted_rector must be called before importing  and using the reactor
from kivy.support import install_twisted_reactor
from kivy import Logger

install_twisted_reactor()

from twisted.internet import reactor
from twisted.internet import protocol

from base64 import b64encode

## Add podroid path
import pythonpath
pythonpath.AddSysPath('../../')

from podroid.config.configuration import *
from podroid.comm.twiscomm import CommService

class PodroidTestProtocol(protocol.Protocol):

    def dataReceived(self, data):

        response = self.factory.app.handle_recieved_data(data)

        if response:
            self.transport.write(response)


class PodroidTestFactory(protocol.Factory):

    protocol = PodroidTestProtocol

    def __init__(self, app):

        self.app = app


from kivy.app import App
from kivy.uix.label import Label

class TwistedServerApp(App, CommService):
           
    def build(self):
        
        ## Initiate Twisted Server
        CommService.__init__(self, 888, "localhost", 8888, clientinit=False, printer=self.print_message)
        
        ## Add local peer used for testing.
        self.add_peer(123, "localhost", 8000)
        
        self.label = Label(text="server started\n")
        
        return self.label
    
    def print_message(self, msg):
        
        self.label.text += msg + '\n'


if __name__ == '__main__':
    TwistedServerApp().run()
