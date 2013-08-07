'''
Created on Aug 5, 2013

@author: Alex Martelli
'''

## Code taken from Alex Martelli's python constant recipe.
class _const:
    
    ## ConstError Exception class
    class ConstError(TypeError): pass
    
    ## Prevent changing of constant once set.
    def __setattr__(self,name,value):
        
        if name != name.upper():
            raise self.ConstError, "Name of constant should be upper case."          
        
        if self.__dict__.has_key(name):
            raise self.ConstError, "Can't rebind constant {}".format(name)
        else:
            self.__dict__[name]=value
            
    def __delattr__(self,name):
        
        if self.__dict__.has_key(name):
            raise self.ConstError, "Can't delete constant {}".format(name)
        
        
import sys
sys.modules[__name__]=_const()