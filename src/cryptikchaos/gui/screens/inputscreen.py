'''
Created on Jul 5, 2014

@author: vaizguy
'''

from kivy.uix.screenmanager import Screen
from cryptikchaos.gui.inputwin import ConsoleInput


class InputScreen(Screen):
    
    def __init__(self, font_type, font_size, handleinput_cmd_hook, getcommands_cmd_hook, goto_consolescreen, **kwargs):
        
        super(InputScreen, self).__init__(**kwargs)
        
        self.console_input = ConsoleInput( 
            font_type,
            font_size, 
            handleinput_cmd_hook, 
            getcommands_cmd_hook,
            goto_consolescreen
        )
        
        ## Add the console input 
        self.add_widget(self.console_input)
        
        ## Focus input box method
        self.focus_inputbox = self.console_input.focus_input_box
