'''
Created on Jul 5, 2014

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"

from kivy.uix.screenmanager import Screen
from cryptikchaos.gui.inputwin import ConsoleInput


class InputScreen(Screen):
    
    def __init__(self, font_type, font_size, handleinput_cmd_hook, 
            getcommands_cmd_hook, goto_consolescreen, **kwargs):
        
        ## Construct screen
        super(InputScreen, self).__init__(**kwargs)
        
        ## Console input
        self.console_input = ConsoleInput( 
            font_type,
            font_size, 
            handleinput_cmd_hook, 
            getcommands_cmd_hook,
            goto_consolescreen
        )
        
        ## Add the console input 
        self.add_widget(self.console_input)