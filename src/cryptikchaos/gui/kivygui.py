'''
Created on Oct 8, 2013

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.3

from kivy.app import App

from cryptikchaos.gui.consolewin import ConsoleWindow
from cryptikchaos.config.configuration import constants


class GUIService(App):

    def build(self):

        "Build the kivy App."
        
        root = ConsoleWindow(
            self.handle_input,
            constants.GUI_WELCOME_MSG
        ) ## TODO messy implementation
        
        self.append_text = root.append_text_to_console
        
        return root