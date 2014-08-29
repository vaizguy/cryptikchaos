'''
Created on Oct 19, 2013

View app environment constants through the App.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6.1"

import ConfigParser

from cryptikchaos.core.env.configuration import constants
from cryptikchaos.core.env import constants as const
from cryptikchaos.libs.utilities import serialize
from cryptikchaos.libs.utilities import deserialize

from cryptikchaos.libs.Table.restTable import restTable

from kivy import Logger

if constants.PYMPLER_AVAILABLE:
    from pympler import summary, muppy, tracker, refbrowser


class EnvService(object):

    """
    Used to view currently defined environment.
    """

    def __init__(self):

        # Check and see if constants rebinding is unsuccessful
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
                
        # Initiate memory tracker
        if constants.PYMPLER_AVAILABLE:
            self.mem_tracker = tracker.SummaryTracker()

    def __del__(self):

        Logger.info("Closing Environment service.")

    def list_constants(self, shorten=True):
        "List all env constants."

        constants = []
        i = 1

        for k in sorted(self.env_dict.keys()):
            v = self.env_dict[k].strip() 

            if len(v[:50]) < 50:
                constants.append(
                    (i, k, v)
                )
            elif shorten:
                constants.append(
                    (i, k,v[:50])
                )
            else:
                constants.append(
                    (i, k, v)
                )

            i += 1

        return constants
    
    def dump_config(self):
        
        # Start config parser
        config = ConfigParser.SafeConfigParser()
        
        # Set env constants into section
        config.add_section('Environment')
        for (k, v) in self.env_dict.iteritems():
            if '%' not in v:
                print k
                config.set('Environment', k, v.encode('string_escape'))
            
        # Writing our configuration file to 'defaults.cfg'
        with open('{}/core/env/defaults.cfg'.format(constants.PROJECT_PATH), 'wb') as configfile:
            config.write(configfile)
            Logger.info("Dumped environment to config file.")
    
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
            fkey: self.env_dict[fkey] for fkey in sorted(
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
            table = restTable(["S.NO", "CONSTANT", "VALUE"])

            for c in constants:
                table.add_row(c)

            return """
Environment Constants:\n
To see value use: 'eko <constant name>'\n
\n{}

""".format(table)
        else:
            return "No environment variables defined."

    # pympler inline memory profiler code
    if constants.PYMPLER_AVAILABLE:
        def memory_summary(self, summarize=True):
            "Using pympler summarize module to view memory summary."
            
            if summarize:
                all_objects = muppy.get_objects()
                Logger.info("Memory Footprint:")
                Logger.info("-----------------")
                return summary.print_(summary.summarize(all_objects), limit=50)
            else:
                Logger.info("Memory Tracker:")
                Logger.info("---------------")
                self.mem_tracker.print_diff()        
               
                
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
    e.dump_config()
