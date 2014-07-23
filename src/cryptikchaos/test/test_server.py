'''
Test Sever used to test the server side protocol.
To Run:
python test_server.py

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"

# Add cryptikchaos path
import pythonpath
pythonpath.AddSysPath('../../')

from cryptikchaos.core.env.configuration import constants
from cryptikchaos.core.comm.service import CommService
from cryptikchaos.libs.utilities import wrap_line
from cryptikchaos.libs.utilities import get_time

from kivy.app import App
from kivy import Logger
from kivy.uix.label import Label
from kivy.resources import resource_add_path

# Add kivy resource paths
resource_add_path(constants.KIVY_RESOURCE_PATH_1)


class TestServerApp(App):

    "Test sever application."

    def build(self):

        self.label = Label(
            markup=True,
            font_name=constants.GUI_FONT_TYPE,
            font_size=constants.GUI_FONT_SIZE,
            text_size=(750, None),
            shorten=True,
            valign='top'
        )

        # Display initial text
        self.display_text(
            """
            \n>> Test Server started <<\
            \n>> Peer {}--{} <<\
            \n[{}]\
            \n\
            \n""".format(
            constants.LOCAL_TEST_PEER_ID,
            constants.LOCAL_TEST_HOST,
            get_time()
        )
        )

        return self.label

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

    def print_message(self, msg, peerid=None):
        "Print a message in the output window."

        # Convert to string
        msg = str(msg).rstrip()

        if not peerid:
            peerid = constants.LOCAL_TEST_PEER_ID

        # If local pid, substitute with peer name
        if peerid == constants.LOCAL_TEST_PEER_ID:
            peerid = constants.LOCAL_TEST_PEER_NAME

        # Get peer message color
        rcc = self.comm_service.swarm_manager.get_peerid_color(
            peerid
        )

        # Single line output with peer id
        text = "{}{}[color={}]{}[/color] : {}\n".format(
            constants.GUI_LABEL_LEFT_PADDING,
            constants.GUI_LABEL_PROMPT_SYM,
            rcc,
            str(peerid),
            msg
        )

        # Factor line
        text = wrap_line(text)

        # Add text
        self.display_text(text)

    def display_text(self, text):

        # Append line to label
        self.label.text += "[color={}]{}[/color]".format(
            constants.GUI_FONT_COLOR,
            text
        )

if __name__ == '__main__':
    try:
        # Build server interface
        TServerApp = TestServerApp()
        # Start test server main loop
        TServerApp.run()
    except KeyboardInterrupt:
        Logger.info("Recieved Keyboard interrupt. [CTRL+C]")
        # Stop services
        TServerApp.on_stop()
    else:
        Logger.info("Closed Cryptikchaos Test Server.")
