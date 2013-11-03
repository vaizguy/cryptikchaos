'''
Created on Nov 3, 2013

@author: vaizguy
'''

from cryptikchaos.libs.Storage.store import Store
from cryptikchaos.libs.Table.prettytable import PrettyTable

from hashlib import md5

class StoreManager(object):
    
    def __init__(self, name, keys):
        
        self._storage = {}
        self._name = name
        self._store_keys = keys
            
    def __str__(self):
        
        return str(self._storage)
    
    def __repr__(self):
        
        return "StoreManager({})".format(
            md5(self._storage).hexdigest()
        )
    
    def keys(self):
        
        return self._storage.keys()
            
    def add_store(self, sid, dictionary={}):
        
        self._storage[sid] = Store(self._store_keys, dictionary)
        
    def delete_store(self, sid):
        
        if sid in self._storage.keys():
            del self._storage[sid]
        else:
            return None
        
    def get_store(self, sid):
        
        if sid in self._storage:
            return self._storage[sid]
        else:
            return None
        
    def set_store_item(self, sid, key, value):
        
        if sid in self._storage:
            _dict = self._storage[sid]
            _dict[key] = value
            self._storage[sid] = _dict
        else:
            return None
        
    def get_store_item(self, sid, key):
        
        if sid in self._storage:
            _dict = self._storage[sid]
            return _dict[key]
        else:
            return None            
        
    def display_store(self):
        
        print "\n{} Storage Table".format(self._name) 
        
        table = PrettyTable(["ID"] + self._store_keys)

        for sid in self._storage.keys():      
                       
            row = [sid] + self._storage[sid].keys()
                      
            table.add_row(row)
                
        print table
            
            
if __name__ == "__main__":
    
    keys = ["key1", "key2", "key3"]
    
    sm = StoreManager("StoreTest", keys)
    
    sm.add_store(1, {"key1": 1, "key2": 2, "key3": 3})
    sm.add_store(2, {"key1": 4, "key2": 5, "key3": 6})
    sm.add_store(3, {"key1": 7, "key2": 8, "key3": 9})
    sm.add_store(4, {"key1": 'a', "key2": 'b', "key3": 'c'})
    
    sm.display_store()
