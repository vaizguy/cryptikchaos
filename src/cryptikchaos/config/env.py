'''
Created on Oct 19, 2013

View app environment constants through the App.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.3

from cryptikchaos.config.configuration import constants

class EnvService:
    """
    Used to view currently defined environment.
    """
    
    def __init__(self):

        self.env_dict = {}

        # Populate constants
        for attr in dir(constants):
            if attr.isupper():
                self.env_dict[attr] = str(getattr(constants, attr)).encode('string_escape')

    def list_constants(self):
        "List all env constants."
        
        constants = ""
        i = 1
        
        for k in sorted(self.env_dict.keys()):
            constants += "\n[" + str(i) + "] " + k
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
                
if __name__ == "__main__":
    
    e = EnvService()
    print e.list_constants()
    print "Peer port = {}".format(e.get_constant("PEER_PORT"))
    
            