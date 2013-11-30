'''
Created on Jul 21, 2013

Podroid is a peer to peer chat application using kivy as the
frontend and twisted framework as the backend.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.5

# Add cryptikchaos path
import pythonpath
pythonpath.AddSysPath('../../')

from cryptikchaos.env.configuration import constants

from cryptikchaos.gui.service import GUIService

from cryptikchaos.libs.utilities import wrap_line

from cryptikchaos.core.parser.service import ParserService

from kivy.logger import Logger


class CryptikChaosApp(
    # GUI service
    GUIService,  
):

    """
    Main kivy app class.
    Contains both
    1. GUI service. (kivy.App)
    2. Twisted Network service. (twiscomm.CommService)
    """
           
    # Communications service
    comm_service = None
    # Config Environment service
    env_service = None
    # GUI service
    gui_service = None
    
    # Peer host (by default is localhost)
    my_host = constants.LOCAL_TEST_HOST
    
    # Lexical parser service
    parser_service = ParserService(
        cmd_aliases = {
            "@" : "send",
            "?" : "help"
        }
    )
  
    def build(self):
        "Build the kivy App."
        
        # Initiate Kivy GUI
        self.gui_service = GUIService.build(self)
        
        # If not in test mode get LAN IP
        if not constants.ENABLE_TEST_MODE:
            self.my_host = constants.PEER_HOST

        return self.gui_service
           
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
                
        # TODO Horizontal scroll is not working
        # Setting maximum line length to 75 and 
        # adding a newline character after 75 chars
        if wrap:
            # Get window size
            wsize = self.getmaxwidth_gui_hook()/8
            # Wrap line
            text = wrap_line(line=text, cmax=wsize)
        
        text = '\n{}'.format(text) 

        # Send text to console
        self.inputtext_gui_hook(text)
        
    def print_table(self, table):
        
        self.print_message(msg=table, wrap=False)

    ## Console-GUI Hooks
    ## ----------------------------------------------------
    def handleinput_cmd_hook(self, console_input):
        "*Send* button (and return key) event call back."
        
        return self.exec_command(console_input)
    
    def getcommands_cmd_hook(self):
        "Get the list of defined commands."
        
        return [cmd for cmd in dir(self) if "cmd_" in cmd[:4]]
    ## ----------------------------------------------------

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
        self.print_message('Invalid Command "{}"'.format(cmd))
        # Command log
        Logger.error('Command "%s" not found', cmd)

    def print_topics(self, header, cmds, maxcol):
        "Print help topics."

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
        Quick one-time tab completion can be done by pressing the TAB key.
        Usage: help [command]
        """

        if arg:
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

    def cmd_addpeer(self, cmdline):
        """
        Command: addpeer
        Adds a new peer to your swarm.
        Usage: addpeer <pid> <host>
        """
        
        try:
            (pid, host) = (cmdline.split(' ')[0], cmdline.split(' ')[1])
        except ValueError:
            self.print_message("Incorrect use of command 'addpeer'.")
            self.cmd_help("addpeer")
            return None
        else:
            self.print_message("Adding Peer {}.".format(pid))
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
            "{} {}".format(
                constants.LOCAL_TEST_PEER_ID,
                constants.LOCAL_TEST_HOST
            )
        )

    def cmd_send(self, cmdline):
        """
        Command: send
        Send a message to another peer's given ID. Peer must
        be present in the swarm. To view swarm use command 'peers'.
        Usage: send <pid> <message>
        Alternative Short Usage: @<pid> <message>        
        """
        
        try:
            (pid, msg) = (
                cmdline.split(' ')[0], ' '.join(cmdline.split(' ')[1:]))
        except ValueError:
            self.print_message("Incorrect use of command 'send'")
            self.cmd_help("send")
            return None
        else:
            if not msg:
                return None

        if self.comm_service.pass_message(pid, msg):
            # command log
            Logger.debug("Message sent to peer {}.".format(pid))
            # Display send message
            self.print_message("[{}] : {}".format(pid, msg))
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
        self.print_message("Sending Test String: {}".format(constants.LOCAL_TEST_STR))
        
        # Check sending of message.
        self.cmd_send(
            "{} {}".format(
                constants.LOCAL_TEST_PEER_ID,
                constants.LOCAL_TEST_STR
            )
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

    def cmd_graphswarm(self, _):
        """
        Command: grapgswarm
        Visualize swarm using network graphing.
        Requires: Networkx python graph library to be installed.
        Usage: graphswarm
        """

        if self.comm_service.swarm_manager.build_swarm_graph():
            self.print_message("Generated peer graph.")
        else:
            self.print_message("Could not generate graph.")
            
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
                       
    def cmd_eko(self, cmdline):
        """
        Command: eko
        View any configuration constant value.
        To view all constants use command 'env'.
        Usage: eko <constant name>
        """
        
        v = self.env_service.get_constant(cmdline)
        
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
    if constants.PYMPLER:
        def cmd_memprof(self, _):
            """
            Command: memprof
            Lists memory footprints of active python objects.
            Top-50
            Usage: memprof
            """
            
            self.env_service.memory_summary()
            self.print_message("Dumped Memory profile to terminal.")


if __name__ == '__main__':

    try:
        # Build App interface
        App = CryptikChaosApp()    
        # Start App mainloop
        App.run()
    except KeyboardInterrupt:
        Logger.info("Recieved Keyboard interrupt. [CTRL+C]")
        # Stop services
        App.on_stop()
    else:
        Logger.info("Closed Cryptikchaos Client.")
        

