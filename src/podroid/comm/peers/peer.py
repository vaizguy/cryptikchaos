'''
Created on Aug 3, 2013

@author: vaizguy
'''

class Peer:
    
    
    def __init__(self, pid, host, port):
        
        self._id   = pid
        self._host = host
        self._port = port
        self._connstat = False
        self._connection = None
    
    
    def get_id(self):
        return self._id
    
    
    def get_host(self):
        return self._host
    
    
    def get_port(self):
        return self._port
    
    
    def is_connected(self):
        return self._connstat
    
    
    def get_connection(self):
        return self._connection
    
    
    def add_connection(self, conn):
        
        self._connection = conn
            

    def update_connection_status(self, status):
        
        if status in (True, False):
            self._connstat = status
        else:
            raise Exception("Invalid Peer Connection Status, must be True or False.")

    
        
        