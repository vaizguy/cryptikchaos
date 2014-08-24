'''
Created on Jun 29, 2014

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6.1"

from kivy.uix.screenmanager import Screen

from cryptikchaos.core.gui.consolewin import ConsoleWindow


class ConsoleScreen(Screen):

    def __init__(self, greeting, goto_inputscreen, **kwargs):

        super(ConsoleScreen, self).__init__(**kwargs)

        self.console_window = ConsoleWindow(
            greeting=greeting,
            goto_inputscreen=goto_inputscreen
        )

        # Add console window widget to screen
        self.add_widget(self.console_window)
