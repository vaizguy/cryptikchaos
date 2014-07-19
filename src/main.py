'''
Created on Jul 21, 2013

Cryptikchaos is a peer to peer chat application using kivy as the
frontend and twisted framework as the backend.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"

import kivy
kivy.require('1.7.2')

# Add cryptikchaos path
import pythonpath
pythonpath.AddSysPath('.')

from cryptikchaos.core.env.configuration import constants
from cryptikchaos.gui.service import GUIService

from kivy.logger import Logger


class CryptikChaosApp(
    # GUI service
    GUIService,  
):

    """
    Main Application class.
    Inherits from GUI service. (gui.service.GUIService)

    """
   
    # Peer host (by default is localhost)
    if constants.ENABLE_TEST_MODE:
        my_host = constants.LOCAL_TEST_HOST
    else:
        my_host = constants.PEER_HOST
        
    def __init__(self):
        
        # Init GUI Service
        super(CryptikChaosApp, self).__init__()
          
    def build(self):
        "Build the kivy App."
                
        # If not in test mode get LAN IP
        if not constants.ENABLE_TEST_MODE:
            self.my_host = constants.PEER_HOST

        return super(CryptikChaosApp, self).build()
           

if __name__ == '__main__':

    try:
        # Build App interface
        App = CryptikChaosApp()    
        # Start App mainloop
        App.run()
    except KeyboardInterrupt:
        Logger.info("Recieved Keyboard interrupt. [CTRL+C]")
        # Stop services
        App.on_stop()
    else:
        Logger.info("Closed Cryptikchaos Client.")
        

