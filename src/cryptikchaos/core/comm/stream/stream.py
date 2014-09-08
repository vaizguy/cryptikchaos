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


class Stream:

    def __init__(self, uid, flag, stype, content, token):

        self._uid = uid
        self._flag = flag
        self._stype = stype
        self._content = content
        self._token = token
        self.dict = {
            'STREAM_FLAG': self._flag,
            'STREAM_TYPE': self._stype,
            'STREAM_CONTENT': self._content,
            'STREAM_PKEY': self._token,
        }
