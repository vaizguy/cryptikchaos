'''
Created on Jul 21, 2013

Cryptikchaos is a peer to peer application using;
kivy - NUI
twisted framework - Async Networking

main.py is the kivy app entry file.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"

import atexit
from kivy.logger import Logger

@atexit.register
def on_close():
    Logger.info("Exiting python.")

def main():
    # Add cryptikchaos path
    import pythonpath
    pythonpath.AddSysPath('.') # ./main.py (pwd: src)
    pythonpath.AddSysPath('../..') # ../../main.py (pwd: test dir)
    
    try:
        from cryptikchaos import CryptikChaosApp
    except KeyboardInterrupt:
        Logger.error("Cryptikchaos services was interrupted.")
    except ImportError:
        Logger.error("Please check if the package `cryptikchaos.CryptikChaosApp` exists.")
    else:
        from cryptikchaos.libs.utilities import run_kivy_app
        run_kivy_app(CryptikChaosApp)

        
if __name__ == '__main__':
    main()
        
