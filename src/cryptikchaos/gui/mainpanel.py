'''
Created on Jun 29, 2014

@author: vaizguy
'''

from kivy.uix.screenmanager import ScreenManager

from cryptikchaos.gui.screens.consolescreen import ConsoleScreen
from cryptikchaos.gui.screens.aboutscreen import AboutScreen


class MainPanel(ScreenManager):
    
    def __init__(self, greeting, font_type, font_size, 
        handleinput_cmd_hook, getcommands_cmd_hook, **kwargs):
        
        super(ScreenManager, self).__init__(**kwargs)
                               
        self.console_screen = ConsoleScreen(
            greeting=greeting, 
            font_type=font_type, 
            font_size=font_size, 
            handleinput_cmd_hook=handleinput_cmd_hook, 
            getcommands_cmd_hook=getcommands_cmd_hook,
            name="console"
            )
        
        self.about_screen = AboutScreen(name="about")
        
        # Add console - GUI hooks
        self.inputtext_gui_hook=self.console_screen.inputtext_gui_hook
        self.getmaxwidth_gui_hook=self.console_screen.getmaxwidth_gui_hook
        
        # Add console screen widget to main screen manager    
        self.add_widget(self.console_screen)
        # Add about screen
        self.add_widget(self.about_screen)
        
        # Default screen
        self.current = "console"
        
    def goto_console_screen(self):
        
        self.current = "console"
        
    def goto_about_screen(self):
        
        self.current = "about"
        
        
if __name__ == '__main__':
    
    from kivy.app import App
    from cryptikchaos.env.configuration import constants
    
    # Add kivy resource paths
    from kivy.resources import resource_add_path
    resource_add_path(constants.KIVY_RESOURCE_PATH_1)
    resource_add_path(constants.KIVY_RESOURCE_PATH_2)
    print constants.KIVY_RESOURCE_PATH_1
    print constants.KIVY_RESOURCE_PATH_2
    
    
    class ScreenManagerApp(App):
    
        def build(self):
            root =MainPanel(
                greeting="MainPanel Test",
                font_type=constants.GUI_FONT_TYPE,
                font_size=constants.GUI_FONT_SIZE,
                handleinput_cmd_hook=lambda *args, **kwargs:None,
                getcommands_cmd_hook=lambda *args, **kwargs:None        
            )
                       
            return root
        
    ScreenManagerApp().run()
