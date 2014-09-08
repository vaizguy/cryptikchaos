'''
Created on Jul 21, 2013

Cryptikchaos uses;
kivy - NUI
twisted framework - Async Networking

This file is part of CryptikChaos.

CryptikChaos is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CryptikChaos is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CryptikChaos. If not, see <http://www.gnu.org/licenses/>.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6.1"

import kivy
kivy.require('1.7.2')

# Add cryptikchaos path
import pythonpath
pythonpath.AddSysPath('../../src')
    
from cryptikchaos.core.services import CoreServices


class CryptikChaosApp(CoreServices):

    """
    Main Application class.
    Inherits from GUI service. (gui.service.GUIService)

    """
    
    def __init__(self, **kwargs):

        # Init GUI Service
        super(CryptikChaosApp, self).__init__(**kwargs)
        
    def __del__(self):
        
        #Constructor calls
        super(CryptikChaosApp, self).__del__()
              
        
if __name__ == '__main__':
    
    from cryptikchaos.libs.utilities import run_kivy_app
    run_kivy_app(CryptikChaosApp)
