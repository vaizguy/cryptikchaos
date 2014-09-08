'''
Created on Aug 19, 2014

This file is part of CryptikChaos.

CryptikChaos is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CryptikChaos is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CryptikChaos. If not, see <http://www.gnu.org/licenses/>.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6.1"

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
    
    def display_text(self, text, clear=False):
        
        if not clear:
            self.text += "[color={}]{}[/color]".format(
                constants.GUI_FONT_COLOR,
                text
            )
        else:
            self.text = "[color={}]{}[/color]".format(
                constants.GUI_FONT_COLOR,
                text
            )            
