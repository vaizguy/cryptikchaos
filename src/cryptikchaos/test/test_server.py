'''
Test Sever used to test the server side protocol.
To Run:
python test_server.py

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.4

# Add cryptikchaos path
import pythonpath
pythonpath.AddSysPath('../../')

from cryptikchaos.config.configuration import constants
from cryptikchaos.comm.twiscomm import CommService
from cryptikchaos.libs.utilities import factor_line
from cryptikchaos.libs.utilities import get_time

from kivy.app import App
from kivy.uix.label import Label


class TestServerApp(App, CommService):
    "Test sever application."

    def build(self):

        # Initiate Twisted Server
        CommService.__init__(
            self,
            peerid=constants.LOCAL_TEST_PEER_ID,
            peerkey=constants.LOCAL_TEST_SERVER_KEY,
            host=constants.LOCAL_TEST_HOST,
            port=constants.LOCAL_TEST_PORT,
            clientinit=False,
            printer=self.print_message)

        self.label = Label(
            text="""
            \n+Test Server started+\
            \n[ {} ]
            \n""".format(get_time())
        )

        return self.label

    def print_message(self, msg, peerid=None):
        "Print a message in the output window."

        # Convert to string
        msg = str(msg).rstrip()
        
        text = ''

        if not peerid:
            peerid = constants.LOCAL_TEST_PEER_ID
            
        # If local pid, substitute with peer name
        if peerid == constants.LOCAL_TEST_PEER_ID:
            peerid = constants.LOCAL_TEST_PEER_NAME

        # Single line output with peer id
        text += "{}{}{} : {}\n".format(
            constants.GUI_LABEL_LEFT_PADDING,
            constants.GUI_LABEL_PROMPT_SYM,
            str(peerid),
            msg
        )
            
        # Factor line
        text = factor_line(text)
        
        # Append line to label
        self.label.text += text

if __name__ == '__main__':
    TestServerApp().run()
