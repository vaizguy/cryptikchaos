'''
Created on Jul 21, 2013

@author: vaizguy
'''
import hmac
import struct

class Capsule(object):
    
        def __init__(self, captype='NULL', content=''):
            
            if len(content) > 40:
                raise Exception('OverflowError: Content exceeded capsule limit of 40')
            
            self._dictionary = {'CAP_TYPE'    : captype,
                                'CAP_CONTENT' : content,
                                'CAP_CHKSUM'  : hmac.new(content).hexdigest()    }
            
            
        def __setitem__(self, key, item):
            
                if key not in self._dictionary:
                    raise KeyError("The key '{}' is not defined.".format(key))
                
                self._dictionary[key] = item
                
                
        def __getitem__(self, key):
            
            return self._dictionary[key]
        
        def pack(self):
            
            l = len(self._dictionary['CAP_CONTENT'])
            return struct.pack("!4sL32s40s", self._dictionary['CAP_TYPE'], l, self._dictionary['CAP_CHKSUM'], self._dictionary['CAP_CONTENT'] )
        
        def unpack(self, stream):
            
            (self._dictionary['CAP_TYPE'], length, self._dictionary['CAP_CHKSUM'], self._dictionary['CAP_CONTENT']) = struct.unpack("!4sL32s40s", stream)
            self._dictionary['CAP_CONTENT'] = self._dictionary['CAP_CONTENT'][:length]
            
        def __str__(self):
            
            return self._dictionary['CAP_TYPE'] + ':' + str(len(self._dictionary['CAP_CONTENT'])) + ':' +  self._dictionary['CAP_CHKSUM'] + ':' + self._dictionary['CAP_CONTENT']
            
            
if __name__ == '__main__':
    
    Ctx = Capsule('TEST', 'This is a capsule test.')
    pkd = Ctx.pack()
    print 'Packed data is :', pkd
    Crx = Capsule() 
    Crx.unpack(pkd)      
    print "Unpacked data :", str(Crx)
        