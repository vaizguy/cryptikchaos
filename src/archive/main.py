from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty


class DroidChatBox(BoxLayout):

    input_box = ObjectProperty()
    output_box = ObjectProperty()

    def read_command(self):
        self.output_box.text += self.input_box.text + '\n'

class DroidChat(App):

    def build(self):
        return DroidChatBox()

DroidChat().run()
