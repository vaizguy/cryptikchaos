'''
Created on Jul 19, 2014

@author: vaizguy
'''

from cryptikchaos.env.configuration import constants

from cryptikchaos.env.service import EnvService
from cryptikchaos.comm.service import CommService

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