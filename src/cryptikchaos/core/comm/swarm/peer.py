'''
Created on Dec 8, 2013

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


class Peer:

    def __init__(self, pid, key, host, port):

        self._pid = pid
        self._key = key
        self._host = host
        self._port = port
        self.dict = {
            "PEER_ID": self._pid,
            "PEER_KEY": self._key,
            "PEER_IP": self._host,
            "PEER_PORT": self._port,
            "PEER_STATUS": False,
            "PEER_COLOR": self._pid
        }
