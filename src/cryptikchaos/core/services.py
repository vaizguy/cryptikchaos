'''
Created on Jul 19, 2014

@author: vaizguy
'''

from cryptikchaos.core.env.configuration import constants

from cryptikchaos.core.env.service import EnvService
from cryptikchaos.core.comm.service import CommService

class CoreServices:
    
    def __init__(self, my_host, print_message):
        
        # Initiate communication service
        self.comm_service = CommService(
            peerid=constants.PEER_ID,
            host=my_host,
            port=constants.PEER_PORT,
            printer=print_message
        )
        
        # Initiate environment service
        self.env_service = EnvService()
        
    def __del__(self):
        
        self.comm_service.__del__()
        self.env_service.__del__()