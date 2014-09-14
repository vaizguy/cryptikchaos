'''
Created on Jun 29, 2014

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

from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import SlideTransition

from cryptikchaos.core.env.configuration import constants
from cryptikchaos.core.gui.screens.consolescreen import ConsoleScreen
from cryptikchaos.core.gui.screens.aboutscreen import AboutScreen
from cryptikchaos.core.gui.screens.inputscreen import InputScreen


class MainPanel(ScreenManager):

    def __init__(self, drawer, greeting, **kwargs):

        # Init Screen manager
        super(ScreenManager, self).__init__(**kwargs)

        # Parent drawer
        self.drawer = drawer

        # Animation
        self.transition_slide_up = SlideTransition(direction="up")
        self.transition_slide_down = SlideTransition(direction="down")
        self.transition_slide_right = SlideTransition(direction="right")
        self.transition_slide_left = SlideTransition(direction="left")

        # Console screen
        self.console_screen = ConsoleScreen(
            greeting=greeting,
            goto_inputscreen=self.goto_input_screen,
            name="console"
        )

        # About app info screen
        self.about_screen = AboutScreen(name="about")

        # Text input screen
        self.input_screen = InputScreen(
            goto_consolescreen=self.goto_console_screen,
            name="input"
        )

        # Add console - GUI hooks
        self.inputtext_gui_hook = self.console_screen.console_window.inputtext_gui_hook
        self.getmaxwidth_gui_hook = self.console_screen.console_window.getmaxwidth_gui_hook
        self.cleardisplay_gui_hook = self.console_screen.console_window.cleardisplay_gui_hook
        self.cmdprog_gui_hook = self.console_screen.console_window.cmdprog_gui_hook
        self.focus_input_gui_hook = self.input_screen.console_input.focus_input_box
        self.unfocus_input_gui_hook = self.input_screen.console_input.unfocus_input_box

        # Add console screen widget to main screen manager
        self.add_widget(self.console_screen)
        # Add about screen
        self.add_widget(self.about_screen)
        # Add input screen
        self.add_widget(self.input_screen)

        # Default screen
        self.current = "console"

    def register_handleinput_cmd_hook(self, hook):
        
        if not (constants.PLATFORM_ANDROID or constants.ENABLE_INPUT_SCREEN):
            self.console_screen.console_window.console_input.register_handleinput_cmd_hook(hook)
        else:
            self.input_screen.register_handleinput_cmd_hook(hook)

    def register_getcommands_cmd_hook(self, hook):
        
        if not (constants.PLATFORM_ANDROID or constants.ENABLE_INPUT_SCREEN):
            self.console_screen.console_window.console_input.register_getcommands_cmd_hook(hook)
        else:
            self.input_screen.register_getcommands_cmd_hook(hook)

    def goto_console_screen(self):

        self.close_navbar()
        self.unfocus_input_gui_hook()
        self.transition = self.transition_slide_down
        self.current = "console"

    def goto_about_screen(self):

        self.close_navbar()
        self.unfocus_input_gui_hook()
        self.transition = self.transition_slide_up
        self.current = "about"

    def goto_input_screen(self):

        self.close_navbar()
        self.transition = self.transition_slide_down
        self.current = "input"
        self.focus_input_gui_hook()

    def is_console_focused(self):
        return self.current == "console"

    def close_navbar(self):
        
        if self.drawer:
            if self.drawer.state == "open":
                self.drawer.anim_to_state("closed")


if __name__ == '__main__':

    from kivy.app import App

    # Add kivy resource paths
    from kivy.resources import resource_add_path
    resource_add_path(constants.KIVY_RESOURCE_PATH_1)
    resource_add_path(constants.KIVY_RESOURCE_PATH_2)

    class ScreenManagerApp(App):

        def build(self):
            root = MainPanel(
                drawer=None,
                greeting="MainPanel Test",
            )

            return root

    ScreenManagerApp().run()
