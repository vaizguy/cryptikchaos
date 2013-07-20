from commcoreserver import CommCoreServerFactory
from commcoreclient import CommCoreClientFactory
from twisted.internet import reactor

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

class PodDroidApp(App):
    connection = None

    def build(self):
        ## Start GUI
        root = self.setup_gui()
        ## Start Server
        self.start_server()      
        return root

    def start_server(self):
        self.print_message("Starting Server..")
        reactor.listenTCP(8000, CommCoreServerFactory(self))
        self.print_message("Server Started..")

        
    def setup_gui(self):
        self.textbox = TextInput(size_hint_y=.1, multiline=False)
        self.textbox.bind(on_text_validate=self.handle_input)
        self.label = Label(text='Welcome...\n')
        self.layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.textbox)
        return self.layout

    def connect_to_server(self):
        reactor.connectTCP('localhost', 8000, CommCoreClientFactory(self))

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

        
    def handle_command(self, msg):
        self.label.text  += "received:  %s\n" % msg

        if msg == "ping":  msg =  "pong"
        if msg == "plop":  msg = "kivy rocks"
        self.label.text += "processing: %s\n" % msg
        return msg
    
    
    def handle_input(self, *args):
        "*Send* button (and return key) event call back"
        
        cmd_line = self.textbox.text
        self.print_message("Processing: %s" % cmd_line)

        #if self.connected:
        if len(cmd_line):
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
        
        return (cmd, args)        
    
    
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
                self.logger.info("Executing: '%s' Args: '%s'", cmd, args)
                #print args
                return func(args)
            
            
    def default_cmd(self, cmd):
        'If command not found'
        self.print_message('Invalid Command "%s"\n' % cmd)        
        self.logger.error('Command "%s" not found', cmd)         
        
        
    def print_topics(self, header, cmds, maxcol):
        "Print help topics"
        if cmds:
            self.print_message("%s\n"%str(header))
            if self.ruler:
                self.print_message("%s\n"%str(self.ruler * len(header)))
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
            
            
                 
if __name__ == '__main__':
    PodDroidApp().run()
