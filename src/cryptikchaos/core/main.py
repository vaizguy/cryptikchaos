'''
Created on Jul 21, 2013

Podroid is a peer to peer chat application using kivy as the
frontend and twisted framework as the backend.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.4

# Add cryptikchaos path
import pythonpath
pythonpath.AddSysPath('../../')

from cryptikchaos.comm.service import CommService
from cryptikchaos.gui.service import GUIService
from cryptikchaos.config.service import EnvService

from cryptikchaos.config.configuration import constants
from cryptikchaos.libs.Table.prettytable import PrettyTable
from cryptikchaos.libs.utilities import get_my_ip
from cryptikchaos.libs.utilities import factor_line 
from cryptikchaos.libs.utilities import criptiklogo

from kivy.logger import Logger
from kivy.clock import Clock

import traceback


class CryptikChaosApp(
    # GUI service
    GUIService,  
    # Communications service
    CommService, 
    # Environment service
    EnvService
):

    """
    Main kivy app class.
    Contains both
    1. GUI service. (kivy.App)
    2. Twisted Network service. (twiscomm.CommService)
    """

    def build(self):
        "Build the kivy App."
                
        # Initiate Kivy GUI
        root = GUIService.build(self)
        
        # Determine host based on test mode
        my_host = constants.LOCAL_TEST_HOST
        # If not in test mode get LAN IP
        if not constants.ENABLE_TEST_MODE:
            my_host = get_my_ip()

        # Initiate Twisted Server & Client services
        CommService.__init__(
            self,
            peerid=constants.PEER_ID,
            peerkey=constants.LOCAL_TEST_CLIENT_KEY,
            host=my_host,
            port=constants.PEER_PORT,
            printer=self.print_message
        )
        
        # Initiate environment
        EnvService.__init__(self)

        return root

    def start(self):
        "Start the application."
                        
        # Print criptikchaos banner
        Clock.schedule_once(self.print_logo)
        
        try:
            # Run the GUI
            self.run()
        except:
            # print traceback
            print traceback.format_exc()
        finally:
            # Cleanup environment
            CommService.__del__(self)
        
    def print_logo(self, dt):
        "Print the criptikchaos logo"
        
        # Get logo
        logo = criptiklogo()
        
        if logo:
            print logo
        
    def print_message(self, msg, peerid=None, intermediate=False, factor=True):
        "Print a message in the output window."

        # Convert to string
        msg = str(msg).rstrip()
        
        # Indicates multiline output required
        if intermediate:
            text = "{}{}\n".format(
                constants.GUI_LABEL_LEFT_PADDING, 
                msg
            )
        else:
        # One line print
            if not peerid:
                peerid = self.my_peerid
                
            # If local pid, substitute with peer name
            if peerid == self.my_peerid:
                peerid = constants.PEER_NAME

            # Single line output with peer id
            text = "{}{}{} : {}\n".format(
                constants.GUI_LABEL_LEFT_PADDING,
                constants.GUI_LABEL_PROMPT_SYM,
                str(peerid),
                msg
            )
                
        # TODO Horizontal scroll is not working
        # Setting maximum line length to 75 and 
        # adding a newline character after 75 chars
        if factor:
            text = factor_line(text)
        else:
            text = '\n{}'.format(text) 

        self.append_text(text)

    ## GUI Callback Hooks
    ## ----------------------------------------------------
    def handle_input_hook(self, console_input):
        "*Send* button (and return key) event call back"
        
        return self.exec_command(console_input)
    
    def get_commands_hook(self):
        "Get the list of defined commands"
        
        return [cmd for cmd in dir(self) if "cmd_" in cmd]
    ## ----------------------------------------------------

    # -----------
    # CLI methods
    # -----------
    def parse_line(self, line):
        "Parse command line."

        if line[0] == '@':
            line = 'send {}'.format(line[1:])

        # Convert to cmd, args
        cmd_split = line.split(' ')

        (cmd, args) = (cmd_split[0], ' '.join(cmd_split[1:]))

        return (cmd, str(args))

    def exec_command(self, cmd_line):
        "Execute a command."

        if cmd_line is not None:
            (cmd, args) = self.parse_line(cmd_line)

            # Search for command
            try:
                func = getattr(self, 'cmd_' + cmd)
            except AttributeError:
                return self.default_cmd(cmd)
            else:
                return func(args)

    def default_cmd(self, cmd):
        "If command not found"

        # Command output
        self.print_message('Invalid Command "{}"'.format(cmd))
        # Command log
        Logger.error('Command "%s" not found', cmd)

    def print_topics(self, header, cmds, maxcol):
        "Print help topics"

        if cmds:
            self.print_message("{}".format(str(header)), None, True)
            if constants.RULER:
                self.print_message(("{}".format(str(constants.RULER * len(header)))), None, True)
            self.columnize(cmds, maxcol - 1)
            self.print_message(("\n"), None, True)
        
    def columnize(self, list, displaywidth=80):
        """Display a list of strings as a compact set of columns.

        Each column is only as wide as necessary.
        Columns are separated by two spaces (one was not legible enough).
        """
        
        if not list:
            self.print_message("<empty>\n", None, True)
            return
        nonstrings = [i for i in range(len(list))
                      if not isinstance(list[i], str)]
        if nonstrings:
            raise TypeError("list[i] not a string for i in %s" %
                            ", ".join(map(str, nonstrings)))
        size = len(list)
        if size == 1:
            self.print_message('%s' % str(list[0]), None, True)
            return
        # Try every row count from 1 upwards
        for nrows in range(1, len(list)):
            ncols = (size + nrows - 1) // nrows
            colwidths = []
            totwidth = -2
            for col in range(ncols):
                colwidth = 0
                for row in range(nrows):
                    i = row + nrows * col
                    if i >= size:
                        break
                    x = list[i]
                    colwidth = max(colwidth, len(x))
                colwidths.append(colwidth)
                totwidth += colwidth + 2
                if totwidth > displaywidth:
                    break
            if totwidth <= displaywidth:
                break
        else:
            nrows = len(list)
            ncols = 1
            colwidths = [0]
        for row in range(nrows):
            texts = []
            for col in range(ncols):
                i = row + nrows * col
                if i >= size:
                    x = ""
                else:
                    x = list[i]
                texts.append(x)
            while texts and not texts[-1]:
                del texts[-1]
            for col in range(len(texts)):
                texts[col] = texts[col].ljust(colwidths[col])
            self.print_message("%s" % str("  ".join(texts)), None, True)

    def cmd_help(self, arg):
        """
        Displays all available command information.
        Usage: help [command]"""

        if arg:
            # XXX check arg syntax
            try:
                func = getattr(self, 'help_' + arg)
            except AttributeError:
                try:
                    doc = getattr(self, 'cmd_' + arg).__doc__
                    if doc:
                        self.print_message("%s" % str(doc), factor=False)
                        return
                except AttributeError:
                    pass
                self.print_message("%s" % str(constants.NOHELP % (arg,)))
                return
            func()
        else:
            names = [name for name in dir(
                self) if 'help_' in name or 'cmd_' in name]
            cmds_doc = []
            cmds_undoc = []
            help_doc = {}
            for name in names:
                if name[:5] == 'help_':
                    help_doc[name[5:]] = 1
            names.sort()
            # There can be duplicates if routines overridden
            prevname = ''
            for name in names:
                if name[:4] == 'cmd_':
                    if name == prevname:
                        continue
                    prevname = name
                    cmd = name[4:]
                    if cmd in help_doc:
                        cmds_doc.append(cmd)
                        del help_doc[cmd]
                    elif getattr(self, name).__doc__:
                        cmds_doc.append(cmd)
                    else:
                        cmds_undoc.append(cmd)
            self.print_message("%s" % str(constants.DOC_LEADER))
            self.print_topics(constants.DOC_HEADER, cmds_doc, 80)
            self.print_topics(constants.MISC_HEADER, help_doc.keys(), 80)
            self.print_topics(constants.UNDOC_HEADER, cmds_undoc, 80)

    # ---------------------------
    # Command definitions
    # ---------------------------

    def cmd_addpeer(self, cmdline):
        """
        Add new peer.
        Usage: addpeer <pid> <host>
        """
        
        try:
            (pid, host) = (int(cmdline.split(' ')[0]), cmdline.split(' ')[1])
        except:
            self.print_message("Incorrect use of command 'addpeer'.")
            self.cmd_help("addpeer")
            return None
        else:
            self.print_message("Adding Peer {}.".format(pid))
            self.add_peer_to_swarm(pid, host)

    def cmd_addtest(self, cmdline):
        """
        Add test server.
        Usage: addtest
        """
        
        # Print to console
        self.print_message(
            "Adding Test server {}@{}".format(
                constants.LOCAL_TEST_HOST, 
                constants.LOCAL_TEST_PORT
            )
        )
        
        # Add Test server to swarm
        self.cmd_addpeer(
            "{} {}".format(
                constants.LOCAL_TEST_PEER_ID,
                constants.LOCAL_TEST_HOST
            )
        )

    def cmd_send(self, cmdline):
        """
        Send message to other peers using peerid.
        Usage: send <pid> <message>
        Alternative Short Usage: @<pid> <message>        
        """
        
        try:
            (pid, msg) = (
                int(cmdline.split(' ')[0]), ' '.join(cmdline.split(' ')[1:]))
        except:
            self.print_message("Incorrect use of command 'send'")
            self.cmd_help("send")
            return None
        else:
            pass

        if self.pass_message(pid, msg):
            # command log
            Logger.debug("Message sent to peer {}.".format(pid))
            # Display send message
            self.print_message("[{}] : {}".format(pid, msg))
        else:
            # command output
            self.print_message(
                "Unable to send message."
            )

    def cmd_sendtest(self, cmdline):
        """
        Tests the pod with the test server running.
        All testcases should be run here.
        Usage: test
        """
        
        # Print test string
        self.print_message("Sending Test String: {}".format(constants.LOCAL_TEST_STR))
        
        # Check sending of message.
        self.cmd_send(
            "{} {}".format(
                constants.LOCAL_TEST_PEER_ID,
                constants.LOCAL_TEST_STR
            )
        )

    def cmd_peers(self, cmdline):
        """
        View live peers.
        Usage: peers
        """

        plist = self.list_live_peers()

        if plist:
            table = PrettyTable(["ID", "KEY", "IP", "PORT", "STATUS"])

            for r in plist:
                table.add_row(r)

            self.print_message("List of live peers:\n{}".format(table), factor=False)
        else:
            self.print_message("No live peers.")

    def cmd_graphswarm(self, cmdline):
        """
        View connected peers in graph format.
        Requires: Networkx python graph library.
        Usage: graphswarm
        """

        if self.build_swarm_graph():
            self.print_message("Generated peer graph.")
        else:
            self.print_message("Could not generate graph.")
            
    def cmd_env(self, cmdline):
        """
        View Application environment constants.
        (useful for realtime debugging)
        Usage: env
        """
        
        self.print_message(
            """\n\nEnvironment Constants:\nTo see value use: 'eko <constant name>'"""
        )
        
        for c in self.list_constants():
            self.print_message(msg=c, intermediate=True)
        
    def cmd_eko(self, cmdline):
        """
        View environment constant value.
        Usage: eko <constant name>
        """
        
        v = self.get_constant(cmdline)
        
        if v:
            self.print_message("{} => {}".format(cmdline, v))
        else:
            self.print_message("{}".format(cmdline))

if __name__ == '__main__':

    # Build App
    App = CryptikChaosApp()
    # Start App mainloop
    App.start()
