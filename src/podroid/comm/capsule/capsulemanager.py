'''
Created on Aug 4, 2013

@author: vaizguy
'''

from podroid.comm.capsule.capsule import Capsule

class CapsuleManager:
    
    def __init__(self):
        
        self.capsule_dict = {}
        
    def pack_capsule(self, captype='NULL', capcontent='', dest_host='127.0.0.1'):
        
        capsule = Capsule(captype, capcontent, dest_host)
        
        self.capsule_dict[capsule.getid()] = capsule
        
        return capsule.pack()
    
    def unpack_capsule(self, serial):
        
        capsule = Capsule()
        capsule.unpack(serial)
        
        self.capsule_dict[capsule.getid()] = capsule
        
        return capsule.tuple()

        
    def get_capsule(self, cid):
        
        return self.capsule_dict[cid].tuple()
    
