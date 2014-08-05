'''
Created on Jul 19, 2014

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"

from kivy.logger import Logger

from cryptikchaos.core.env.configuration import constants

from cryptikchaos.core.env.service import EnvService
from cryptikchaos.core.comm.service import CommService
from cryptikchaos.core.parser.service import ParserService
from cryptikchaos.core.device.service import DeviceService


class CoreServices:

    def __init__(self):

        # Peer host (by default is localhost)
        if constants.ENABLE_TEST_MODE:
            my_host = constants.LOCAL_TEST_HOST
        else:
            my_host = constants.PEER_HOST

        # Initiate device service
        self.device_service = DeviceService()

        # Initiate communication service
        self.comm_service = CommService(
            peerid=constants.PEER_ID,
            host=my_host,
            port=constants.PEER_PORT,
            printer=self.print_message
        )

        # Initiate environment service
        self.env_service = EnvService()

        # Initiate Lexical parser service
        self.parser_service = ParserService(
            cmd_aliases=constants.CMD_ALIASES
        )

        # Get hooks
        self.inputtext_gui_hook = None
        self.getmaxwidth_gui_hook = None

    def __del__(self):

        Logger.info("Closing services.")

        try:
            self.comm_service.__del__()
            self.env_service.__del__()
            self.parser_service.__del__()
        except:
            pass

        Logger.info("Successfully closed services.")

    def register_inputtext_gui_hook(self, hook):

        self.inputtext_gui_hook = hook

    def register_getmaxwidth_gui_hook(self, hook):

        self.getmaxwidth_gui_hook = hook

    def print_message(self, msg, peerid=None, intermediate=False, wrap=True):
        "Print a message in the output window."

        # Convert to string
        msg = str(msg).rstrip()

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
        self.inputtext_gui_hook(text)

    def print_table(self, table):

        self.print_message(msg=table, wrap=False)

    # Console-GUI Hooks
    # ----------------------------------------------------
    def handleinput_cmd_hook(self, console_input):
        "*Send* button (and return key) event call back."

        return self.exec_command(console_input)

    def getcommands_cmd_hook(self):
        "Get the list of defined commands."

        return [cmd for cmd in dir(self) if "cmd_" in cmd[:4]]
    # ----------------------------------------------------

    # -----------
    # CLI methods
    # -----------
    def parse_line(self, line):
        "Parse command line."

        (cmd, arg_str) = self.parser_service.parse_command(line)

        return (cmd, arg_str)

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
        "If command not found."

        # Command output
        self.print_message(
            'Invalid Command "{}", enter "help" for command listing.'.format(cmd))
        # Command log
        Logger.error('Command "%s" not found', cmd)

    def print_topics(self, header, cmds, maxcol):
        "Print help topics."

        if cmds:
            self.print_message("{}".format(str(header)), None, True)
            if constants.RULER:
                self.print_message(
                    ("{}".format(str(constants.RULER * len(header)))), None, True)
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
        Quick one-time tab completion can be done by pressing the TAB key.
        Usage: help [command]
        """

        if arg:

            if type(arg) in (list, tuple):
                arg = arg[0]

            # XXX check arg syntax
            try:
                func = getattr(self, 'help_' + arg)
            except AttributeError:
                try:
                    doc = getattr(self, 'cmd_' + arg).__doc__
                    if doc:
                        self.print_message("%s" % str(doc), wrap=False)
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

    def cmd_addpeer(self, cmdline=[]):
        """
        Command: addpeer
        Adds a new peer to your swarm.
        Usage: addpeer <pid> <host>
        """

        try:
            (pid, host) = (cmdline[0], cmdline[1])
        except IndexError:
            self.print_message("Incorrect use of command 'addpeer'.")
            self.cmd_help("addpeer")
            return None
        else:
            self.print_message("Adding Peer {} @ {}.".format(pid, host))
            self.comm_service.add_peer_to_swarm(pid, host)

    def cmd_addtest(self, _):
        """
        Commands: addtest
        Adds the test server to swarm.
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
            [constants.LOCAL_TEST_PEER_ID, constants.LOCAL_TEST_HOST]
        )

    def cmd_send(self, cmdline=[]):
        """
        Command: send
        Send a message to another peer's given ID. Peer must
        be present in the swarm. To view swarm use command 'peers'.
        Usage: send <pid> <message>
        Alternative Short Usage: @<pid> <message>
        """

        try:
            (pid, msg) = (
                cmdline[0], ' '.join(cmdline[1:]))
        except IndexError:
            self.print_message("Incorrect use of command 'send'")
            self.cmd_help("send")
            return None
        else:
            if not msg:
                Logger.warn("Please enter a message to send.")
                return None

        if self.comm_service.pass_message(pid, msg):
            # command log
            Logger.debug("Message sent to peer {}.".format(pid))
            # Display send message
            self.print_message("[>> {}] : {}".format(pid, msg))
        else:
            # command output
            self.print_message(
                "Unable to send message."
            )

    def cmd_sendtest(self, _):
        """
        Command: sendtest
        Tests the message sending capability of the client using a
        running test server.
        Usage: test
        """

        # Print test string
        self.print_message(
            "Sending Test String: {}".format(constants.LOCAL_TEST_STR)
        )

        # Check sending of message.
        self.cmd_send(
            [constants.LOCAL_TEST_PEER_ID, constants.LOCAL_TEST_STR]
        )

    def cmd_peers(self, _):
        """
        Command: peers
        View all peers present in the swarm.
        Usage: peers
        """

        self.print_table(
            self.comm_service.swarm_manager.peer_table()
        )

    def cmd_peerip(self, cmdline=[]):
        """
        Command: getip
        Display peer's IP address.
        Usage: peerip <peer ID 1> <peer ID 2> ... <peer ID n>
        """

        for peer_id in cmdline:
            self.comm_service.display_peer_host(peer_id)

    def cmd_env(self, _):
        """
        Command: env
        View Application configuration constants.
        (useful for realtime debugging)
        Usage: env
        """

        self.print_table(
            self.env_service.display_table()
        )

    def cmd_eko(self, cmdline=[]):
        """
        Command: eko
        View any configuration constant value.
        If constant name is not present then the
        name will be echoed to output.
        To view all constants use command 'env'.
        Usage: eko <constant name>
        """

        # Force value to be string
        if isinstance(cmdline, list):
            cmdline = " ".join(cmdline)

        # Get constant
        v = self.env_service.get_constant(cmdline)

        # Print constant value or string
        if v:
            self.print_message("{} => {}".format(cmdline, v))
        else:
            self.print_message("{}".format(cmdline))

    def cmd_exit(self, _):
        """
        Command: exit
        Exit the application
        Usage: exit
        """

        self.stop()

    # Pympler memory profiler
    if constants.PYMPLER_AVAILABLE:
        def cmd_memprof(self, _):
            """
            Command: memprof
            Lists memory footprints of active python objects.
            Requires Pympler module to be installed.
            Usage: memprof
            """

            self.env_service.memory_summary()
            self.print_message("Dumped Memory profile to terminal.")

    # Swarm graph visualizer
    if constants.NETWORKX_AVAILABLE:
        def cmd_graphswarm(self, _):
            """
            Command: graphswarm
            Visualize swarm using network graphing.
            Requires: Networkx python graph library to be installed.
            Usage: graphswarm
            """

            if self.comm_service.swarm_manager.plot_swarm_graph():
                self.print_message("Generated peer graph.")
            else:
                self.print_message("No peers in swarm.")