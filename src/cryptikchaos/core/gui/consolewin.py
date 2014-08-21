'''
Created on Oct 15, 2013

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

from cryptikchaos.core.env.configuration import constants
if not (constants.PLATFORM_ANDROID or constants.ENABLE_INPUT_SCREEN):
    from cryptikchaoscore.gui.consoleinput import ConsoleInput
from cryptikchaos.core.gui.consolesv import ConsoleScrollView


class ConsoleWindow(GridLayout):

    "Console window class."

    def __init__(self, goto_inputscreen, greeting):

        # Init super
        super(ConsoleWindow, self).__init__()

        # Number of cols
        self.cols = 1

        self.goto_input_screen = goto_inputscreen

        # Create viewing area
        self.view_area = GridLayout(cols=1, size_hint=(1, None))

        ## Create scrollable label for console output
        self.scroll_view = ConsoleScrollView()
        
        self.add_widget(self.scroll_view)

        # Internal function-hook alias
        self.display_text = self.inputtext_gui_hook
        self.display_text(greeting)

        # Input text box
        if not (constants.PLATFORM_ANDROID or constants.ENABLE_INPUT_SCREEN):
            self.console_input = ConsoleInput(
                # Goto console screen
                goto_consolescreen=lambda *args, **kwargs: None,
                # Size
                size_y=0.1
            )
            # Add widget
            self.add_widget(self.console_input)
            
        else:
            # Command input button
            self.enter_cmd_button = Button(
                text="Enter Command",
                size_hint_y=0.1,
            )
            # Bind event - on_press
            self.enter_cmd_button.bind(on_press=self.goto_inputscreen)
            # Add button
            self.add_widget(self.enter_cmd_button)

    # GUI Hooks-----------------------
    def inputtext_gui_hook(self, text):

        self.scroll_view.display_text(text)

    def getmaxwidth_gui_hook(self):

        return self.width
    # ---------------------------------

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
                # Font type face
                font_type=constants.GUI_FONT_TYPE,
                # Font size
                font_size=14
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
