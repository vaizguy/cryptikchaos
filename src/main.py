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
pythonpath.AddSysPath('../../../src')
pythonpath.AddSysPath('../../src')

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

    def __init__(self):

        # Init GUI Service
        super(CryptikChaosApp, self).__init__()


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
