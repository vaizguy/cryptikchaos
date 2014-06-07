'''
Created on Dec 14, 2013

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label     import Label
from kivy.uix.button    import Button
from kivy.uix.popup     import Popup


class AboutPopUp(Popup):
    
    def __init__(self, dismiss_cb):
        
        # Init super
        super(AboutPopUp, self).__init__()

        # Set title
        self.title='About'
        
        # Size
        self.size_hint=(0.9, 0.9)
        
        # Pop up dismiss action
        self.bind(on_dismiss=dismiss_cb)

        # information about app label
        about_label = Label(
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
        
        # Bind text size to label
        about_label.bind(size=about_label.setter('text_size')) 
        # set content
        self.content = about_label
               
        # Set pop up size
        #self.size_hint=(0.7, 0.5)

class NavBar(BoxLayout):
    
    def __init__(self, drawer, handleinput_cmd_hook):
        
        # Hooks
        self.handleinput_cmd_hook = handleinput_cmd_hook
        
        # Parent hooks
        self.drawer = drawer
        
        # Init super
        super(NavBar, self).__init__()
                       
        # Set vertical orientation
        self.orientation='vertical'
        
        # Set up label
        title_label = Label(
            text="\n\n[color=999999][b]CryptikChaos[sup]TM[/sup][/b][/color]\n", 
            markup=True, 
            valign='top',
            halign='center'
        )
        # Bind text size to label
        title_label.bind(size=title_label.setter('text_size')) 
        # Set height   
        title_label.size_hint_y = 0.85
        # Bind to parent       
        self.add_widget(title_label)
        
        ## Create popup
        self.about_popup = AboutPopUp(
            dismiss_cb=lambda help_func: self.handleinput_cmd_hook("help")
        )
 
        ## Minimize
        # Set up button
        console_button = Button(text='Console')
        # BG color
        console_button.background_color = [1, 1, 1, 1]
        # Set height
        console_button.size_hint_y = 0.05
        # Set action
        console_button.bind(on_release=self.drawer.toggle_state)
        # Bind to parent
        self.add_widget(console_button) 
              
        ## ABOUT
        # Set up button
        about_button = Button(text='About')
        # BG color
        about_button.background_color = [0, 0, 0, 1]
        # Set height
        about_button.size_hint_y = 0.05
        # Set action
        about_button.bind(on_release=self.action_about)
        # Bind to parent
        self.add_widget(about_button) 
      
        ## EXIT 
        # Set up button
        exit_button = Button(text='Exit')
        # BG color
        exit_button.background_color = [0, 0, 0, 1]   
        # Set height
        exit_button.size_hint_y = 0.05
        # Set action
        exit_button.bind(on_release=self.action_exit)
        # Bind to parent
        self.add_widget(exit_button) 
        
    def action_exit(self, instance):
        
        # Exit app
        self.handleinput_cmd_hook("exit")
        
    def action_about(self, instance):
        
        # Open pop up
        self.about_popup.open()       
        