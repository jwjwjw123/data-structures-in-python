from HashTableOpenAddressingBase import HashTableOpenAddressingBase
import math

class HashTableQuadraticProbing(HashTableOpenAddressingBase):
    def __init__(self, capacity=7, load_factor=0.65):
        super().__init__(capacity, load_factor)
    
    def __nextPowerOfTwo(self, n):
        k = int(math.log(n, 2))
        return 2**(k+1)

    def setup_probing(self, key):
        pass

    def probe(self, x):
        # Quadratic probing function (x^2 + x)/2
        return (x * x + x) // 2
    
    def increase_capacity(self):
        self.capacity = self.__nextPowerOfTwo(self.capacity)

    def adjust_capacity(self):
        pow2 = int(math.log(self.capacity, 2))
        if self.capacity == pow2:
            return
        self.increase_capacity()