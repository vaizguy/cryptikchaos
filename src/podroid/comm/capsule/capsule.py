'''
Created on Jul 21, 2013

@author: vaizguy
'''
import hmac
import struct
import uuid
import socket

from podroid.config.configuration import *

class Capsule(object):
    
        def __init__(self, captype='NULL', content='', dest_host='127.0.0.1'):
            
            if len(content) > constants.CAPS_CONTENT_LEN:
                raise Exception('OverflowError: Content exceeded capsule limit of 40')
            if len(captype) > constants.CAPS_TYPE_LEN:
                raise Exception('OverflowError: Type exceeded capsule limit of 4')
            if dest_host == "localhost":
                dest_host = constants.LOCAL_TEST_HOST            
            
            self._dictionary = {'CAP_ID'      : str( uuid.uuid5(uuid.NAMESPACE_URL, dest_host) )[0:constants.CAPS_ID_LEN],
                                'CAP_DESTIP'  : self._ip_to_uint32(dest_host),
                                'CAP_TYPE'    : captype.upper(),
                                'CAP_CONTENT' : content,
                                'CAP_LEN'     : len(content),
                                'CAP_CHKSUM'  : hmac.new(content).hexdigest()    }
            
            
        def __setitem__(self, key, item):
            
                if key not in self._dictionary:
                    raise KeyError("The key '{}' is not defined.".format(key))
                
                self._dictionary[key] = item
                
                
        def __getitem__(self, key):
            
            return self._dictionary[key]
        
        def pack(self):
            
            return struct.pack("!8sI4s40sL32s", 
                               self._dictionary['CAP_ID'], 
                               self._dictionary['CAP_DESTIP'],                               
                               self._dictionary['CAP_TYPE'], 
                               self._dictionary['CAP_CONTENT'], 
                               self._dictionary['CAP_LEN'], 
                               self._dictionary['CAP_CHKSUM'] )
        
        
        def unpack(self, stream):
            
            (self._dictionary['CAP_ID'], 
             self._dictionary['CAP_DESTIP'],                                            
             self._dictionary['CAP_TYPE'], 
             self._dictionary['CAP_CONTENT'], 
             self._dictionary['CAP_LEN'], 
             self._dictionary['CAP_CHKSUM']) = struct.unpack("!8sI4s40sL32s", stream)
                          
            
        def __str__(self):
            
            string=''
            
            for (k, v) in self._dictionary.iteritems():
                string += str(v) + ':'
                
            return string.strip(':')
                
        
        def getid(self):
            
            return self._dictionary['CAP_ID']
        
        def getip(self):
            
            return self._uint32_to_ip(self._dictionary['CAP_DESTIP'])
        
        def gettype(self):
            
            return self._dictionary['CAP_TYPE']
        
        def tuple(self):
            
            return (self._dictionary['CAP_ID'], 
                    self.getip(),
                    self._dictionary['CAP_TYPE'], 
                    self._dictionary['CAP_CONTENT'][0:self._dictionary['CAP_LEN']], 
                    self._dictionary['CAP_LEN'], 
                    self._dictionary['CAP_CHKSUM'])
        
        def _ip_to_uint32(self, ip):
            t = socket.inet_aton(ip)
            return struct.unpack("!I", t)[0]
        
        def _uint32_to_ip(self, ipn):
            t = struct.pack("!I", ipn)
            return socket.inet_ntoa(t)
    
            
if __name__ == '__main__':
    
    Ctx = Capsule('TEST', 'This is a capsule test.')
    pkd = Ctx.pack()
    print 'Packed data is :', pkd
    Crx = Capsule() 
    Crx.unpack(pkd)      
    print "Unpacked data :", Crx.tuple()
        