'''
Created on Sep 7, 2014

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
        # Start thread
        self.start()
        
    def exec_cmd(self, command):
        
        self._cmd_deck.appendleft(command)
        
    def is_empty(self):
        
        return bool(self._cmd_deck)
        
    def run(self):
        
        while(not self.stop.is_set()):
           
            if self._cmd_deck:
                # Get command and arguments
                cmd = self._cmd_deck.pop()
                
                Logger.debug("CMDTHREADER: Executing command -> {}".format(cmd))
                # Execute command
                cmd()
                
            else:
                sleep(2)
                
    def on_stop(self):
        
        Logger.debug("CMDTHREADER: Exiting Thread {}.".format(id(self)))
        # Set stop event
        self.stop.set()
                
if __name__ == '__main__':
    from functools import partial    
    cmd_t = CMDThreaderService()
    
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