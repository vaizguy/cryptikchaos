'''
Created on Jul 5, 2014

This file is part of CryptikChaos.

CryptikChaos is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CryptikChaos is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CryptikChaos. If not, see <http://www.gnu.org/licenses/>.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6.1"

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
