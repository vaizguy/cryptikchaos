'''
Created on Jul 19, 2014

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"

from kivy.logger import Logger

from cryptikchaos.core.env.configuration import constants

from cryptikchaos.core.env.service import EnvService
from cryptikchaos.core.comm.service import CommService
from cryptikchaos.core.parser.service import ParserService


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
        
        # Initiate Lexical parser service
        self.parser_service = ParserService(
            cmd_aliases = constants.CMD_ALIASES 
        )
        
    def __del__(self):
        
        Logger.info("Closing services.")  

        self.comm_service.__del__()
        self.env_service.__del__()
        self.parser_service.__del__()
        
        Logger.info("Successfully closed services.")