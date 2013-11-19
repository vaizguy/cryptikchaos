'''
Created on Oct 8, 2013

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.5

from cryptikchaos.env.configuration import constants

from kivy.app import App
from kivy.resources import resource_add_path
from kivy.clock import Clock
from kivy.logger import Logger

from cryptikchaos.gui.consolewin import ConsoleWindow
from cryptikchaos.env.service import EnvService
from cryptikchaos.comm.service import CommService


class GUIService(App):
    "Graphival user interface service."
           
    # Init attributes
    inputtext_gui_hook = None
    getmaxwidth_gui_hook = None
    comm_service = None
    env_service = None

    def build(self):
        "Build the kivy App."
        
        # Add kivy resource paths
        resource_add_path(constants.KIVY_RESOURCE_PATH)
        
        # Build ConsoleWindow
        root = ConsoleWindow(
            # Input handler hook
            handleinput_cmd_hook=self.handleinput_cmd_hook,
            # Get command list hook
            getcommands_cmd_hook=self.getcommands_cmd_hook,
            # Console splash greeting
            greeting=constants.GUI_WELCOME_MSG,
            # Font type face
            font_type=constants.GUI_FONT_TYPE,
            # Font size
            font_size=constants.GUI_FONT_SIZE
        )
        ## TODO messy implementation, here if in the
        ## main application class we do not have self.handle_input_hook
        ## and self.get_commands_hook the app will crash.
        
        # Apeend text to console hook
        self.inputtext_gui_hook = root.inputtext_gui_hook
        # Get App GUI Width
        self.getmaxwidth_gui_hook = root.getmaxwidth_gui_hook
        
        return root
       
    def on_start(self):
        '''Event handler for the on_start event, which is fired after
        initialization (after build() has been called), and before the
        application is being run.
        '''
        
        Logger.info("Cryptikchaos Client started.")
        
        # Print criptikchaos banner
        Clock.schedule_once(self.print_logo, 1)
        
        # Initiate Twisted Server & Client services
        self.comm_service = CommService(
            peerid=constants.PEER_ID,
            peerkey=constants.LOCAL_TEST_CLIENT_KEY,
            host=self.my_host,
            port=constants.PEER_PORT,
            printer=self.print_message
        )
        
        # Initiate environment service
        self.env_service = EnvService()
        
    def on_stop(self):
        '''Event handler for the on_stop event, which is fired when the
        application has finished running (e.g. the window is about to be
        closed).
        '''
        
        Logger.info("Closing services.")  
        
        # Close services
        self.comm_service.__del__()
        self.env_service.__del__()
        
        Logger.info("Successfully closed services.")
        Logger.info("Closing Cryptikchaos Client.")

    def print_logo(self, *args):
        "Print the criptikchaos logo."
                
        if constants.GUI_LOGO:
            # Print logo through log
            Logger.info('\n{}'.format(constants.GUI_LOGO))