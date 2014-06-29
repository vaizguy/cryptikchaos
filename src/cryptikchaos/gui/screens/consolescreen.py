'''
Created on Jun 29, 2014

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"

from kivy.uix.screenmanager import Screen

from cryptikchaos.gui.consolewin import ConsoleWindow


class ConsoleScreen(Screen):
    
    def __init__(self, greeting, font_type, font_size, handleinput_cmd_hook, getcommands_cmd_hook, **kwargs):
        
        super(ConsoleScreen, self).__init__(**kwargs)
                
        self.console_window = ConsoleWindow(
            # Input handler hook
            handleinput_cmd_hook=handleinput_cmd_hook,
            # Get command list hook
            getcommands_cmd_hook=getcommands_cmd_hook,
            # Console splash greeting
            greeting=greeting,
            # Font type face
            font_type=font_type,
            # Font size
            font_size=font_size
        )
        
        ## Add console window widget to screen
        self.add_widget(self.console_window)
                
        self.inputtext_gui_hook=self.console_window.inputtext_gui_hook
        self.getmaxwidth_gui_hook=self.console_window.getmaxwidth_gui_hook
