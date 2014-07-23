'''
Created on Nov 3, 2013

@author: vaizguy
'''

from kivy.logger import Logger

from cryptikchaos.libs.Storage.store import Store
from cryptikchaos.libs.Table.prettytable import PrettyTable

from hashlib import md5


class StoreManager(object):

    def __init__(self, name, valid_keys):
        "Initialize store manager."

        Logger.info("Opening [{}] store manager.".format(
            name
        )
        )

        # Store attributes
        self._storage = {}
        self._name = name
        self._store_keys = valid_keys

    def __str__(self):
        "Store as string."

        return str(self._storage)

    def __repr__(self):
        "Store representation."

        return "StoreManager({})".format(
            md5(self._storage).hexdigest()
        )

    def __del__(self):
        "Delete store contents"

        try:
            del self._name
            del self._storage
            del self._name
            del self._store_keys
        except:
            pass

    def keys(self):
        "Return the storage index keys."

        return self._storage.keys()

    def in_store(self, sid):
        "Check if store id exists."

        return sid in self.keys()

    def add_store(self, sid, dictionary):
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
        "Set item in existing store."

        try:
            _dict = self._storage[sid]
        except KeyError:
            raise Exception(
                "Store needs to be created before being modified."
            )
        else:
            _dict[key] = value
            self._storage[sid] = _dict

    def get_store_item(self, sid, key):
        "Return item from store."

        if self.in_store(sid):
            _dict = self._storage[sid]
            return _dict[key]
        else:
            return None

    def storage_table(self):
        "Display Store in table format."

        if not self._storage.keys():
            return None

        table = PrettyTable(["ID"] + list(self._store_keys))

        for sid in self._storage.keys():

            row = [sid]

            _dict = self._storage[sid]

            for k in _dict.keys():
                # get value
                v = _dict[k]
                # Check on length
                if (len(str(v)) <= 8):
                    row += [v]
                else:
                    row += ["{}..".format(v[:8])]

            table.add_row(row)

        return table

    def get_store_hmac(self, sid):
        "Get stores checksum"

        return self._storage[sid].hmac()

    def check_hmac(self, sid, hmac):
        "Validate store checksum"

        return self._storage[sid].check_hmac(hmac)


if __name__ == "__main__":

    k = ["key1", "key2", "key3"]

    sm = StoreManager("StoreTest", k)

    sm.add_store(1, {"key1": 1, "key2": 2, "key3": 3})
    sm.add_store(2, {"key1": 4, "key2": 5, "key3": 6})
    sm.add_store(3, {"key1": 7, "key2": 8, "key3": 9})
    sm.add_store(4, {"key1": 'a', "key2": 'b', "key3": 'c'})
    print sm

    print sm.storage_table()
