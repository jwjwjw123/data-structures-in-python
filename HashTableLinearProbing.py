from HashTableOpenAddressingBase import HashTableOpenAddressingBase

class HashTableLinearProbing(HashTableOpenAddressingBase):
    # This is the linear constant used in the linear probing, it can be 
    # any positive number. The table capacity will be adjusted so that
    # the GCD(capacity, LINEAR_CONSTANT) = 1 so that all buckets can be probed.
    LINEAR_CONSTANT = 17
    
    def __init__(self, capacity=7, load_factor=0.65):
        super().__init__(capacity, load_factor)


    def setup_probing(self, key):
        pass
    
    def probe(self, x):
        return self.LINEAR_CONSTANT * x

    # Adjust the capacity so that the linear constant and 
    # the table capacity are relatively prime
    def adjust_capacity(self):
        while self.gcd(self.LINEAR_CONSTANT, self.capacity) != 1:
            self.capacity += 1

    