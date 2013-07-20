from commcoreserver import CommCoreServerFactory
from commcoreclient import CommCoreClientFactory
from twisted.internet import reactor

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

class PodDroidApp(App):
    connection = None

    def build(self):
        ## Start GUI
        root = self.setup_gui()
        ## Start Server
        self.start_server()      
        return root

    def start_server(self):
        reactor.listenTCP(8000, CommCoreServerFactory(self))
        
    def setup_gui(self):
        self.textbox = TextInput(size_hint_y=.1, multiline=False)
        self.textbox.bind(on_text_validate=self.process_command)
        self.label = Label(text='connecting...\n')
        self.layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.textbox)
        return self.layout

    def connect_to_server(self):
        reactor.connectTCP('localhost', 8000, CommCoreClientFactory(self))

    def on_connection(self, connection):
        self.print_message("connected succesfully!")
        self.connection = connection

    def send_message(self, *args):
        msg = self.textbox.text
        if msg and self.connection:
            self.connection.write(str(self.textbox.text))
            self.textbox.text = ""

    def print_message(self, msg):
        self.label.text += msg + "\n"

    def process_command(self, *args):
        cmd = self.textbox.text
        self.print_message("Processing: %s" % cmd)
        
    def handle_command(self, msg):
        self.label.text  += "received:  %s\n" % msg

        if msg == "ping":  msg =  "pong"
        if msg == "plop":  msg = "kivy rocks"
        self.label.text += "processing: %s\n" % msg
        return msg

if __name__ == '__main__':
    PodDroidApp().run()
