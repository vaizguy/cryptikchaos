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
      
if __name__ == '__main__':
    # Add cryptikchaos path
    import pythonpath
    pythonpath.AddSysPath('.') # ./main.py (pwd: src)
    pythonpath.AddSysPath('../..') # ../../main.py (pwd: test dir)
    
    from cryptikchaos import CryptikChaosApp
    from cryptikchaos.libs.utilities import run_kivy_app
    run_kivy_app(CryptikChaosApp)
