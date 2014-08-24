'''
Created on Aug 3, 2014

Code from kivy wiki,
https://github.com/kivy/kivy/wiki/Scrollable-Label

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6.1"

from kivy.properties import StringProperty

from cryptikchaos.core.gui.rstdocbase import RstDocumentBase


class  ConsoleScrollView(RstDocumentBase):
       
    text = StringProperty('')


