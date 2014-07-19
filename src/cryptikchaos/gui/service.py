'''
Created on Oct 8, 2013

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"

from cryptikchaos.env.configuration import constants

from kivy.app import App
from kivy.resources import resource_add_path
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.core.window import Window

try:
    from cryptikchaos.libs.garden.navigationdrawer \
        import NavigationDrawer
except ImportError:
        from kivy.garden.navigationdrawer import NavigationDrawer
else:
    pass    
    
from cryptikchaos.gui.mainpanel import MainPanel
from cryptikchaos.gui.navbar import NavBar
from cryptikchaos.core.services import CoreServices

# Add kivy resource paths
resource_add_path(constants.KIVY_RESOURCE_PATH_1)
resource_add_path(constants.KIVY_RESOURCE_PATH_2)


class GUIService(App):
    "Graphival user interface service."
           
    # Init attributes
    inputtext_gui_hook = None
    getmaxwidth_gui_hook = None
    core_services = None

    def build(self):
        "Build the kivy App."
                
        # Main drawer
        drawer = NavigationDrawer()
        
        self.main_panel = MainPanel(
            # Input handler hook
            handleinput_cmd_hook=self.handleinput_cmd_hook,
            # Get command list hook
            getcommands_cmd_hook=self.getcommands_cmd_hook,
            # Console splash greeting
            greeting=constants.GUI_WELCOME_MSG,
            # Font type face
            font_type=constants.GUI_FONT_TYPE,
            # Font size
            font_size=constants.GUI_FONT_SIZE,
        )
        
        # Set up Side pane
        self.side_panel = NavBar(
            # Input handler hook
            handleinput_cmd_hook=self.handleinput_cmd_hook,
            # drawer obj
            drawer=drawer,
            # screen manager obj
            main_panel=self.main_panel                
        )
               
        ## TODO messy implementation, here if in the
        ## main application class we do not have self.handle_input_hook
        ## and self.get_commands_hook the app will crash.
        
        # Add main and side pane
        drawer.add_widget(self.side_panel)
        drawer.add_widget(self.main_panel)
        
        # Set animation type
        drawer.anim_type ='slide_above_anim'

        # Apeend text to console hook
        self.inputtext_gui_hook = self.main_panel.inputtext_gui_hook
        # Get App GUI Width
        self.getmaxwidth_gui_hook = self.main_panel.getmaxwidth_gui_hook
        
        # Bind Keyboard hook
        self.bind(on_start=self.post_build_init)
                
        return drawer
       
    def on_start(self):
        '''Event handler for the on_start event, which is fired after
        initialization (after build() has been called), and before the
        application is being run.
        '''
        
        Logger.info("Cryptikchaos Client started.")
        
        # Print criptikchaos banner
        Clock.schedule_once(self.print_logo, 1)
        
        # Start code services
        self.core_services = CoreServices(self.my_host, self.print_message)        
        
    def on_stop(self):
        '''Event handler for the on_stop event, which is fired when the
        application has finished running (e.g. the window is about to be
        closed).
        '''
        
        Logger.info("Closing services.")  
        
        ## Close services
        self.core_services.__del__()
        
        Logger.info("Successfully closed services.")
        Logger.info("Closing Cryptikchaos Client.")
        
    def on_pause(self):
        
        return True
    
    def on_resume(self):
        
        pass

    def print_logo(self, *args):
        "Print the criptikchaos logo."
                
        if constants.GUI_LOGO:
            # Print logo through log
            Logger.info('\n{}'.format(constants.GUI_LOGO))
        
        return args
    
    def post_build_init(self, *args):
        
        if constants.PLATFORM_ANDROID:
            import android
            android.map_key(android.KEYCODE_BACK, 1001)

        win = Window
        win.bind(on_keyboard=self.my_key_handler)

    def my_key_handler(self, window, keycode1, keycode2, text, modifiers):
        
        if keycode1 in [27, 1001]:
            # Go to console screen or close app
            if self.main_panel.is_console_focused():
                self.stop()                
            else:
                self.main_panel.goto_console_screen()
            return True
        return False