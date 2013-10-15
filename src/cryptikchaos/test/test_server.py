'''
Test Sever used to test the server side protocol.
To Run:
python test_server.py

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.2

# install_twisted_rector must be called before importing  and using the reactor
from kivy.support import install_twisted_reactor

install_twisted_reactor()

from twisted.internet import protocol

# Add cryptikchaos path
import pythonpath
pythonpath.AddSysPath('../../')

from cryptikchaos.config.configuration import *
from cryptikchaos.comm.twiscomm import CommService


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

        # Initiate Twisted Server
        CommService.__init__(
            self,
            peerid=constants.LOCAL_TEST_PEER_ID,
            peerkey=constants.LOCAL_TEST_SERVER_KEY,
            host=constants.LOCAL_TEST_HOST,
            port=constants.LOCAL_TEST_PORT,
            clientinit=False,
            printer=self.print_message)
        
        self.label = Label(text="Server started\n")

        return self.label

    def print_message(self, msg):

        self.label.text += msg + '\n'


if __name__ == '__main__':
    TwistedServerApp().run()
