'''
Created on Jun 29, 2014

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"

from kivy.uix.screenmanager import Screen

from cryptikchaos.core.gui.rstdocbase import RstDocumentBase


class AboutScreen(Screen):

    def __init__(self, **kwargs):

        super(Screen, self).__init__(**kwargs)

        # information about app label
        self.about_label = RstDocumentBase(
            text="""
CryptikChaos[sup]TM[/sup] [i]is a work in progress![i]
=======================================================

.. NOTE:: [i]"..and the G33K_ shall inherit the earth."[/i]

This is an experimental application and still under development.
You can find topics of help under the help_ command.

About
=====
:Home: [i]http://felix-vaizlabs.rhcloud.com[/i]
:Author: Arun Vaidya <vaizguy@gmail.com>
:License: GPLv3
:Code: [i]http://www.github.com/vaizguy/cryptikchaos[/i]
:Groups: [i]cryptikchaos@googlegroups.com[/i]

""" ,
            markup=True,
            valign='top',
            halign='left',
        )
        
        self.add_widget(self.about_label)

if __name__ == '__main__':
    
    from kivy.app import App
    
    class AboutLabelPreviewApp(App):
        
        def build(self):
            return AboutScreen()
        
    A = AboutLabelPreviewApp()
    A.run()
    
    
