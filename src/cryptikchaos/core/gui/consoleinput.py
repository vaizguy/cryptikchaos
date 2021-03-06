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

from re import match
from kivy.uix.textinput import TextInput

from cryptikchaos.core.env.configuration import constants


class ConsoleInput(TextInput):

    "Console text input class."

    def __init__(self, goto_consolescreen, size_y=1, **kwargs):

        # Init super
        super(ConsoleInput, self).__init__(**kwargs)

        # Single line input, enter triggers
        # on_text_validate
        self.multiline = True
        # Not password input
        self.password = False
        # Set size
        self.size_hint_y = size_y
        # Sets focus active
        self.focus = False
        # Set background color
        self.background_color = [0, 0, 0, 1]
        # Set text color
        self.foreground_color = [1, 1, 1, 1]
        # Set padding for text input
        if not constants.PLATFORM_ANDROID:
            self.padding = [15, 20, 10, 0]

        # Input command handler
        self.handleinput_cmd_hook = None
        # Get list of defined commands
        self.getcommands_cmd_hook = None
        # Go to console screen
        self.goto_consolescreen = goto_consolescreen

        # Prompt length
        self.prompt_len = len(constants.GUI_LABEL_PROMPT_SYM)

        # Command buffer
        self.autocomplete_buffer = set()
        self.help_displayed_flag = False

        # Bind to function on entry
        self.bind(on_text_validate=self.on_enter)

        # Finally add prompt
        self._reset_prompt(self)
        
        # Set hooks to do nothing
        self.handleinput_cmd_hook = lambda *args, **kwargs:None
        self.getcommands_cmd_hook = lambda *args, **kwargs:None

    def _filter_prompt(self, text):
        "Remove prompt symbol from text."

        if constants.GUI_LABEL_PROMPT_SYM in text:
            # If prompt in text
            return text[self.prompt_len:]
        else:
            return text

    def _get_input_text(self, instance):
        "Used to get console input text."

        return self._filter_prompt(instance.text)

    def _add_text(self, instance, text=None):
        "Used to access instance.text."

        # Change text
        if text:
            instance.text = "{}{}".format(
                constants.GUI_LABEL_PROMPT_SYM,
                text
            )
        else:
            instance.text = "{}".format(constants.GUI_LABEL_PROMPT_SYM)

    def _reset_prompt(self, instance):
        "Reset the prompt to default."

        # Clear input text in input box
        self._add_text(instance)

        # Reset cursor
        #instance.do_cursor_movement("cursor_end")

    def register_handleinput_cmd_hook(self, hook):

        self.handleinput_cmd_hook = hook

    def register_getcommands_cmd_hook(self, hook):

        self.getcommands_cmd_hook = hook

    def focus_input_box(self):

        self.focus = True

    def unfocus_input_box(self):

        self.focus = False

    def _pass(self):
        pass

    def on_enter(self, instance):
        "Called on text input entry."

        # Clear help displayed flag
        instance.help_displayed_flag = False

        # Clear command buffer
        instance.autocomplete_buffer = set()

        # Get data input
        input_text = instance._get_input_text(instance)

        # Set focus
        if not constants.ENABLE_INPUT_SCREEN:
            instance.focus_input_box()
        else:
            instance.unfocus_input_box()

        # Handle input
        if input_text:
            # Reset prompt
            instance._reset_prompt(instance)
            # Got to console screen
            instance.goto_consolescreen()
            # Handle the input
            instance.handleinput_cmd_hook(input_text)

    def on_tab(self, instance, pcmd):
        "Method hook for entry of [TAB]"
        
        if not self.help_displayed_flag and pcmd not in 'help':
            # Display help
            instance.handleinput_cmd_hook("help")

            # Set help displayed flag
            instance.help_displayed_flag = True

        # Reset prompt
        instance._reset_prompt(instance)

        # Available list of Commands
        command_list = [c[4:] for c in self.getcommands_cmd_hook()]

        # Get commands with pcmd matches
        pcmd_matches = [c for c in command_list if match(r'\s*{}'.format(pcmd), c)
                        and c not in instance.autocomplete_buffer]

        # Sort cmd list alphabetically
        pcmd_matches = sorted(pcmd_matches)

        # Reset autocomplete buffer
        if (instance.autocomplete_buffer == set(command_list)):
            instance.autocomplete_buffer = set()

        # command completion
        if pcmd_matches:
            # first match for now ## TODO
            fcmd = pcmd_matches.pop()
            # Send to command buffer
            instance.autocomplete_buffer.add(fcmd)
            # Change text
            instance._add_text(instance, fcmd)
            # move cursor to end
            instance.do_cursor_movement("cursor_end")

    def on_text(self, instance, value):
        "Method hook called on change of TextInput.text value."

        # Prompt is readonly
        if (
            len(value) <= instance.prompt_len or
            constants.GUI_LABEL_PROMPT_SYM not in
            value[:instance.prompt_len]
        ):
            # Reset prompt
            instance._reset_prompt(instance)

        # Partial comm
        pcmd = instance._filter_prompt(value).rstrip('\t')

        # If TAB is entered
        if (
            not constants.PLATFORM_ANDROID and
            9 in [ord(c) for c in value]
        ):
            instance.on_tab(instance, pcmd)

    def insert_text(self, substring, from_undo=False):
        "Method hook called on character input."

        # On entry of command
        if substring == "\n":
            return self.on_enter(self)

        return super(ConsoleInput, self).insert_text(substring, from_undo=from_undo)
