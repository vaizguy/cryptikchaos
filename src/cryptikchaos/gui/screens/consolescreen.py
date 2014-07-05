'''
Created on Jun 29, 2014

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"

from kivy.uix.screenmanager import Screen

from cryptikchaos.gui.consolewin import ConsoleWindow


class ConsoleScreen(Screen):
    
    def __init__(self, greeting, font_type, font_size, 
        handleinput_cmd_hook, getcommands_cmd_hook, goto_inputscreen, **kwargs):
        
        super(ConsoleScreen, self).__init__(**kwargs)
        
        self.console_window = ConsoleWindow(
            greeting=greeting,
            font_type=font_type, 
            font_size=font_size, 
            handleinput_cmd_hook=handleinput_cmd_hook, 
            getcommands_cmd_hook=getcommands_cmd_hook, 
            goto_inputscreen=goto_inputscreen
        )
        
        ## Add console window widget to screen
        self.add_widget(self.console_window)
           
        self.inputtext_gui_hook=self.console_window.inputtext_gui_hook
        self.getmaxwidth_gui_hook=self.console_window.getmaxwidth_gui_hook
