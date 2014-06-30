'''
Created on Jun 29, 2014

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"

from kivy.uix.screenmanager import Screen
from kivy.uix.label         import Label

class AboutScreen(Screen):
    
    def __init__(self, **kwargs):
        
        super(Screen, self).__init__(**kwargs)
        
        # information about app label
        self.about_label = Label(
            text="""

[b]CryptikChaos[sup]TM[/sup][/b] is still experimental!!

[b]This application [/b] [i]will be[/i] [b]AWESOME!![/b]

[i]Under development, vaizlabs.[i]

Get the code,
[i]www.github.com/vaizguy/cryptikchaos[/i]

Thoughts?
[i]cryptikchaos@googlegroups.com[/i]

""",
            markup=True, 
            valign='top',
            halign='left',
        )  
        
        self.add_widget(self.about_label)
    

    