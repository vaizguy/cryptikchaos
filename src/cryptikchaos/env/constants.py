"""
Constant types in Python.
"""
__doc__ = """
This is a variation on "Constants in Python" by Alex Martelli, from which the
solution idea was borrowed, and enhanced according suggestions of Zoran Isailovski.

In Python, any variable can be re-bound at will -- and modules don't let you
define special methods such as an instance's __setattr__ to stop attribute
re-binding. Easy solution (in Python 2.1 and up): use an instance as "module"...

In Python 2.1 and up, no check is made any more to force entries in sys.modules
to be actually module objects. You can install an instance object there and take
advantage of its attribute-access special methods (e.g., as in this snippet, to
prevent type rebindings. 

Usage:
  import consttype
  consttype.magic = 23    # Bind an attribute to a type ONCE
  consttype.magic = 88    # Re-bind it to a same type again
  consttype.magic = "one" # But NOT re-bind it to another type: this raises consttype._ConstError
  del consttype.magic     # Remove an named attribute
  consttype.__del__()     # Remove all attributes
"""


class _constants:
    "Code taken from Alex Martelli's python constant recipe."

    # ConstError Exception class
    class ConstError(TypeError):
        pass
    
    def __repr__(self):
        
        return "Constant()"

    # Prevent changing of constant once set.
    def __setattr__(self, name, value):

        if name != name.upper():
            raise self.ConstError("Name of constant should be upper case.")

        if self.__dict__.has_key(name):
            raise self.ConstError, "Can't rebind constant {}".format(name)
        else:
            self.__dict__[name] = value
            
    def __setitem__(self, name, value):
        
        return self.__setattr__(name, value)

    def __delattr__(self, name):

        if self.__dict__.has_key(name):
            raise self.ConstError("Can't delete constant {}".format(name))

import sys
# Save reference to module
ref = sys.modules['__main__'] 
# overwrite module reference
sys.modules[__name__] = _constants()

if __name__ == "__main__":
    import constants
    
    constants.TEST = "REBIND TEST PASS"
    try:
        constants.TEST = "REBIND TEST FAIL"
    except constants.ConstError:
        pass

    print constants.TEST