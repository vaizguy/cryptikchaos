from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.logger import Logger

## Add podroid path
import pythonpath
pythonpath.AddSysPath('../../')

from podroid.comm.twiscomm import CommService
from podroid.config.configuration import *

class PodDroidApp(App, CommService):
    
       
    def build(self):
        ## Start GUI
        root = self.setup_gui()
        ## Start Server
        CommService.__init__(self, 123, 'localhost', 8000)
        #-#self.tcomm = self.setup_node()      
        return root


    def setup_node(self):
        self.print_message("Starting Server..")
        ## Values hard coded for now.
        #-#comm_service = CommService(123, 'localhost', 8000)
        self.print_message("Server Started..")
        #-#return comm_service

        
    def setup_gui(self):
        
        ## Create label
        self.label = Label(text='Welcome to Podnet.\n')
               
        ## Create Textbox
        self.textbox = TextInput(size_hint_y=.15, size_hint_x=.8, multiline=False)
        self.textbox.bind(on_text_validate=self.handle_input)

        ## Create button
        self.enter_button = Button(text='Enter', size_hint_y=.15, size_hint_x=.2) 
        self.enter_button.bind(on_press=self.handle_input)
        
        self.text_input_layout = BoxLayout(orientation='horizontal')
        self.text_input_layout.add_widget(self.textbox)
        self.text_input_layout.add_widget(self.enter_button)
        
        self.main_layout = BoxLayout(orientation='vertical')
        self.main_layout.add_widget(self.label)
        self.main_layout.add_widget(self.text_input_layout)
        return self.main_layout


    def on_connection(self, connection):
        self.print_message("connected succesfully!")
        self.connection = connection


    def send_message(self, *args):
        msg = self.textbox.text
        if msg and self.connection:
            self.connection.write(str(self.textbox.text))
            self.textbox.text = ""


    def print_message(self, msg):
        self.label.text += msg + "\n"
          
    
    def handle_input(self, *args):
        "*Send* button (and return key) event call back"
        
        cmd_line = self.textbox.text

        #if self.connected:
        if len(cmd_line):
            self.print_message("Processing: %s" % cmd_line)
            self.textbox.text = ""
            return self.exec_command(cmd_line)
        else:
            return None
   
   
    ## CLI methods ##
    def parse_line(self, line):
        "Parse command line."
        
        if line[0] == '@':
            line = 'send ' + line[1:]
                       
        ## Convert to cmd, args
        cmd_split = line.split(' ')
               
        (cmd, args) = (cmd_split[0], ' '.join(cmd_split[1:]))
        
        return (cmd, str(args))
    
    
    def exec_command(self, cmd_line):
        "Execute a command."
        
        if cmd_line is not None:
            (cmd, args) = self.parse_line(cmd_line)
            #print cmd, args
            ## Search for command
            try:
                func = getattr(self, 'cmd_' + cmd)
            except AttributeError:
                return self.default_cmd(cmd)
            else:
                #self.logger.info("Executing: '%s' Args: '%s'", cmd, args)
                #print args
                return func(args)
            
            
    def default_cmd(self, cmd):
        'If command not found'
        self.print_message('Invalid Command "%s"\n' % cmd)        
        #self.logger.error('Command "%s" not found', cmd)         
        
        
    def print_topics(self, header, cmds, maxcol):
        "Print help topics"
        if cmds:
            self.print_message("%s\n"%str(header))
            if constants.RULER:
                self.print_message("%s\n"%str(constants.RULER * len(header)))
            self.columnize(cmds, maxcol-1)
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
            raise TypeError, ("list[i] not a string for i in %s" %
                              ", ".join(map(str, nonstrings)))
        size = len(list)
        if size == 1:
            self.print_message('%s\n'%str(list[0]))
            return
        # Try every row count from 1 upwards
        for nrows in range(1, len(list)):
            ncols = (size+nrows-1) // nrows
            colwidths = []
            totwidth = -2
            for col in range(ncols):
                colwidth = 0
                for row in range(nrows):
                    i = row + nrows*col
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
                i = row + nrows*col
                if i >= size:
                    x = ""
                else:
                    x = list[i]
                texts.append(x)
            while texts and not texts[-1]:
                del texts[-1]
            for col in range(len(texts)):
                texts[col] = texts[col].ljust(colwidths[col])
            self.print_message("%s\n"%str("  ".join(texts))) 
            
             
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
                    doc=getattr(self, 'cmd_' + arg).__doc__
                    if doc:
                        self.print_message("%s\n"%str(doc))
                        return
                except AttributeError:
                    pass
                self.print_message("%s\n"%str(constants.NOHELP % (arg,)))
                return
            func()
        else:
            names = [name for name in dir(self) if 'help_' in name or 'cmd_' in name]
            cmds_doc = []
            cmds_undoc = []
            help_doc = {}
            for name in names:
                if name[:5] == 'help_':
                    help_doc[name[5:]]=1
            names.sort()
            # There can be duplicates if routines overridden
            prevname = ''
            for name in names:
                if name[:4] == 'cmd_':
                    if name == prevname:
                        continue
                    prevname = name
                    cmd=name[4:]
                    if cmd in help_doc:
                        cmds_doc.append(cmd)
                        del help_doc[cmd]
                    elif getattr(self, name).__doc__:
                        cmds_doc.append(cmd)
                    else:
                        cmds_undoc.append(cmd)
            self.print_message("%s\n"%str(constants.DOC_LEADER))
            self.print_topics(constants.DOC_HEADER,   cmds_doc,   80)
            self.print_topics(constants.MISC_HEADER,  help_doc.keys(),80)
            self.print_topics(constants.UNDOC_HEADER, cmds_undoc, 80)
            
            
    ## ---------------------------
    ## Command definitions 
    ## ---------------------------
    def cmd_send(self, cmdline):
        """
        Send message to other peers using peerid.
        Usage: send <pid> <message>
        """

        (pid, msg) = ( int(cmdline.split(' ')[0]), ' '.join(cmdline.split(' ')[1:]) )
        #-#self.tcomm.send_data(888, 'test_class', 'test_data')      
        
        if self.pass_message(pid, msg):
            Logger.debug( "Message sent." )
        else:
            Logger.error( "Unable to send message." )       
    
    
    def cmd_test(self, cmdline):
        """
        Tests the pod with the test server running.
        All testcases should be run here.
        Usage: test
        """
        
        ## Check sending of message.
        self.cmd_send(str(constants.LOCAL_TEST_PEER_ID) + " " + constants.LOCAL_TEST_STR) 


if __name__ == '__main__':
    
    PodDroidApp().run()
