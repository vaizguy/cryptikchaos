'''
Created on Oct 15, 2013

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

from cryptikchaos.core.env.configuration import constants
if not (constants.PLATFORM_ANDROID or constants.ENABLE_INPUT_SCREEN):
    from cryptikchaos.gui.inputwin import ConsoleInput


class ConsoleWindow(GridLayout):

    "Console window class."

    def __init__(self, goto_inputscreen,
                 greeting, font_type, font_size):

        # Init super
        super(ConsoleWindow, self).__init__()

        # Number of cols
        self.cols = 1

        self.goto_input_screen = goto_inputscreen

        if not constants.PLATFORM_ANDROID:
            # Height and width
            self.height = 400
            self.width = 800

        # Create viewing area
        self.view_area = GridLayout(cols=1, size_hint=(1, None))

        # Create label for console output
        self.label = Label(
            size_hint=(1, None),
            markup=True,
            font_name=font_type,
            font_size=font_size,
            valign='top',
            halign='left',
        )

        if not constants.PLATFORM_ANDROID:
            self.label.text_size = (self.width - 50, None)
            self.label.shorten = True,

        # bind label to scrollable size
        self.label.bind(texture_size=self.label.setter('size'))

        # Add label to viewing area
        self.view_area.add_widget(self.label)

        # Scroll view label
        self.scroll_view = ScrollView(
            size_hint_y=0.9,
        )

        if not constants.PLATFORM_ANDROID:
            self.scroll_view.size = (self.height, self.width)

        # TODO X-axis scroll not working
        self.scroll_view.do_scroll_y = True
        self.scroll_view.do_scroll_x = True
        # Add label to scroll view
        self.scroll_view.add_widget(self.view_area)

        # Bind text size to view area
        self.view_area.bind(minimum_height=self.view_area.setter('height'))

        self.add_widget(self.scroll_view)

        # Internal function-hook alias
        self.display_text = self.inputtext_gui_hook

        # Display welcome message
        self.display_text(text=greeting)

        # Input text box
        if not (constants.PLATFORM_ANDROID or constants.ENABLE_INPUT_SCREEN):
            self.console_input = ConsoleInput(
                # Font type
                font_type=font_type,
                # Font size
                font_size=font_size,
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
                size_hint_y=0.1
            )
            self.enter_cmd_button.bind(on_press=self.goto_inputscreen)

            # Add button
            self.add_widget(self.enter_cmd_button)

    # GUI Hooks-----------------------
    def inputtext_gui_hook(self, text):

        self.label.text += "[color={}]{}[/color]".format(
            constants.GUI_FONT_COLOR,
            text
        )

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
                greeting="Testing Window!",
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
