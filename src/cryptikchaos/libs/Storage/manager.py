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
        "Store as string."
        
        return str(self._storage)
    
    def __repr__(self):
        "Store representation."
        
        return "StoreManager({})".format(
            md5(self._storage).hexdigest()
        )
    
    def keys(self):
        "Return the storage index keys."
        
        return self._storage.keys()
    
    def in_store(self, sid):
        "Check if store id exists."
        
        return sid in self.keys()
            
    def add_store(self, sid, dictionary={}):
        "Add a new store."
        
        self._storage[sid] = Store(self._store_keys, dictionary)
        
    def delete_store(self, sid):
        "Delete store."
        
        if self.in_store(sid):
            del self._storage[sid]
        else:
            return None
        
    def get_store(self, sid):
        "Return the store."
        
        if self.in_store(sid):
            return self._storage[sid]
        else:
            return None
        
    def set_store_item(self, sid, key, value):
        "Set item in store."
      
        if self.in_store(sid):
            _dict = self._storage[sid]
            _dict[key] = value
            self._storage[sid] = _dict
        else:
            return None
        
    def get_store_item(self, sid, key):
        "Return item from store."
        
        if self.in_store(sid):
            _dict = self._storage[sid]
            return _dict[key]
        else:
            return None            
        
    def storage_table(self):
        "Display Store in table format."
        
        print "\n{} Storage Table".format(self._name) 
        
        table = PrettyTable(["ID"] + list(self._store_keys))

        for sid in self._storage.keys():   
            
            row = [sid]
            
            _dict = self._storage[sid]
            
            for k in _dict.keys():
                # get value
                v = _dict[k]
                # Check on length
                if len(str(v)) <= 15:
                    row += [_dict[k]]
                else:
                    row += ["{}XXX".format(v[:10])]
                      
            table.add_row(row)
                
        return table
            
            
if __name__ == "__main__":
    
    keys = ["key1", "key2", "key3"]
    
    sm = StoreManager("StoreTest", keys)
    
    sm.add_store(1, {"key1": 1, "key2": 2, "key3": 3})
    sm.add_store(2, {"key1": 4, "key2": 5, "key3": 6})
    sm.add_store(3, {"key1": 7, "key2": 8, "key3": 9})
    sm.add_store(4, {"key1": 'a', "key2": 'b', "key3": 'c'})
    print sm
    
    print sm.storage_table()
