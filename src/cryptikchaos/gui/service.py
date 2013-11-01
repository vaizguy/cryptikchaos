'''
Created on Oct 8, 2013

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.4

from kivy.app import App
from kivy.resources import resource_add_path

from cryptikchaos.gui.consolewin import ConsoleWindow
from cryptikchaos.config.configuration import constants


class GUIService(App):
    "Graphival user interface service."

    def build(self):
        "Build the kivy App."
        
        # Add kivy resource paths
        resource_add_path(constants.KIVY_RESOURCE_PATH)
        
        # Build ConsoleWindow
        root = ConsoleWindow(
            # Input handler hook
            handle_input_hook=self.handle_input_hook,
            # Get command list hook
            get_cmd_hook=self.get_commands_hook,
            # Console splash greeting
            greeting=constants.GUI_WELCOME_MSG,
            # Font type face
            font_type=constants.GUI_FONT_TYPE,
            # Font size
            font_size=constants.GUI_FONT_SIZE
        )
        ## TODO messy implementation, here if in the
        ## main application class we do not have self.handle_input_hook
        ## and self.get_commands_hook the app will crash.
        
        # Apeend text to console hook
        self.append_text_hook = root.append_text_to_console
        
        # Get App GUI Width
        self.get_maxwidth_hook = root.get_maxwidth
        
        return root