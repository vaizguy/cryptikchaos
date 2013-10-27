'''
Created on Oct 19, 2013

View app environment constants through the App.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.4

from cryptikchaos.config.configuration import constants
from cryptikchaos.libs.utilities import serialize
from cryptikchaos.libs.utilities import deserialize


class EnvService:
    """
    Used to view currently defined environment.
    """
    
    def __init__(self):

        self.env_dict = {}

        # Populate constants
        for attr in dir(constants):
            if attr.isupper():
                self.env_dict[attr] = str(
                    getattr(constants, attr)
                ).encode('string_escape')

    def list_constants(self):
        "List all env constants."
        
        constants = []
        i = 1
        
        for k in sorted(self.env_dict.keys()):
            constants.append( "[" + str(i) + "] " + k )
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
        "Return all the capsule config as dict"
        
        return { 
            fkey : self.env_dict[fkey] for fkey in sorted(
                [k for k in self.env_dict.keys() if k[0:5] == "CAPS_"]
            )
        }
               
    def serialize_caps_conf(self):
        "Serialize capsule configuration."
        
        return serialize(self.caps_conf_dict())
    
    def deserialize_caps_conf(self, serialstr):
        "Deserialize capsule configuration."
        
        return deserialize(serialstr)
    
    def config_equal(self, serialstr):
        """
        Check if recieved capsule configuration matches current
        capsule configuration.
        """
        
        return (
            self.deserialize_caps_conf(serialstr) == self.caps_conf_dict()
        )
        
if __name__ == "__main__":
    
    e = EnvService()
    print e.list_constants()
    print "Peer port = {}".format(e.get_constant("PEER_PORT"))
    print "Is configs equal: {}".format(e.config_equal(
        e.serialize_caps_conf())
    )
    print "Len of serial config: {}".format(len(e.serialize_caps_conf()))
    