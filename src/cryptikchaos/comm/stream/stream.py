'''
Created on Dec 8, 2013

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"

import hmac


class Stream:
    
    def __init__(self, uid, flag, stype, content, skey):
        
        self._uid = uid
        self._flag = flag
        self._stype = stype
        self._content = content
        self._skey = skey
        self.dict = {
            'STREAM_FLAG'   : self._flag,
            'STREAM_TYPE'   : self._stype,
            'STREAM_CONTENT': self._content,
            'STREAM_PKEY'   : self._skey,
            'STREAM_CHKSUM' : self._gen_hmac()     
        }
        
    def _gen_hmac(self):
        "Generate stream hmac."
        
        return hmac.new(str(self._flag)+self._stype+self._content+self._uid+self._skey).hexdigest()
    
    def check_hmac(self, uid, flag, stype, content, skey):
        "Check for HMAC integrity"
        
        return hmac.new(str(flag)+stype+content+uid+skey).hexdigest() == self.dict["STREAM_CHKSUM"]
    