'''
Created on Oct 8, 2013

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.4

from kivy.app import App

from cryptikchaos.gui.consolewin import ConsoleWindow
from cryptikchaos.config.configuration import constants


class GUIService(App):
    "Graphival user interface service."

    def build(self):
        "Build the kivy App."
        
        root = ConsoleWindow(
            # Input handler hook
            handle_input_hook=self.handle_input_hook,
            # Get command list hook
            get_cmd_hook=self.get_commands_hook,
            # Console splash greeting
            greeting=constants.GUI_WELCOME_MSG
        ) ## TODO messy implementation
        
        self.append_text = root.append_text_to_console
        
        return root