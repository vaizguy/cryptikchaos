'''
Created on Oct 8, 2013

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
from kivy.resources import resource_add_path
from kivy.logger import Logger
from kivy.core.window import Window
from kivy.clock import Clock

from cryptikchaos.core.env.configuration import constants

try:
    from cryptikchaos.libs.garden.navigationdrawer \
        import NavigationDrawer
except ImportError:
        from kivy.garden.navigationdrawer import NavigationDrawer
else:
    pass

from cryptikchaos.core.gui.mainpanel import MainPanel
from cryptikchaos.core.gui.sidepanel import SidePanel

# Add kivy resource paths
resource_add_path(constants.KIVY_RESOURCE_PATH_1)
resource_add_path(constants.KIVY_RESOURCE_PATH_2)


class GUIService(App):

    "Graphical user interface service."

    # Init attributes
    core_services = None

    def __init__(self, handleinput_cmd_hook, getcommands_cmd_hook, **kwargs):

        # Init App
        super(GUIService, self).__init__(**kwargs)
        
        # Disable default kivy settings
        self.use_kivy_settings = False
        
        # Main drawer
        self.drawer = NavigationDrawer()

        # Set up Main panel
        self.main_panel = MainPanel(
            # drawer obj
            drawer=self.drawer,
            # Console splash greeting
            greeting=constants.GUI_WELCOME_MSG,
        )

        # Set up Side pane
        self.side_panel = SidePanel(
            # drawer obj
            drawer=self.drawer,
            # screen manager obj
            main_panel=self.main_panel
        )

        # Apeend text to console hook
        self.inputtext_gui_hook = self.main_panel.inputtext_gui_hook
        # Get App GUI Width
        self.getmaxwidth_gui_hook = self.main_panel.getmaxwidth_gui_hook
        # Clear display hook
        self.cleardisplay_gui_hook = self.main_panel.cleardisplay_gui_hook
        # Update progress bar
        self.cmdprog_gui_hook = self.main_panel.cmdprog_gui_hook

        # Register CMD hooks
        self.main_panel.register_handleinput_cmd_hook(
            handleinput_cmd_hook)
        self.main_panel.register_getcommands_cmd_hook(
            getcommands_cmd_hook)
        self.side_panel.register_handleinput_cmd_hook(
            handleinput_cmd_hook)

    def build(self):
        "Build the kivy App."
        
        # Set title
        self.title = "CryptikChaos"

        # Add main and side pane
        self.drawer.add_widget(self.side_panel)
        self.drawer.add_widget(self.main_panel)

        # Set animation type
        self.drawer.anim_type = 'slide_above_anim'

        # Bind Keyboard hook
        self.bind(on_start=self.post_build_init)

        return self.drawer

    def on_start(self):
        '''Event handler for the on_start event, which is fired after
        initialization (after build() has been called), and before the
        application is being run.
        '''

        Logger.debug("GUI: Cryptikchaos Client started.")

        # Print criptikchaos banner
        Clock.schedule_once(self.print_logo, 1)

    def on_stop(self):
        '''Event handler for the on_stop event, which is fired when the
        application has finished running (e.g. the window is about to be
        closed).
        '''
        
        Logger.debug("GUI: Stopped Cryptikchaos Client.")

    def on_pause(self):

        return True

    def on_resume(self):

        pass

    def print_logo(self, *args):
        "Print the criptikchaos logo."

        if constants.GUI_LOGO:
            # Print logo through log
            Logger.info('GUI: \n{}'.format(constants.GUI_LOGO))

        return args

    def post_build_init(self, *args):

        if constants.PLATFORM_ANDROID:
            import android
            android.map_key(android.KEYCODE_BACK, 1001)

        win = Window
        win.bind(on_keyboard=self.my_key_handler)
        
    def toggle_drawer_state(self):
        if self.drawer.state == "open":
            self.drawer.anim_to_state("closed")
        else:
            self.drawer.anim_to_state("open")
        
    def my_key_handler(self, window, keycode1, keycode2, text, modifiers):
        
        #Logger.debug("H/W Keypress: {}".format(keycode1))
        
        if keycode1 in [27, 1001]:
            # Go to console screen or close app
            if self.drawer.state == "open":
                self.drawer.anim_to_state("closed")
            elif self.main_panel.is_console_focused():
                self.stop()
            else:
                self.main_panel.goto_console_screen()
            return True
        elif keycode1 == 319:
            # Open navbar with menu key
            self.toggle_drawer_state()
            return True
        else:
            return False
