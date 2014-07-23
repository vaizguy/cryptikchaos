'''
Created on Dec 8, 2013

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"


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
