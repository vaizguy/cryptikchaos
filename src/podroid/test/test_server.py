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

from podroid.comm.capsule.capsule import Capsule

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

class TwistedServerApp(App):

    def build(self):

        self.label = Label(text="server started\n")
        reactor.listenTCP(8888, PodroidTestFactory(self))
        return self.label

    def handle_recieved_data(self, serial):
        
        Logger.debug( "Handling {}".format(b64encode(serial)) )
        
        ## Response
        rsp = serial
        
        ## Unpack capsule
        c_rx = Capsule()
        c_rx.unpack(serial)
        c_rx_type = c_rx.gettype()

        self.label.text  = "received:  %s\n" % str(c_rx)

        if c_rx_type == "PING":
            rsp =  "PONG" ## Legacy
            
        elif c_rx_type == "TEST":
            pass ## Resend the same msg.
        
        elif c_rx_type == "BULK":  ## TODO ## NOT WORKNG
            dip = c_rx.getip()
            c_tx = Capsule(captype="MACK", content='', dest_host=dip)
            rsp = c_tx.pack()
            
        self.label.text += "responded: %s\n" % rsp

        return rsp


if __name__ == '__main__':
    TwistedServerApp().run()
