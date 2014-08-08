'''
Created on Jul 21, 2013

Cryptikchaos is a peer to peer application using;
kivy - NUI
twisted framework - Async Networking

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"

import kivy
kivy.require('1.7.2')

# Add cryptikchaos path
import pythonpath
pythonpath.AddSysPath('../../src')
    
from cryptikchaos.gui.service import GUIService


class CryptikChaosApp(GUIService):

    """
    Main Application class.
    Inherits from GUI service. (gui.service.GUIService)

    """
    
    def __init__(self):

        # Init GUI Service
        super(CryptikChaosApp, self).__init__()
              
        
if __name__ == '__main__':
    
    from cryptikchaos.libs.utilities import run_kivy_app
    run_kivy_app(CryptikChaosApp)
