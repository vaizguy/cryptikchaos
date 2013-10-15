'''
Created on Oct 8, 2013

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = 0.2

from kivy.app import App

from cryptikchaos.gui.consolewin import ConsoleWindow


class GUIService(App):

    def build(self):

        "Build the kivy App."
        
        root = ConsoleWindow(self.handle_input) ## TODO messy implementation
        
        self.append_text = root.append_text_to_console
        
        return root