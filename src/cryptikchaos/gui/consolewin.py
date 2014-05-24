'''
Created on Oct 15, 2013

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView

from cryptikchaos.env.configuration import constants

import re


class ConsoleInput(TextInput):
    "Console text input class."
    
    def __init__(self, font_type, font_size, handleinput_cmd_hook, getcommands_cmd_hook):

        # Init super
        super(ConsoleInput, self).__init__()
        
        # Single line input, enter triggers
        # on_text_validate
        self.multiline=False
        # Not password input
        self.password=False
        # Font type
        self.font_name = font_type
        # Font size
        self.font_size = font_size
        # Set size
        self.size_hint_y=0.1
        # Sets focus active
        self.focus = True
        # Set background color
        self.background_color = [0, 0, 0, 0]
        # Set text color
        self.foreground_color = [1, 1, 1, 1]
        # Set padding for text input
        if not constants.ENABLE_ANDROID_MODE:            
            self.padding = [25, 20, 10, 0]
        
        # Input command handler
        self.handleinput_cmd_hook = handleinput_cmd_hook
        # Get list of defined commands
        self.getcommands_cmd_hook = getcommands_cmd_hook
        
        # Prompt length
        self.prompt_len = len(constants.GUI_LABEL_PROMPT_SYM)
        
        # Command buffer
        self.command_buffer = ''
        self.autocomplete_buffer = set()
        self.help_displayed_flag = False
        
        # Bind to function on entry
        self.bind(on_text_validate=self.on_enter)
        
        # Finally add prompt
        self._reset_prompt(self)
        
    def _filter_prompt(self, text):
        "Remove prompt symbol from text."
        
        if constants.GUI_LABEL_PROMPT_SYM in text: 
            # If prompt in text
            return text[self.prompt_len:]
        else:
            return text
    
    def _get_input_text(self, instance):
        "Used to get console input text."
                
        return self._filter_prompt(instance.text)

    def _add_text(self, instance, text=None):
        "Used to access instance.text."
        
        # Change text
        if text:
            instance.text = "{}{}".format(
                constants.GUI_LABEL_PROMPT_SYM, 
                text
            )
        else:
            instance.text = "{}".format(constants.GUI_LABEL_PROMPT_SYM)
    
    def _reset_prompt(self, instance):
        "Reset the prompt to default."
        
        # Clear input text in input box
        self._add_text(instance)
        
        # Reset cursor
        instance.do_cursor_movement("cursor_end")
        
    def on_enter(self, instance):
        "Called on text input entry."
        
        # Clear help displayed flag
        self.help_displayed_flag = False
        
        # Clear command buffer
        self.autocomplete_buffer = set()
        
        # Get data input
        input_text = self._get_input_text(instance)
        
        # Handle input
        if input_text:
            # Reset prompt
            self._reset_prompt(instance)
            # Handle the input
            self.handleinput_cmd_hook(input_text)
            
        # Set focus
        self.focus = True ## TODO not working.
        
    def on_tab(self, instance, pcmd):
        "Method hook for entry of [TAB]"
              
        if not self.help_displayed_flag:
            # Display help
            self.handleinput_cmd_hook("help")
            
            # Set help displayed flag
            self.help_displayed_flag = True
        
        # Reset prompt 
        self._reset_prompt(instance)
        
        # Available list of Commands
        command_list = [c[4:] for c in self.getcommands_cmd_hook()]
        
        # Get commands with pcmd matches
        pcmd_matches = [c for c in command_list if re.match(r'\s*{}'.format(pcmd), c) \
                                            and c not in self.autocomplete_buffer]
        
        # Sort cmd list alphabetically
        pcmd_matches = sorted(pcmd_matches)
               
        # Reset autocomplete buffer
        if (self.autocomplete_buffer == set(command_list)):
            self.autocomplete_buffer = set()
               
        # command completion
        if pcmd_matches:
            # first match for now ## TODO
            fcmd = pcmd_matches.pop()
            # Send to command buffer
            self.autocomplete_buffer.add(fcmd)
            # Change text
            self._add_text(instance, fcmd)
            # move cursor to end
            instance.do_cursor_movement("cursor_end")
            
    def on_text(self, instance, value):
        "Method hook called on change of TextInput.text value."
        
        # Prompt is readonly
        if (
            len(value) <= self.prompt_len or \
            constants.GUI_LABEL_PROMPT_SYM not in value[:self.prompt_len]
           ):
            # Reset prompt
            self._reset_prompt(instance)
              
        # Partial comm
        pcmd = self._filter_prompt(value).rstrip('\t')
                
        # If TAB is entered
        if 9 in [ord(c) for c in value]:
            self.on_tab(instance, pcmd)
            

class ConsoleWindow(GridLayout):
    "Console window class."
    
    def __init__(self, handleinput_cmd_hook, getcommands_cmd_hook,
        greeting, font_type, font_size):
        
        # Init super
        super(ConsoleWindow, self).__init__()
        
        # Number of cols
        self.cols = 1
        
        if not constants.ENABLE_ANDROID_MODE:
            # Height and width
            self.height = 400
            self.width = 800
        
        # Create viewing area
        self.view_area = GridLayout(cols = 1, size_hint = (1, None))
        
        # Create label for console output
        self.label = Label(
            size_hint=(1, None),
            markup=True,
            font_name=font_type,
            font_size=font_size,
            valign='top',
            halign='left',    
        )
        
        if not constants.ENABLE_ANDROID_MODE:
            self.label.text_size=(self.width-50, None)
            self.label.shorten=True,

        # bind label to scrollable size
        self.label.bind(texture_size=self.label.setter('size'))
                
        # Add label to viewing area      
        self.view_area.add_widget(self.label)
                               
        # Scroll view label
        self.scroll_view = ScrollView(
            size_hint_y=0.9,
        )
        
        if not constants.ENABLE_ANDROID_MODE:
            self.scroll_view.size=(self.height, self.width)
        
        # TODO X-axis scroll not working
        self.scroll_view.do_scroll_y = True
        self.scroll_view.do_scroll_x = True
        # Add label to scroll view
        self.scroll_view.add_widget(self.view_area)
        
        # Bind text size to view area
        self.view_area.bind(minimum_height = self.view_area.setter('height'))
                
        self.add_widget(self.scroll_view)
        
        # Input text box
        self.console_input = ConsoleInput(
            # Font type
            font_type=font_type,
            # Font size
            font_size=font_size,
            # Input handler hook
            handleinput_cmd_hook=handleinput_cmd_hook, 
            # CMD list hook
            getcommands_cmd_hook=getcommands_cmd_hook
        )
        
        # Internal function-hook alias
        self.display_text = self.inputtext_gui_hook
        
        self.add_widget(self.console_input)
        
        # Display welcome message
        self.display_text(text=greeting)
        
    ## GUI Hooks-----------------------
    def inputtext_gui_hook(self, text):
        
        self.label.text += "[color={}]{}[/color]".format(
            constants.GUI_FONT_COLOR,
            text
        )
        
    def getmaxwidth_gui_hook(self):
        
        return self.width
    ##---------------------------------
        
    def on_resize(self, instance, width, height):
        
        # New height and width
        instance.width = width
        instance.height = height

            
if __name__ == '__main__': 
    
    from kivy.resources import resource_add_path
    from kivy.core.window import Window 
    
    class ConsoleWindowTest(App):

        def build(self):
                    
            # Build ConsoleWindow
            root = ConsoleWindow(
                # Input handler hook
                handleinput_cmd_hook=self.handle_input_hook,
                # Get command list hook
                getcommands_cmd_hook=lambda: [],
                # Console splash greeting
                greeting="Testing Window!",
                # Font type face
                font_type=constants.GUI_FONT_TYPE,
                # Font size
                font_size=14
            ) ## TODO messy implementation
            
            # Window resize hook
            Window.bind(on_resize=self.resize)
           
            return root
        
        def handle_input_hook(self, text):
            
            print "Input", text
            
        def resize(self, instance, height, width):
            
            print "New heightxwidth {}x{}".format(height, width)
    
    # Add resource path
    resource_add_path(constants.KIVY_RESOURCE_PATH_1)

    ConsoleWindowTest().run()