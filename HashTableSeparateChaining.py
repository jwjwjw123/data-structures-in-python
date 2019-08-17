"""
An implementation of a hash-table using separate chaining with a linked list

"""

from collections import deque

class Entry:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.hash = hash(key)

    def __eq__(self, other):
        if not isinstance(other, Entry):
            # Don't attempt to compare against unrelated types
            return NotImplemented
        if self.hash != other.hash:
            return False
        return self.key == other.key

    def __str__(self):
        return str(self.key) + " => " + str(self.value)

class HashTableSeparateChaining:
    __DEFAULT_CAPACITY = 3

    def __init__(self, capacity=3, maxLoadFactor=0.75):
        if capacity < 0:
            raise ValueError
        if maxLoadFactor <= 0 or maxLoadFactor == float('inf'):  
            raise ValueError
        self.capacity = max(capacity, self.__DEFAULT_CAPACITY)
        self.size = 0
        self.maxLoadFactor = maxLoadFactor
        self.threshold = int(self.capacity * self.maxLoadFactor)
        self.table = deque([None for _ in range(self.capacity)])
    
    def __len__(self):
        return self.size

    def __bool__(self):
        return self.size != 0

    def __normalizeIndex(self, keyHash):
        return keyHash % self.capacity

    # Clears all the contents of the hashtable
    def clear(self):
        self.table = deque([None for _ in range(self.capacity)])
        self.size = 0

    def __contains__(self, key):
        bucketIndex = self.__normalizeIndex(hash(key))
        return self.__bucketSeekEntry(bucketIndex, key) is not None

    def __setitem__(self, key, value):
        if key is None:
            raise ValueError
        newEntry = Entry(key, value)
        bucketIndex = self.__normalizeIndex(newEntry.hash)
        self.__bucketInsertEntry(bucketIndex, newEntry)

    def __getitem__(self, key):
        if key is None:
            return None
        bucketIndex = self.__normalizeIndex(hash(key))
        entry = self.__bucketSeekEntry(bucketIndex, key)
        if entry is not None:
            return entry.value
        else:
            return None

    def remove(self, key):
        if key is None:
            return None
        bucketIndex = self.__normalizeIndex(hash(key))
        self.__bucketRemoveEntry(bucketIndex, key)


    # Removes an entry from a given bucket if it exists
    def __bucketRemoveEntry(self, bucketIndex, key):
        entry = self.__bucketSeekEntry(bucketIndex, key)
        if entry is not None:
            bucket = self.table[bucketIndex]
            bucket.remove(entry)
            self.size -= 1

    # Inserts an entry in a given bucket only if the entry does not already
    # exist in the given bucket, but if it does then update the entry value
    def __bucketInsertEntry(self, bucketIndex, entry):
        bucket = self.table[bucketIndex]
        if bucket is None:
            self.table[bucketIndex] = bucket = deque([])
        existingEntry = self.__bucketSeekEntry(bucketIndex, entry.key)
        if existingEntry is None:
            bucket.append(entry)
            self.size += 1
            if self.size > self.threshold:
                self.__resizeTable()
        else:
            # oldVal = existingEntry.value
            existingEntry.value = entry.value

    # Finds and returns a particular entry in a given bucket if it exists,
    # return null otherwise
    def __bucketSeekEntry(self, bucketIndex, key):
        if key is None:
            return None
        bucket = self.table[bucketIndex]
        if bucket is None:
            return None
        for entry in bucket:
            if entry.key == key:
                return entry
        return None

    # Resize the internal table holding buckets of entries
    def __resizeTable(self):
        self.capacity *= 2
        self.threshold = int(self.capacity * self.maxLoadFactor)

        newTable = deque([None for _ in range(self.capacity)])

        for i in range(len(self.table)):
            if self.table[i] is not None:
                for entry in self.table[i]:
                    bucketIndex = self.__normalizeIndex(entry.hash)
                    bucket = newTable[bucketIndex]
                    if bucket is None:
                        newTable[bucketIndex] = bucket = deque([])
                    bucket.append(entry)
                # Avoid memory leak. Help the GC
                self.table[i].clear()
                self.table[i] = None

        self.table = newTable


    def keys(self):
        keys = deque([])
        for bucket in self.table:
            if bucket is not None:
                for entry in bucket:
                    keys.append(entry.key)
        return keys

    def values(self):
        values = deque([])
        for bucket in self.table:
            if bucket is not None:
                for entry in bucket:
                    values.append(entry.value)
        return values

    # Returns an iterator to iterate over all the keys in this map
    def __iter__(self):
        bucketIndex = 0
        self.arr = deque([])
        # bucketIter = None if self.table[0] is None else self.table[0]
        # if bucketIter is None or len(bucketIter) == 0:
        while bucketIndex < self.capacity:
            if self.table[bucketIndex] is not None:
                bucket = self.table[bucketIndex]
                for entry in bucket:
                    self.arr.append(entry.key)
            bucketIndex += 1

        return iter(self.arr)

    # Returns a string representation of this hash table
    def __str__(self):
        result = "{"
        for i in range(self.capacity):
            if self.table[i] is None:
                continue
            for entry in self.table[i]:
                result += str(entry) + ", "
        result += "}"
        return result
    
# import random

# for _ in range(75000):
#     myMap = HashTableSeparateChaining()
#     for _ in range(750):
#         randomVal = random.randint(-350, 350)
#         myMap[randomVal] = 5
