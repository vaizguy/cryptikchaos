from kivy.app import App
from kivy.uix.label import Label
from commcoreserver import CommCoreServerFactory

class TwistedServerApp(App):

    def build(self):
        self.label = Label(text="server started\n")
        reactor.listenTCP(8000, EchoFactory(self))
        return self.label

    def handle_command(self, msg):
        self.label.text  = "received:  %s\n" % msg

        if msg == "ping":  msg =  "pong"
        if msg == "plop":  msg = "kivy rocks"
        self.label.text += "processing: %s\n" % msg
        return msg


if __name__ == '__main__':
    TwistedServerApp().run()
