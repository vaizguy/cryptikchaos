'''
Created on Oct 19, 2013

View app environment constants through the App.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.5

from cryptikchaos.env.configuration import constants
from cryptikchaos.env import constants as const
from cryptikchaos.libs.utilities import serialize
from cryptikchaos.libs.utilities import deserialize

from cryptikchaos.libs.Table.prettytable import PrettyTable

from kivy import Logger

if constants.PYMPLER_AVAILABLE:
    from pympler import summary, muppy


class EnvService:
    """
    Used to view currently defined environment.
    """
    
    def __init__(self):
        
        ## Check and see if constants rebinding is unsuccessful
        try:
            constants.REBIND_CHECK = False
        except const.ConstError:
            Logger.info("Environment constants are secure.")
        else:
            raise Exception("Error with environment setup.")
                

        self.env_dict = {}

        # Populate constants
        for attr in dir(constants):
            if attr.isupper():
                self.env_dict[attr] = str(
                    getattr(constants, attr)
                ).encode('string_escape')
                
    def __del__(self):
        
        Logger.info("Clearing enviroment.")
        # Delete env dict
        if not self.env_dict:
            del self.env_dict

    def list_constants(self):
        "List all env constants."
        
        constants = []
        i = 1
        
        for k in sorted(self.env_dict.keys()):
            v = self.env_dict[k].strip()
            
            if len(v[:20]) < 20:
                constants.append(
                (i, k, "{}".format(v.encode('string_escape')[:20]))
                )
            else:
                constants.append(
                (i, k, "{}...".format(v.encode('string_escape')[:20]))
                )                
            i += 1
            
        return constants
    
    def get_constant(self, name):
        "Get value of particular constant."
        
        try:
            v = self.env_dict[name]
        except KeyError:
            return None
        else:
            return v
        
    def caps_conf_dict(self):
        "Return all the capsule config as dict."
        
        return { 
            fkey : self.env_dict[fkey] for fkey in sorted(
                [k for k in self.env_dict.keys() if k[0:5] == "STREAM_"]
            )
        }
               
    def serialize_stream_conf(self):
        "Serialize capsule configuration."
        
        return serialize(self.caps_conf_dict())
    
    def deserialize_stream_conf(self, serialstr):
        "Deserialize capsule configuration."
        
        return deserialize(serialstr)
    
    def config_equal(self, serialstr):
        """
        Check if recieved capsule configuration matches current
        capsule configuration.
        """
        
        return (
            self.deserialize_stream_conf(serialstr) == self.caps_conf_dict()
        )
    
    def display_table(self):
        """
        View Application environment constants.
        (useful for realtime debugging)
        Usage: env
        """
        
        constants = self.list_constants()
        
        if constants:
            table = PrettyTable(["S.NO", "CONSTANT", "VALUE"])
        
            for c in constants:
                table.add_row(c)
            
            return """
                \nEnvironment Constants:
                \nTo see value use: 'eko <constant name>'
                \n{}""".format(table)
        else:
            return "No environment variables defined."
        
    ## pympler inline Memory profiler Conditional code
    if constants.PYMPLER_AVAILABLE:
        def memory_summary(self):
            "Using pympler summarize module to view memory summary."
             
            all_objects = muppy.get_objects()     
            Logger.info("Memory Footprint:")
            Logger.info("-----------------")
            return summary.print_(summary.summarize(all_objects), limit=50)
    
    
if __name__ == "__main__":    
    e = EnvService()
    lc = e.list_constants()
    print lc
    print "Peer port = {}".format(e.get_constant("PEER_PORT"))
    print "Is configs equal: {}".format(e.config_equal(
        e.serialize_stream_conf())
    )
    print "Len of serial config: {}".format(len(e.serialize_stream_conf()))
    
    print e.display_table()
    