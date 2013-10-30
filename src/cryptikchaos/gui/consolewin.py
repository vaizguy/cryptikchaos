'''
Created on Oct 15, 2013

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.4

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView

import re


class ConsoleInput(TextInput):
    "Console text input class"
    
    def __init__(self, handle_input_hook, get_cmd_hook):

        # Init super
        super(ConsoleInput, self).__init__()
        
        # Single line input, enter triggers
        # on_text_validate
        self.multiline=False
        # Not password input
        self.password=False
        # Set size
        self.size_hint_y=0.1
        # Sets focus active
        self.focus = True
        
        # Input command handler
        self.handle_input = handle_input_hook
        # Get list of defined commands
        self.get_commands = get_cmd_hook
        
        # Bind to function on entry
        self.bind(on_text_validate=self.new_input)
        
    def new_input(self, instance):
        "Called on text input entry"
        
        # Get data input
        input_text = instance.text
        
        # Handle input
        if input_text:
            # Clear text in input box
            instance.text = ""         
            # Handle the input
            self.handle_input(input_text)
            
        # Set focu
        self.focus = True ## TODO not working.
        
    def on_text(self, instance, value):
        "Method hook called on change of TextInput.text value"   

        # Partial comm
        pcmd = value.rstrip('\t')
        # List of commands
        cmd_list =  [c[4:] for c in self.get_commands()]
        # Get commands with pcmd matches
        pcmd_matches = [c for c in cmd_list if re.match(r'^{}'.format(pcmd), c)]

        # command completion
        if '\t' in value and pcmd_matches:
            # first match for now ## TODO
            fcmd = pcmd_matches.pop()
            # Change text
            instance.text = fcmd
            # position difference
            diff = len(fcmd) - len(pcmd)
            # get current position
            (x, y) = self.cursor
            # Shift cursor
            self.cursor = (x+diff, y)
            # move cursor to end
            self.do_cursor_movement("cursor_end")


class ConsoleWindow(GridLayout):
    "Console window class."
    
    def __init__(self, handle_input_hook, get_cmd_hook, greeting, 
        font_type, font_size):
        
        # Init super
        super(ConsoleWindow, self).__init__()
        
        # Number of cols
        self.cols = 1
        
        self.label = Label(
            text=greeting,
            size_hint_y=None,
            height=100,
            halign='left',
            markup=True,
            font_name=font_type,
            font_size=font_size,
            text_size=(750, None),
            shorten=True,
            valign='top'
        )
                        
        # bind label to scrollable size
        self.label.bind(texture_size=self.label.setter('size'))
                       
        # Scroll view label
        scroll_view = ScrollView(
            size_hint_y=0.9, 
        )
        # TODO X-axis scroll not working
        scroll_view.do_scroll_y = True
        scroll_view.do_scroll_x = True
        # Add label to scroll view
        scroll_view.add_widget(self.label)
        
        self.add_widget(scroll_view)
        
        # Input text box
        self.console_input = ConsoleInput(
            # Input handler hook
            handle_input_hook=handle_input_hook, 
            # CMD list hook
            get_cmd_hook=get_cmd_hook
        )
        
        self.add_widget(self.console_input)
        
    def append_text_to_console(self, text):
        
        self.label.text += text


class ConsoleWindowTest(App):

    def build(self):
                
        # Build ConsoleWindow
        root = ConsoleWindow(
            # Input handler hook
            handle_input_hook=self.handle_input_hook,
            # Get command list hook
            get_cmd_hook=lambda: None,
            # Console splash greeting
            greeting="Testing Window!",
            # Font type face
            font_type=constants.GUI_FONT_TYPE,
            # Font size
            font_size=constants.GUI_FONT_SIZE
        ) ## TODO messy implementation
        
        return root
    
    def handle_input_hook(self, textbox):
        
        print "Input", textbox.text
        textbox.text = ""
        textbox.focus = True
        self.root.append_text_to_console("\nInput Success\n")
            
if __name__ == '__main__': 
                     
    ConsoleWindowTest().run()