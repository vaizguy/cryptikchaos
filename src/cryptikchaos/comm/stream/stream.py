'''
Created on Dec 8, 2013

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"

import hmac


class Stream:
    
    def __init__(self, uid, flag, stype, content, token):
        
        self._uid = uid
        self._flag = flag
        self._stype = stype
        self._content = content
        self._token = token
        
        self.rebuild_dict = self.build_dict

        self.build_dict()
       
    def gen_hmac(self):
        "Generate stream hmac."
        
        return hmac.new(
            str(self._flag)+\
            self._stype+\
            self._content+\
            self._uid+\
            self._token
        ).hexdigest()
    
    def check_hmac(self, stream_hmac):
        "Check for HMAC integrity"
        
        return stream_hmac == self.gen_hmac()
    
    def update_content(self, content):
        
        self._content = content
        self.rebuild_dict()

    def build_dict(self):
        
        self.dict = {
            'STREAM_FLAG'   : self._flag,
            'STREAM_TYPE'   : self._stype,
            'STREAM_CONTENT': self._content,
            'STREAM_PKEY'   : self._token,
        }
        