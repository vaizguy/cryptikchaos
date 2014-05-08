'''
Created on Nov 10, 2013

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"

from kivy.logger import Logger

class ParserService:
    "shell-style parser class."
    
    def __init__(self, cmd_aliases):
        "Initialize parser."
        
        # Past entered commands
        self.past_commands = []
        # Set the command aliases
        self.cmd_aliases = cmd_aliases
        
    def _replace_aliases(self, line):
        "Replace command aliases i.e '!, @, #' with command."
        
        for alias in self.cmd_aliases.keys():
            # Check if alias is present
            if line[0] == alias:
                cmd = self.cmd_aliases[alias]
                Logger.info("Encountered alias '{}', Replacing with '{}'.".format(alias, cmd))
                line = "{} {}".format(cmd, line[1:])
                
        return line
        
    def parse_command(self, line):
        "parse command into required command format."
        
        if ' ' not in line:
            return (line , [])
               
        # Check for and replace aliases
        line = self._replace_aliases(line)
        
        # split line
        tokens = line.split(" ")
               
        # get command and args in required format
        (cmd, arg_str) = (tokens[0], tokens[1:])

        return (cmd, arg_str)


if __name__ == "__main__":
    
    cmd_string = "@arg1 --opt1 arg2 arg3 arg4"
    p = ParserService({"@": "cmd"})
    print p.parse_command(line=cmd_string)