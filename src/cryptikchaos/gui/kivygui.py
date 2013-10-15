'''
Created on Oct 8, 2013

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.2

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from kivy.uix.button import Button
from kivy.logger import Logger
from kivy.uix.scrollview import ScrollView

from cryptikchaos.config.configuration import *

class GUIService(App):

    def build(self):

        "Build the kivy App."

        # Initiate Kivy GUI
        root = self.setup_gui()

        return root

    def setup_gui(self):
        "Setup the Kivy GUI"

        # Create label
        self.scroll_label = ScrollView(
            pos_hint={
                'center_x': 0.3,
                'center_y': 0.3
            }
        )

        # Create label
        self.label = Label(
            text=constants.GUI_WELCOME_MSG,
            halign='left',
            size_hint_y=None,
            height="40dp"
        )

        self.label.bind(texture_size=self.label.setter('size'))

        self.scroll_label.do_scroll_y = True
        self.scroll_label.add_widget(self.label)

        # Create Textbox
        self.textbox = TextInput(
            size_hint_y=.1,
            size_hint_x=.8,
            multiline=False
        )
        self.textbox.focus = True
        self.textbox.bind(on_text_validate=self.handle_input)

        # Create button
        self.enter_button = Button(
            text='Enter',
            size_hint_y=.1,
            size_hint_x=.2
        )
        self.enter_button.bind(on_press=self.handle_input)

        self.text_input_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 1)
        )

        self.text_input_layout.add_widget(self.textbox)
        self.text_input_layout.add_widget(self.enter_button)

        self.main_layout = BoxLayout(
            orientation='vertical',
            height="50dp"
        )

        self.main_layout.add_widget(self.scroll_label)
        self.main_layout.add_widget(self.text_input_layout)
        return self.main_layout