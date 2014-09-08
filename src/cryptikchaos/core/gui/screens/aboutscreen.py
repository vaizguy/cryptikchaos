'''
Created on Jun 29, 2014

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

from kivy.uix.screenmanager import Screen

from cryptikchaos.core.env.configuration import constants
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

This is an experimental application and still under development.\n
You can find topics of help under the help_ command.

About
=====
:Home: [i]http://felix-vaizlabs.rhcloud.com[/i]
:Author: Arun Vaidya <vaizguy@gmail.com>
:License: GPLv3
:Code: [i]http://www.github.com/vaizguy/cryptikchaos[/i]
:Groups: [i]cryptikchaos@googlegroups.com[/i]
:UID: {}
:Host: {}
:Platform: {}
:Version: {}\n
--------------\n
""".format( 
           constants.PEER_ID,
           constants.MY_HOST,
           constants.PLATFORM,
           __version__
           ) ,
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
    
    
