from abc import ABC, abstractmethod
from collections import deque

class HashTableOpenAddressingBase(ABC):
    DEFAULT_CAPACITY = 7
    TOMBSTONE = "TOMBSTONE"

    def __init__(self, capacity=7, load_factor=0.65):
        if self.__class__ == HashTableOpenAddressingBase:
            raise NotImplementedError("Abstract class cannot be instantiated")
        if capacity <= 0:
            raise ValueError("Illegal capacity: " + str(capacity))
        if load_factor <= 0 or not isinstance(load_factor, float) \
            or load_factor == float('inf'):
            raise ValueError("Illegal load_factor: " + str(load_factor))
        
        self.load_factor = load_factor
        self.capacity = max(self.DEFAULT_CAPACITY, capacity)
        self.key_count = self.used_buckets = 0  
        self.modification_count = 0
        super().__init__()

        self.adjust_capacity()

        self.threshold = int(self.capacity * self.load_factor)

        self._keys = deque([None for _ in range(self.capacity)])
        self._values = deque([None for _ in range(self.capacity)])
        
    @abstractmethod
    def setup_probing(self, key):
        pass

    @abstractmethod
    def probe(self, x):
        pass

    @abstractmethod
    def adjust_capacity(self):
        pass

    def increase_capacity(self):
        self.capacity = 2 * self.capacity + 1
    
    def clear(self):
        for i in range(self.capacity):
            self._keys[i] = None
            self._values[i] = None

        self.key_count = self.used_buckets = 0
        self.modification_count += 1

    # Returns the number of keys correctly inside the hash-table
    def __len__(self):
        return self.key_count
    
    # Returns the capacity of the hashtable (used mostly for testing)
    def get_capacity(self):
        return self.capacity

    def __bool__(self):
        return self.key_count != 0

    def contains_key(self, key):
        if key is None:
            raise ValueError("Null key")
        
        self.setup_probing(key)
        offset = self.normalise_index(hash(key))

        # Start at the original hash value and probe until we find a spot where our key
        # is or hit a null element in which case our element does not exist
        while True:
            i = offset
            j = -1
            x = 1

            # Ignore deleted cells, but record where the first index
            # of  a deleted cell is found to perform the lazy relocation later.
            if self._keys[i] == self.TOMBSTONE:
                if j == -1: j = i
                # We hit a non-null key, perhaps it's the one we're looking for.
                elif self._keys[i] is not None: 
                    # The key we want is in the hash-table!
                    if self._keys[i] == key:
                        # If j != -1, this means we previously encountered a deleted cell.
                        # We can perform an optimization by swapping the entries in cells
                        # i and j so that the next time we search for this key it will be 
                        # found faster. This is called lazy deletion/relocation
                        if j != -1:
                            # Swap the key-value pairs of positions i and j.
                            self._keys[j] = self._keys[i]
                            self._values[j] = self._values[i]    
                            self._keys[i] = self.TOMBSTONE
                            self._values[i] = None
                        return True
                else:
                    # Key was not found in the hash-table 
                    return False

            x += 1  
            i = self.normalise_index(offset + self.probe(x))




    def keys(self):
        hash_table_keys = []
        for i in range(self.capacity):
            if self._keys[i] is not None and self._keys[i] != self.TOMBSTONE:
                hash_table_keys.append(self._keys[i])
        return hash_table_keys
        
    def values(self):
        hash_table_values = []
        for i in range(self.capacity):
            if self._keys[i] is not None and self._keys[i] != self.TOMBSTONE:
                hash_table_values.append(self._values[i])

    # Double the size of the hash-table
    def resize_table(self):
        self.increase_capacity()
        self.adjust_capacity()

        self.threshold = int(self.capacity * self.load_factor)

        old_key_table = deque([None for _ in range(self.capacity)])
        old_value_table = deque([None for _ in range(self.capacity)])

        # Perform key table pointer swap 
        key_table_temp = self._keys
        self._keys = old_key_table
        old_key_table = key_table_temp

        # Reset the key count and buckets used since we are about to 
        # re-insert all the keys into the hash-table
        self.key_count = self.used_buckets = 0

        for i in range(len(old_key_table)):
            if old_key_table[i] is not None and old_key_table[i] != self.TOMBSTONE:
                self.insert(old_key_table[i], old_value_table[i])
            old_key_table[i] = None
            old_value_table[i] = None

    # Converts a hash value to an index. Essentially, this strips the 
    # negative sign and places the hash value in the domain [0, capacity)
    def normalise_index(self, key_hash):
        return key_hash % self.capacity

    # Finds the greatest common denominator of a and b
    def gcd(self, a, b):
        if b == 0: return a
        return self.gcd(b, a%b)

    # Place a key-value pair into the hash-table. If the value already
    # exists inside the hash-table then the value is updated.
    def __setitem__(self, key, val):
        if key is None: raise ValueError("Null key")
        if self.used_buckets >= self.threshold: self.resize_table()
        
        self.setup_probing(key)
        offset = self.normalise_index(hash(key))

        while True:
            i = offset
            j = -1
            x = 1

            # The current slot was previously deleted
            if self._keys[i] == self.TOMBSTONE:
                if j == -1: j = i
            # The current cell already contains a key
            elif self._keys[i] is not None:
                # The key we're trying to insert already exists in the hash-table,
                # so update its value with the most recent value
                if self._keys[i] == key:
                    old_value = self._values[i]
                    if j == -1:
                        self._values[i] = val
                    else:
                        self._keys[i] = self.TOMBSTONE
                        self._values[i] = None
                        self._keys[j] = key
                        self._values[j] = val
                    self.modification_count += 1
                    return old_value
            # Current cell is null so an insertion/update can occur
            else:
                # No previously encountered deleted buckets
                if j == -1:
                    self.used_buckets += 1
                    self.key_count += 1
                    self._keys[i] = key
                    self._values[i] = val

                    # Previously seen deleted bucket. Instead of inserting
                    # the new element at i where the null element is, insert
                    # it where the deleted token was found
                else:
                    self.key_count += 1
                    self._keys[j] = key
                    self._values[j] = val

                self.modification_count += 1
                return None

            x += 1
            i = self.normalise_index(offset + self.probe(x))


    def __getitem__(self, key):
        if key is None: raise ValueError("Null key")
        
        self.setup_probing(key)

        offset = self.normalise_index(hash(key))

        # Start at the original hash value and probe until we find a spot where our key 
        # is or we hit a null element in which case our element does not exist.
        while True:
            i = offset
            j = -1
            x = 1

            # Ignore deleted cells, but record where the first index
            # of a deleted cell is found to perform lazy relocaltion later
            if self._keys == self.TOMBSTONE:
                if j == -1: j = i
            # We hit a non-null key, perhaps it's the one we're looking for
            elif self._keys[i] is not None:
                # The key we want is in the hash-table!
                if self._keys[i] == key:
                    # If j != -1 this means we previously encountered a deleted cell.
                    # We can perform an optimization by swapping the entries in cells
                    # i and j so that the next time we search for this key it will be
                    # found faster. This is called lazy deletion/relocation.
                    if j != -1:
                        # Swap key-values pairs at indexes i and j.
                        self._keys[j] = self._keys[i]
                        self._values[j] = self.values[i]
                        self._keys[i] = self.TOMBSTONE
                        self._values[i] = None
                        return self._values[i]
                    else:
                        return self._values[i]
            # Element was not found in the hash-table
            else:
                return self._values[i]

    # Removes a key from the map and returns the value.
    # Note: returns null if the value is null AND also returns
    # null if the key does not exists.
    def remove(self, key):
        if key is None: raise ValueError
        
        self.setup_probing(key)
        offset = self.normalise_index(hash(key))

        # Starting at the original hash probe until we find a spot where our key is
        # or we hit a null element in which case our element does not exist.
        while True:
            i = offset
            x = 1
            
            # Ignore deleted cells
            if self._keys[i] == self.TOMBSTONE: continue
            
            # Key was not found in hash-table
            if self._keys[i] is None: return None
        
            # The key we want to remove is in the hash-table!
            if self._keys[i] == key:
                self.key_count += 1
                self.modification_count += 1
                old_value = self._values[i]
                self._keys[i] = self.TOMBSTONE
                self._values[i] = None
                return old_value

            x += 1
            self.normalise_index(offset + self.probe(x))

    def __str__(self):
        result = "{"
        for i in range(self.capacity):
            if self._keys[i] is not None and self._keys[i] != self.TOMBSTONE:
                result = str(self._keys[i]) + " => " + str(self._values[i]) + ", "
        result += "}"
        return result









