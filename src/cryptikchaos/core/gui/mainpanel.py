'''
Created on Jun 29, 2014

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"

from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import SlideTransition

from cryptikchaos.core.gui.screens.consolescreen import ConsoleScreen
from cryptikchaos.core.gui.screens.aboutscreen import AboutScreen
from cryptikchaos.core.gui.screens.inputscreen import InputScreen


class MainPanel(ScreenManager):

    def __init__(self, drawer, greeting, font_type, font_size, **kwargs):

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
            font_type=font_type,
            font_size=font_size,
            goto_inputscreen=self.goto_input_screen,
            name="console"
        )

        # About app info screen
        self.about_screen = AboutScreen(name="about")

        # Text input screen
        self.input_screen = InputScreen(
            font_type=font_type,
            font_size=font_size,
            goto_consolescreen=self.goto_console_screen,
            name="input"
        )

        # Add console - GUI hooks
        self.inputtext_gui_hook = self.console_screen.console_window.inputtext_gui_hook
        self.getmaxwidth_gui_hook = self.console_screen.console_window.getmaxwidth_gui_hook
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

        self.input_screen.register_handleinput_cmd_hook(hook)

    def register_getcommands_cmd_hook(self, hook):

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
        self.transition = self.transition_slide_left
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
    from cryptikchaos.core.env.configuration import constants

    # Add kivy resource paths
    from kivy.resources import resource_add_path
    resource_add_path(constants.KIVY_RESOURCE_PATH_1)
    resource_add_path(constants.KIVY_RESOURCE_PATH_2)

    class ScreenManagerApp(App):

        def build(self):
            root = MainPanel(
                drawer=None,
                greeting="MainPanel Test",
                font_type=constants.GUI_FONT_TYPE,
                font_size=constants.GUI_FONT_SIZE,
            )

            return root

    ScreenManagerApp().run()
