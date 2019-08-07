"""
A generic dynamic array implementation

"""
class DynamicArray:
    def __init__(self, capacity=0):
        self._index = 0
        self.capacity = capacity # actual array size
        self.arr = [None for _ in range(self.capacity)] 
        self.size = 0 # length user thinks array is

    def __len__(self):
        return self.size
    
    def isEmpty(self):
        return self.size == 0

    def __getitem__(self, index):
        return self.arr[index]

    def __setitem__(self, index, elem):
        self.arr[index] = elem

    def clear(self):
        for i in range(self.size): self.arr[i] = None
    
    def add(self, elem):
        # To resize
        if self.size + 1 >= self.capacity:
            if self.capacity == 0: 
                self.capacity = 1
            else: 
                self.capacity *= 2
            new_arr = DynamicArray(self.capacity)
            for i in range(self.size):
                new_arr[i] = self.arr[i]
            self.arr = new_arr
        self.arr[self.size] = elem
        self.size += 1

    # Removes an element at the specified index in this array
    def removeAt(self, rm_index):
        if rm_index >= self.size or rm_index < 0: 
            raise IndexError 
        data = self.arr[rm_index]
        new_arr = DynamicArray(self.capacity - 1)
        i, j = 0, 0
        while i < self.size: #self.size = 3 
            if i == rm_index: 
                j -= 1
            else: 
                new_arr[j] = self.arr[i]
            i += 1
            j += 1
        self.arr = new_arr
        self.size -= 1
        return data

    def remove(self, elem):
        index = self.indexOf(elem)
        if index == -1: return False
        self.removeAt(index)
        return True

    def indexOf(self, elem):
        for i in range(self.size):
            if elem == self.arr[i]:
                return i
        return -1
    
    def __contains__(self, elem):
        return self.indexOf(elem) != -1
    
    

    def __iter__(self):
        return self

    def __next__(self):
        if self._index > self.size: raise StopIteration
        else:
            data = self.arr[self._index]
            self._index += 1
            return data
        
    def __str__(self):
        if self.size == 0: return "[]"
        else:
            ans = "["
            for i in range(self.size - 1):
                ans += str(self.arr[i]) + ", "
            ans += str(self.arr[self.size - 1]) + "]"
        return ans

