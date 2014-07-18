'''
Created on Jul 5, 2014

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"

import re
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

from cryptikchaos.env.configuration import constants


class ConsoleInput(TextInput):
    "Console text input class."
    
    def __init__(self, font_type, font_size, handleinput_cmd_hook, 
            getcommands_cmd_hook, goto_consolescreen,size_y=1):

        # Init super
        super(ConsoleInput, self).__init__()
        
        # Single line input, enter triggers
        # on_text_validate
        self.multiline=True
        # Not password input
        self.password=False
        # Font type
        self.font_name = font_type
        # Font size
        self.font_size = font_size
        # Set size
        self.size_hint_y=size_y
        # Sets focus active
        self.focus = False            
        # Set background color
        self.background_color = [1, 1, 1, 1]
        # Set text color
        self.foreground_color = [0, 0, 0, 1]
        # Set padding for text input
        if not constants.PLATFORM_ANDROID:            
            self.padding = [25, 20, 10, 0]
        
        # Input command handler
        self.handleinput_cmd_hook = handleinput_cmd_hook
        # Get list of defined commands
        self.getcommands_cmd_hook = getcommands_cmd_hook
        # Go to console screen
        self.goto_consolescreen = goto_consolescreen
        
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
        
    def focus_input_box(self):
        
        self.focus = True
        
    def unfocus_input_box(self):
        
        self.focus = False
        
    def _pass(self): pass
        
    def on_enter(self, instance):
        "Called on text input entry."
        
        # Clear help displayed flag
        self.help_displayed_flag = False
        
        # Clear command buffer
        self.autocomplete_buffer = set()
        
        # Get data input
        input_text = self._get_input_text(instance)
        
        # Set focus
        Clock.schedule_once(lambda dt: self._pass, 1)
        if not constants.ENABLE_INPUT_SCREEN:
            self.focus_input_box()
        else:
            self.unfocus_input_box()

        # Handle input
        if input_text:
            # Reset prompt
            self._reset_prompt(instance)
            # Handle the input
            self.handleinput_cmd_hook(input_text)
            # Got to console screen
            self.goto_consolescreen()
        
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
            
    def insert_text(self, substring, from_undo=False):
        "Method hook called on character input."
        
        # On entry of command
        if substring == "\n":
            return self.on_enter(self)
        
        return super(ConsoleInput, self).insert_text(substring, from_undo=from_undo)