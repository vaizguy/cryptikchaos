'''
Created on Jun 29, 2014

@author: vaizguy
'''

from kivy.uix.screenmanager import Screen
from kivy.uix.label         import Label

class AboutScreen(Screen):
    
    def __init__(self, **kwargs):
        
        super(Screen, self).__init__(**kwargs)
        
        # information about app label
        self.about_label = Label(
            text="""

[b]CryptikChaos[sup]TM[/sup][/b] is a P2P messenger.

[b]This application is[/b] [i]STILL[/i] [b]experimental[/b].

[i]Developed by vaizlabs.[i]

Get the code:
[i]www.github.com/vaizguy/cryptikchaos[/i]

Contact:
[i]cryptikchaos@googlegroups.com[/i]

""",
            markup=True, 
            valign='top',
            halign='left',
        )  
        
        self.add_widget(self.about_label)
    

    