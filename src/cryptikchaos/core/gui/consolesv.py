'''
Created on Aug 3, 2014

Code from kivy wiki,
https://github.com/kivy/kivy/wiki/Scrollable-Label

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"

from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty

from cryptikchaos.core.env.configuration import constants

Builder.load_string('''
<ConsoleScrollView>:
    label_w: labelWindow
    size_hint_y: 0.9
    do_scroll_y: True
    
    Label:
        id: labelWindow
        size_hint_y: None
        height: self.texture_size[1]
        text_size: self.width, None
        markup: True
        shorten: True
        text: root.text
        font_name: root.font_type
        font_size: root.font_size
        
        canvas.before:
            Color: 
                rgba: 0, 0, 0, 1
            Rectangle:
                pos: self.pos
                size: self.size
''')


class  ConsoleScrollView(ScrollView):
       
    text = StringProperty('')
    label_w = ObjectProperty()
    font_type = ObjectProperty()
    font_size = ObjectProperty()
    
    def display_text(self, text):
        
        self.label_w.text += "[color={}]{}[/color]".format(
            constants.GUI_FONT_COLOR,
            text
        )

