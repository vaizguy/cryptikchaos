'''
Created on Oct 15, 2013

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

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.clock import mainthread

from cryptikchaos.core.env.configuration import constants
if not (constants.PLATFORM_ANDROID or constants.ENABLE_INPUT_SCREEN):
    from cryptikchaos.core.gui.consoleinput import ConsoleInput
from cryptikchaos.core.gui.consolesv import ConsoleScrollView


class ConsoleWindow(GridLayout):

    "Console window class."

    def __init__(self, goto_inputscreen, greeting, **kwargs):

        # Init super
        super(ConsoleWindow, self).__init__(**kwargs)

        # Number of cols
        self.cols = 1
        
        # Save greeting
        self.greeting = greeting

        # Screen transition hook
        self.goto_input_screen = goto_inputscreen

        # Create scrollable label for console output
        self.scroll_view = ConsoleScrollView()
        self.scroll_view.size_hint_y = 0.9
        
        # Add scroll view widget
        self.add_widget(self.scroll_view)

        # Internal function-hook alias
        self.display_text = self.inputtext_gui_hook
        
        # Clear screen and print title
        self.display_text(greeting, clear=True)
        
        # Add progress bar
        self.progress_bar = ProgressBar(max=1000, size_hint_y=0.01)
        
        self.add_widget(self.progress_bar)

        # Input text box
        if not (constants.PLATFORM_ANDROID or constants.ENABLE_INPUT_SCREEN):
            self.console_input = ConsoleInput(
                # Goto console screen
                goto_consolescreen=lambda *args, **kwargs: None,
                # Size
                size_y=0.09
            )
                
            # Add widget
            self.add_widget(self.console_input)
            
        else:
            # Command input button
            self.enter_cmd_button = Button(
                text="Enter Command",
                size_hint_y=0.09,
            )
            # Bind event - on_press
            self.enter_cmd_button.bind(on_press=self.goto_inputscreen)
            # Add button
            self.add_widget(self.enter_cmd_button)

    # GUI Hooks-----------------------
    @mainthread
    def inputtext_gui_hook(self, text, clear=False):

        self.scroll_view.display_text(text, clear)

    @mainthread
    def getmaxwidth_gui_hook(self):

        return self.width
    
    @mainthread
    def cleardisplay_gui_hook(self):
        
        self.scroll_view.display_text(self.greeting, clear=True)
        
    @mainthread
    def cmdprog_gui_hook(self, status_val):
        
        self.progress_bar.value = status_val
    # ---------------------------------
    
    if not (constants.PLATFORM_ANDROID or constants.ENABLE_INPUT_SCREEN):
        def register_handleinput_cmd_hook(self, hook):
            
            self.console_input.register_handleinput_cmd_hook(hook)
            
        def register_getcommands_cmd_hook(self, hook):
            
            self.console_input.register_getcommands_cmd_hook(hook)

    def on_resize(self, instance, width, height):

        # New height and width
        instance.width = width
        instance.height = height

    def goto_inputscreen(self, instance):

        return self.goto_input_screen()


if __name__ == '__main__':

    from kivy.resources import resource_add_path
    from kivy.core.window import Window

    class ConsoleWindowTest(App):

        def build(self):

            # Build ConsoleWindow
            root = ConsoleWindow(
                goto_inputscreen=lambda *args, **kwargs: None,                 
                # Console splash greeting
                greeting="Testing Window!" * 1000,
            )

            # Window resize hook
            Window.bind(on_resize=self.resize)
            
            return root

        def handle_input_hook(self, text):

            print "Input", text

        def resize(self, instance, height, width):

            print "New heightxwidth {}x{}".format(height, width)

    # Add resource path
    resource_add_path(constants.KIVY_RESOURCE_PATH_1)

    ConsoleWindowTest().run()
