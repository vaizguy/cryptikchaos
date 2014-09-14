'''
Created on Jul 21, 2013

+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
   __                                _ _  __  ___
  /  \  ____.  _^_   ____  __.__ _*_  |  /   /    _     _  .___.  .___  .___.
 /      |    \  |   |    \   |    |   | /   /      |   |   |   |  |   | |   \
/       |____/  |   |____/   |    |   |/___/       |   |   |   |  |   | |
\       |\      |   |        |    |   |\   \       |-+-|   |-+-|  | 0 | |___.
 \      | \     |   |        |    |   | \   \      |   |   |   |  |   |     |
  \__/ _|  \_. _|_ _|        |   _|_ _|_ \__ \___ _|   |_ _|   |_ |___| /___|

+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

The Cryptikchaos program is an attempt to create a command line interface
providing various functionalities including peer to peer communications using
the `twisted framework <https://twistedmatrix.com>` with asynchronous I/O using
the `kivy NUI <www.kivy.org>` ;

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
__license__ = "GNU GPLv3"

# Minimum requirements;
import kivy 
kivy.require('1.7.2')

from kivy.logger import Logger

import atexit
@atexit.register
def on_close():
    Logger.info("MAIN APP: Exiting python.")

def main():
    # Add cryptikchaos path
    import pythonpath
    pythonpath.AddSysPath('.') # ./main.py (pwd: src)
    pythonpath.AddSysPath('../..') # ../../main.py (pwd: test dir)
    
    try:
        from cryptikchaos.app import CryptikChaosApp
    except KeyboardInterrupt:
        Logger.error("MAIN APP: Cryptikchaos services was interrupted.")
    else:
        from cryptikchaos.libs.utilities import run_kivy_app
        run_kivy_app(CryptikChaosApp)

        
if __name__ == '__main__':
    main()
        
