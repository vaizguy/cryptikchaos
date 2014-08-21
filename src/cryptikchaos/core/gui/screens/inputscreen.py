'''
Created on Jul 5, 2014

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"

from kivy.uix.screenmanager import Screen
from cryptikchaos.core.gui.consoleinput import ConsoleInput


class InputScreen(Screen):

    def __init__(self, goto_consolescreen, **kwargs):

        # Construct screen
        super(InputScreen, self).__init__(**kwargs)

        # Console input
        self.console_input = ConsoleInput(
            goto_consolescreen=goto_consolescreen
        )

        # Add the console input
        self.add_widget(self.console_input)

    def register_handleinput_cmd_hook(self, hook):

        self.console_input.register_handleinput_cmd_hook(hook)

    def register_getcommands_cmd_hook(self, hook):

        self.console_input.register_getcommands_cmd_hook(hook)
