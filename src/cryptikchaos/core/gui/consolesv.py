'''
Created on Aug 3, 2014

Code from kivy wiki,
https://github.com/kivy/kivy/wiki/Scrollable-Label

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"

from kivy.properties import StringProperty, NumericProperty

from cryptikchaos.core.gui.rstdocbase import RstDocumentBase


class  ConsoleScrollView(RstDocumentBase):
       
    text = StringProperty('')
    font_type = StringProperty()
    font_size = NumericProperty()

