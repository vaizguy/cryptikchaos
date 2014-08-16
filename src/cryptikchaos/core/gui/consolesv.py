'''
Created on Aug 3, 2014

Code from kivy wiki,
https://github.com/kivy/kivy/wiki/Scrollable-Label

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"

from kivy.uix.rst import RstDocument
from kivy.properties import StringProperty, NumericProperty

from cryptikchaos.core.env.configuration import constants


class  ConsoleScrollView(RstDocument):
       
    text = StringProperty('')
    font_type = StringProperty()
    font_size = NumericProperty()
    
    def display_text(self, text):
        
        self.text += "[color={}]{}[/color]".format(
            constants.GUI_FONT_COLOR,
            text
        )

