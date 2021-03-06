'''
Created on Nov 3, 2013

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

from cryptikchaos.libs.customtypes import TransformedDict
from cryptikchaos.libs.utilities import md5hash
import hmac
import exceptions


class Store(TransformedDict):

    "custom store"

    def __init__(self, keys, dictionary):
        "Initialize dictionary."

        # autherized keys
        self._valid_keys = keys

        # Init parent
        super(Store, self).__init__(**dictionary)

    def __str__(self):
        "String equivalent."

        return TransformedDict.__str__(self)

    def __repr__(self):
        "Object representation as string."

        return "Store({})".format(TransformedDict.__repr__(self))

    def __dict__(self):
        "Return dictionary obj"

        return TransformedDict.__dict__()

    def __getitem__(self, key):
        "Get value from dictionary."

        # Get item
        return TransformedDict.__getitem__(self, key)

    def __setitem__(self, key, value):
        "Set key value-pair in dictionary"

        if key in self._valid_keys:
            return TransformedDict.__setitem__(self, key, value)
        else:
            raise Exception("Error: Invalid peer attribute '{}'.".format(key))

    def __delitem__(self, key):
        "Reset key's value."

        if key in self._valid_keys:
            # Delete the item
            TransformedDict.__delitem__(self, key)
            # Re-create key with no value
            TransformedDict.__setitem__(self, key, None)
        else:
            # Delete unauth key
            TransformedDict.__delitem__(self, key)

    def __keytransform__(self, key):
        "Manipulate key"

        return self._hash_key(key)

    def _hash_key(self, key):
        "Return md5 hash of key"

        return md5hash(key)

    def keys(self):
        "Return list of keys"

        return self._valid_keys

    def iteritems(self):
        "Iter (key, value) tuples"

        return [(k, self.__getitem__(k)) for k in self._valid_keys]

    def values(self):
        "Return list of values"

        return [self.__getitem__(k) for k in self._valid_keys]

    def items(self):
        "iteritem alias"

        return [(k, v) for (k, v) in self.iteritems()]

    def hmac(self):
        "Get Store checksum"

        _hmac = hmac.new(self.__repr__())

        for key in self._valid_keys:
            _hmac.update(str(self.__getitem__(key)))

        return _hmac.hexdigest()

    def check_hmac(self, _hmac):
        "HMAC challenge"

        try:
            return hmac.compare_digest(self.hmac(), _hmac)
        except exceptions.AttributeError:
            return self.hmac() == _hmac
        else:
            pass


if __name__ == "__main__":
    store = Store(keys=["key1", "key2"], dictionary={"key1": 1, "key2": 2})
    print store
    print store["key1"]
    del store["key2"]
    print store
    print store.__repr__()
    import cPickle
    print cPickle.loads(cPickle.dumps(store, protocol=0)) == store
