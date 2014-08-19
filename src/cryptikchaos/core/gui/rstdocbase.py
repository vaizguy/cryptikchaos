'''
Created on Aug 19, 2014

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"

from kivy.uix.rst import RstDocument
from kivy.properties import DictProperty

from cryptikchaos.core.env.configuration import constants


class RstDocumentBase(RstDocument):
    
    colors = DictProperty({
        'background': "2E2E2E",
        'link': 'ce5c00',
        'paragraph': 'E6E3E3',
        'title': '204a87',
        'bullet': '000000'}
    )
    
    def display_text(self, text):
        
        self.text += "[color={}]{}[/color]".format(
            constants.GUI_FONT_COLOR,
            text
        )