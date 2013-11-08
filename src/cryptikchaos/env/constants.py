'''
Created on Aug 5, 2013

@author: Alex Martelli
'''


class _constant:
    "Code taken from Alex Martelli's python constant recipe."

    # ConstError Exception class
    class ConstError(TypeError):
        pass

    # Prevent changing of constant once set.
    def __setattr__(self, name, value):

        if name != name.upper():
            raise self.ConstError("Name of constant should be upper case.")

        if name in self.__dict__:
            raise self.ConstError("Can't rebind constant {}".format(name))
        else:
            self.__dict__[name] = value

    def __delattr__(self, name):

        if name in self.__dict__:
            raise self.ConstError("Can't delete constant {}".format(name))

import sys
# Save reference to module
ref = sys.modules['__main__'] 
# overwrite module reference
sys.modules[__name__] = _constant()
