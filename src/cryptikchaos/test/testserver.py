'''
Test Sever used to test the server side protocol.
To Run:
python testserver.py

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"

# Add cryptikchaos path
import pythonpath
pythonpath.AddSysPath('../..') # (pwd: test)

from cryptikchaos.core.env.configuration import constants
from cryptikchaos.core.comm.service import CommService
from cryptikchaos.core.gui.consolesv import ConsoleScrollView
from cryptikchaos.libs.utilities import get_time

from kivy.app import App
from kivy import Logger
from kivy.resources import resource_add_path

# Add kivy resource paths
resource_add_path(constants.KIVY_RESOURCE_PATH_1)


class CryptikChaosTestApp(App):

    "Test sever application."
    
    def build(self):

        self.test_win = ConsoleScrollView(
            font_type=constants.GUI_OUTPUT_FONT_TYPE,
            font_size=constants.GUI_OUTPUT_FONT_SIZE
        )

        # Display initial text
        self.test_win.display_text(
            """
=========================
CryptikChaos Test_ Server
=========================
:PeerID: {}\n
:PeerIP: {}\n
:Date: {}\n
------------\n
""".format(
            constants.LOCAL_TEST_PEER_ID,
            constants.LOCAL_TEST_HOST,
            get_time()
        )
        )

        return self.test_win

    def on_start(self):
        '''Event handler for the on_start event, which is fired after
        initialization (after build() has been called), and before the
        application is being run.
        '''

        Logger.info("Cryptikchaos Test server started.")

        # Initiate Twisted Server
        self.comm_service = CommService(
            peerid=constants.LOCAL_TEST_PEER_ID,
            host=constants.LOCAL_TEST_HOST,
            port=constants.LOCAL_TEST_PORT,
            clientinit=False,
            printer=self.print_message)

    def on_stop(self):
        '''Event handler for the on_stop event, which is fired when the
        application has finished running (e.g. the window is about to be
        closed).
        '''

        Logger.info("Closing services.")

        # Close services
        self.comm_service.__del__()

        Logger.info("Successfully closed services.")
        Logger.info("Closing Cryptikchaos Test Server.")

    def print_message(self, msg, peerid=None, intermediate=False):
        "Print a message in the output window."

        # Indicates multiline output required
        if intermediate:
            text = "{}{}".format(
                constants.GUI_LABEL_LEFT_PADDING,
                msg
            )
        else:
        # One line print
            if not peerid:
                peerid = self.comm_service.peerid

            # If local pid, substitute with peer name
            if peerid == self.comm_service.peerid:
                peerid = constants.PEER_NAME

            # Get peer message color
            rcc = self.comm_service.swarm_manager.get_peerid_color(
                peerid
            )

            # Single line output with peer id
            text = "{}{}[color={}]{}[/color] : {}".format(
                constants.GUI_LABEL_LEFT_PADDING,
                constants.GUI_LABEL_PROMPT_SYM,
                rcc,
                str(peerid),
                msg
            )

        text = '\n{}'.format(text)

        # Send text to console
        self.display_text('\n'+text)
            
        # Print in log
        if constants.ENABLE_CMD_LOG:
            # Get peer id for log
            if not peerid:
                logger_peerid = constants.PEER_NAME
            else:
                logger_peerid = peerid
                
            Logger.debug("[{}] => {}".format(logger_peerid, msg))

    def display_text(self, text):

        # Append line to label
        self.test_win.text += "\n[color={}]{}[/color]".format(
            constants.GUI_FONT_COLOR,
            text
        )

if __name__ == '__main__':
    
    from cryptikchaos.libs.utilities import run_kivy_app   
    run_kivy_app(CryptikChaosTestApp)
