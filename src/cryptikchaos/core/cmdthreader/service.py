'''
Created on Sep 7, 2014

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

from threading import Thread, Event
from time import sleep
from kivy import Logger
from collections import deque


class CMDThreaderService(Thread):
    "Execute console commands in parallel thread."
    
    def __init__(self):
        
        super(CMDThreaderService, self).__init__()
        # deck that holds the commands
        self._cmd_deck = deque()
        # Set to stop event
        self.stop = Event()
        Logger.debug("CMDTHREADER: Starting Thread {}.".format(id(self)))
        # CMD status updater
        self._gui_service = None
        self.cmdprog_gui_hook = None
        
    def register_gui_service(self, gui_service):
               
        if not self._gui_service:
            self._gui_service = gui_service
            self.cmdprog_gui_hook = self._gui_service.cmdprog_gui_hook
        
    def exec_cmd(self, command):
        
        self._cmd_deck.appendleft(command)
        
    def is_empty(self):
        
        return bool(self._cmd_deck)
        
    def run(self):
                            
        if not self._gui_service:
            Logger.warn("CMDTHREADER: No GUI service registered.")
                
        while(not self.stop.is_set()):
           
            if self._cmd_deck:
                                
                # get number of commands
                cmd_cnt = len(self._cmd_deck)
                
                # Get command and arguments
                cmd = self._cmd_deck.pop()
                
                # Update command exec progress
                if self._gui_service:
                    if cmd_cnt-1 == 0:
                        self.cmdprog_gui_hook(
                            500) if self.cmdprog_gui_hook else None
                    else:
                        self.cmdprog_gui_hook(
                            1000*((1)/cmd_cnt)) if self.cmdprog_gui_hook else None
                
                Logger.debug("CMDTHREADER: Executing command -> {}".format(cmd))
                # Execute command
                cmd()
                
                if self._gui_service:
                    if cmd_cnt-1 == 0:
                        self.cmdprog_gui_hook(1000) if self.cmdprog_gui_hook else None
          
            else:
                sleep(2)
                # Reset progress
                if self._gui_service:
                    self.cmdprog_gui_hook(0) if self.cmdprog_gui_hook else None
                
    def on_stop(self):
        
        Logger.debug("CMDTHREADER: Exiting Thread {}.".format(id(self)))
        # Set stop event
        self.stop.set()
                
if __name__ == '__main__':
    from functools import partial    
    cmd_t = CMDThreaderService()
    cmd_t.start()
    
    def printer(msg):
        print msg
    
    try_1 = partial(printer, "func 1")
    try_2 = partial(printer, "func 2")
    cmd_t.exec_cmd(try_1)
    cmd_t.exec_cmd(try_2)
    
    # For testing purpose we wait for commands to execute before
    # closing the thread
    while(True):
        if not cmd_t.is_empty():
            cmd_t.on_stop()
            sleep(1)
            exit(0)