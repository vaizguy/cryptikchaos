'''
Created on Oct 15, 2013

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.2

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView

from cryptikchaos.config.configuration import *


class ConsoleWindow(GridLayout):
    
    def __init__(self, handle_input):
        # Init super
        super(ConsoleWindow, self).__init__()
        
        # Number of cols
        self.cols = 1
        
        self.label = Label(
            text=constants.GUI_WELCOME_MSG, 
            size_hint_y=0.9
        )
        
        # Scroll view label
        scroll_view = ScrollView()
        scroll_view.add_widget(self.label)
        
        self.add_widget(scroll_view)
        
        # Input text box
        self.console_input = TextInput(password=False, multiline=False, size_hint_y=0.1)
        self.console_input.focus = True
        self.console_input.bind(on_text_validate=handle_input)
        
        self.add_widget(self.console_input)
        
    def append_text_to_console(self, text):
        self.label.text += '\n' + text

class ConsoleWindowTest(App):

    def build(self):
        self.root = ConsoleWindow(self.handle_input)
        return self.root
    
    def handle_input(self, textbox):
        print "Input", textbox.text
        self.root.append_text_to_console("Success")
            
if __name__ == '__main__': 
                     
    ConsoleWindowTest().run()