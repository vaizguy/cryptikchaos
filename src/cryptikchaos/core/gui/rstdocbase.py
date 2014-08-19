'''
Created on Aug 19, 2014

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"

from kivy.uix.rst import RstDocument
from kivy.properties import DictProperty

from cryptikchaos.core.env.configuration import constants

if constants.PLATFORM_ANDROID:
    bg_color = "0A0A0A"
    link_color = "ce5c00"
    para_color = "E6E3E3"
    title_color = "204a87"
    bullet_color = "000000"
else:
    bg_color = "2E2E2E"
    link_color = "ce5c00"
    para_color = "E6E3E3"
    title_color = "204a87"
    bullet_color = "000000"

    
class RstDocumentBase(RstDocument):
    
    colors = DictProperty({
        'background': bg_color,
        'link': link_color,
        'paragraph': para_color,
        'title': title_color,
        'bullet': bullet_color}
    )
    
    def display_text(self, text):
        
        self.text += "[color={}]{}[/color]".format(
            constants.GUI_FONT_COLOR,
            text
        )