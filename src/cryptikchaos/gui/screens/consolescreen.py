'''
Created on Jun 29, 2014

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"

from kivy.uix.screenmanager import Screen

from cryptikchaos.gui.consolewin import ConsoleWindow


class ConsoleScreen(Screen):
    
    def __init__(self, greeting, font_type, font_size, goto_inputscreen, **kwargs):
        
        super(ConsoleScreen, self).__init__(**kwargs)
        
        self.console_window = ConsoleWindow(
            greeting=greeting,
            font_type=font_type, 
            font_size=font_size, 
            goto_inputscreen=goto_inputscreen
        )

        ## Add console window widget to screen
        self.add_widget(self.console_window)