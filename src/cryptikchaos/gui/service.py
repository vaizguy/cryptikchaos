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
            handleInput_cmd_hook=self.handleInput_cmd_hook,
            # Get command list hook
            getCMD_cmd_hook=self.getCMD_cmd_hook,
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
        self.inputText_gui_hook = root.inputText_gui_hook
        
        # Get App GUI Width
        self.getMaxWidth_gui_hook = root.getMaxWidth_gui_hook
        
        return root