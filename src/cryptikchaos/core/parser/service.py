'''
Created on Nov 10, 2013

@author: vaizguy
'''

from shlex import shlex


class ParserService:
    "shell-style lexical parser class."
    
    def __init__(self, cmd_aliases={}):
        "Initialize parser."
        
        # Past entered commands
        self.past_commands = []
        # Shell lexer
        self.shell_lexer = shlex
        # Set the command aliases
        self.cmd_aliases = cmd_aliases
        
    def _replace_aliases(self, line):
        "Replace command aliases i.e '!, @, #' with command."
        
        for alias in self.cmd_aliases.keys():
            # Check if alias is present
            if line[0] == alias:
                cmd = self.cmd_aliases[alias]
                line = "{} {}".format(cmd, line[1:])
                
        return line
        
    def parse_command(self, line):
        "parse command into required command format."
        
        # Check for and replace aliases
        line = self._replace_aliases(line)
        # create lexer
        shlexer = self.shell_lexer(instream=line, posix=True)
        # get command and args in required format
        (cmd, arg_str) = (next(shlexer), shlexer.instream.read())
        
        return (cmd, arg_str)


if __name__ == "__main__":
    
    cmd_string = "@arg1 --opt1 arg2 arg3 arg4"
    p = Parser({"@": "cmd"})
    print p.parse_command(line=cmd_string)