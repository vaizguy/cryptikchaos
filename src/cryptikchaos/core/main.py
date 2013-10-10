'''
Created on Jul 21, 2013

Podroid is a peer to peer chat application using kivy as the
frontend and twisted framework as the backend.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.1

# Add cryptikchaos path
import pythonpath
pythonpath.AddSysPath('../../')

from cryptikchaos.comm.twiscomm import CommService
from cryptikchaos.gui.kivygui import GUIService
from cryptikchaos.config.configuration import *
from cryptikchaos.libs.Table.prettytable import PrettyTable

import uuid

from kivy.logger import Logger


class PodDroidApp(GUIService, CommService):

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

        # Initiate Twisted Server & Client services
        CommService.__init__(self, 
                             peerid=constants.PEER_ID,
                             peerkey=constants.LOCAL_TEST_CLIENT_KEY,
                             host=constants.LOCAL_TEST_HOST,
                             port=constants.PEER_PORT,
                             printer=self.print_message)

        return root

    def print_message(self, msg):
        "Print a message in the output window."

        # Convert to string
        msg = str(msg)

        self.label.text += constants.GUI_LABEL_LEFT_PADDING + \
            msg.strip(" ") + "\n"

    def handle_input(self, *args):
        "*Send* button (and return key) event call back"

        # Total text input entered by user
        cmd_line = self.textbox.text

        # if self.connected:
        if len(cmd_line):
            self.print_message(
                "{}".format(
                    constants.GUI_LABEL_PROMPT_SYM +
                    cmd_line))
            self.textbox.text = ""
            return self.exec_command(cmd_line)
        else:
            return None

    # -----------
    # CLI methods
    # -----------
    def parse_line(self, line):
        "Parse command line."

        if line[0] == '@':
            line = 'send ' + line[1:]

        # Convert to cmd, args
        cmd_split = line.split(' ')

        (cmd, args) = (cmd_split[0], ' '.join(cmd_split[1:]))

        return (cmd, str(args))

    def exec_command(self, cmd_line):
        "Execute a command."

        if cmd_line is not None:
            (cmd, args) = self.parse_line(cmd_line)
            # print cmd, args
            # Search for command
            try:
                func = getattr(self, 'cmd_' + cmd)
            except AttributeError:
                return self.default_cmd(cmd)
            else:
                #self.logger.info("Executing: '%s' Args: '%s'", cmd, args)
                # print args
                return func(args)

    def default_cmd(self, cmd):
        'If command not found'

        self.print_message('Invalid Command "{}"\n'.format(cmd))
        Logger.error('Command "%s" not found', cmd)

    def print_topics(self, header, cmds, maxcol):
        "Print help topics"

        if cmds:
            self.print_message("{}\n".format(str(header)))
            if constants.RULER:
                self.print_message("{}\n".format(str(constants.RULER * len(header))))
            self.columnize(cmds, maxcol - 1)
            self.print_message("\n")

    def columnize(self, list, displaywidth=80):
        """Display a list of strings as a compact set of columns.

        Each column is only as wide as necessary.
        Columns are separated by two spaces (one was not legible enough).
        """

        if not list:
            self.print_message("<empty>\n")
            return
        nonstrings = [i for i in range(len(list))
                      if not isinstance(list[i], str)]
        if nonstrings:
            raise TypeError("list[i] not a string for i in %s" %
                            ", ".join(map(str, nonstrings)))
        size = len(list)
        if size == 1:
            self.print_message('%s\n' % str(list[0]))
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
            self.print_message("%s\n" % str("  ".join(texts)))

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
                        self.print_message("%s\n" % str(doc))
                        return
                except AttributeError:
                    pass
                self.print_message("%s\n" % str(constants.NOHELP % (arg,)))
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
            self.print_message("%s\n" % str(constants.DOC_LEADER))
            self.print_topics(constants.DOC_HEADER, cmds_doc, 80)
            self.print_topics(constants.MISC_HEADER, help_doc.keys(), 80)
            self.print_topics(constants.UNDOC_HEADER, cmds_undoc, 80)

    # ---------------------------
    # Command definitions
    # ---------------------------
    
    def cmd_addpeer(self, cmdline):
        """
        Add new peer.
        Usage: addpeer <pid> <host> <port>
        """
        try:
            (pid, host) = (int(cmdline.split(' ')[0]), cmdline.split(' ')[1])
        except:
            self.print_message("Incorrect Command Use.")
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
        self.print_message(
            "Adding Test server {}@{}".format(
                constants.LOCAL_TEST_HOST, constants.LOCAL_TEST_PORT
                )
        )
        self.add_peer_to_swarm(888, "localhost")

    def cmd_send(self, cmdline):
        """
        Send message to other peers using peerid.
        Usage: send <pid> <message>
        """
        try:
            (pid, msg) = (
                int(cmdline.split(' ')[0]), ' '.join(cmdline.split(' ')[1:]))
        except:
            self.print_message("Incorrect Command Use.")
            self.cmd_help("send")
            return None
        else:
            pass

        if self.pass_message(pid, msg):
            Logger.debug("Message sent to peer {}.".format(pid))
        else:
            Logger.error(
                "Unable to send message. Peer {} is offline.".format(pid))

    def cmd_test(self, cmdline):
        """
        Tests the pod with the test server running.
        All testcases should be run here.
        Usage: test
        """
        # Check sending of message.
        self.cmd_send(
            str(constants.LOCAL_TEST_PEER_ID) + " " + constants.LOCAL_TEST_STR)

    def cmd_peers(self, cmdline):
        """
        View live peers.
        Usage: peers
        """

        self.print_message("List of live peers:")
        plist = self.list_live_peers()
        table = PrettyTable(["ID", "KEY", "IP", "PORT", "STATUS"])

        for r in plist:
            table.add_row(r)

        self.print_message(table)


if __name__ == '__main__':

    PodDroidApp().run()
