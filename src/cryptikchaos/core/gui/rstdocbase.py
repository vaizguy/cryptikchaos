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
        'background': constants.RSTDOC_BG_COLOR,
        'link': constants.RSTDOC_LINK_COLOR,
        'paragraph': constants.RSTDOC_PARA_COLOR,
        'title': constants.RSTDOC_TITLE_COLOR,
        'bullet': constants.RSTDOC_BULLET_COLOR}
    )
    
    def display_text(self, text):
        
        self.text += "[color={}]{}[/color]".format(
            constants.GUI_FONT_COLOR,
            text
        )
