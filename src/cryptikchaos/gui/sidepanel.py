'''
Created on Dec 14, 2013

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class SidePanel(BoxLayout):

    def __init__(self, drawer, main_panel):

        # Hooks
        self.handleinput_cmd_hook = None

        # Parent hooks
        self.drawer = drawer
        self.main_panel = main_panel

        # Init super
        super(SidePanel, self).__init__()

        # Set vertical orientation
        self.orientation = 'vertical'

        # Set up label
        title_label = Label(
            text="\n\n[color=999999][b]CryptikChaos[sup]TM[/sup][/b][/color]\n",
            markup=True,
            valign='top',
            halign='center'
        )
        # Bind text size to label
        title_label.bind(size=title_label.setter('text_size'))
        # Set height
        title_label.size_hint_y = 0.85
        # Bind to parent
        self.add_widget(title_label)

        # Minimize
        # Set up button
        console_button = Button(text='Console')
        # BG color
        console_button.background_color = [1, 1, 1, 1]
        # Set height
        console_button.size_hint_y = 0.05
        # Set action
        console_button.bind(on_release=self.action_console)
        # Bind to parent
        self.add_widget(console_button)

        # ABOUT
        # Set up button
        about_button = Button(text='About')
        # BG color
        about_button.background_color = [0, 0, 0, 1]
        # Set height
        about_button.size_hint_y = 0.05
        # Set action
        about_button.bind(on_release=self.action_about)
        # Bind to parent
        self.add_widget(about_button)

        # EXIT
        # Set up button
        exit_button = Button(text='Exit')
        # BG color
        exit_button.background_color = [0, 0, 0, 1]
        # Set height
        exit_button.size_hint_y = 0.05
        # Set action
        exit_button.bind(on_release=self.action_exit)
        # Bind to parent
        self.add_widget(exit_button)

    def register_handleinput_cmd_hook(self, hook):

        self.handleinput_cmd_hook = hook

    def action_exit(self, instance):

        self.drawer.toggle_state()
        # Exit app
        self.handleinput_cmd_hook("exit")

    def action_about(self, instance):

        self.drawer.toggle_state()
        self.main_panel.goto_about_screen()

    def action_console(self, instance):

        self.drawer.toggle_state()
        self.main_panel.goto_console_screen()
