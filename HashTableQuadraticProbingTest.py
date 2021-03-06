import unittest
import random
import math
from HashTableQuadraticProbing import HashTableQuadraticProbing

class HashObject:
    def __init__(self, hash, data):
        self.hash = hash
        self.data = data

    def __eq__(self, other):
        if not isinstance(other, HashObject):
            return False
        return self.hash == other.hash and self.data == other.data

    def __hash__(self):
        return self.hash

class HashTableQuadraticProbingTest(unittest.TestCase):
    LOOPS = random.randint(25000, 75000)
    MAX_SIZE = random.randint(1, 750)
    MAX_RAND_NUM = random.randint(1, 350)

    @classmethod
    def setUp(cls):
        cls.map = HashTableQuadraticProbing()

    def testNullKey(self):
        with self.assertRaises(ValueError):
            self.map[None] = 5

    def testIllegalCreation1(self):
        with self.assertRaises(ValueError):
            HashTableQuadraticProbing(-3, 0.5)

    def testIllegalCreation2(self):
        with self.assertRaises(ValueError):
            HashTableQuadraticProbing(5, float('inf'))

    def testIllegalCreation3(self):
        with self.assertRaises(ValueError):
            HashTableQuadraticProbing(6, -0.5)

    def testLegalCreation(self):
        HashTableQuadraticProbing(6, 0.9)

    def testUpdatingValue(self):
        self.map[1] = 1
        self.assertEqual(1, self.map[1])

        self.map[1] = 5
        self.assertEqual(5, self.map[1])

        self.map[1] = -7
        self.assertEqual(-7, self.map[1])

    def assertCapacityIsPowerOfTwo(self, ht):
        sz = ht.get_capacity()
        if sz == 0:
            return
        self.assertTrue(math.log(sz, 2).is_integer())

    # Test that as the table size increases, the hashtable
    # remains as a power of two
    def testTableSize(self):
        loops = 10000
        for sz in range(1, 33):
            self.map = HashTableQuadraticProbing(sz)
            for i in range(loops):
                self.assertCapacityIsPowerOfTwo(self.map)
                self.map[i] = i

    def testIterator(self):
        map2 = {}
        for _ in range(self.LOOPS):
            self.map.clear()
            map2.clear()
            self.assertTrue(not self.map)

            self.map = HashTableQuadraticProbing()

            rand_nums = self.gen_rand_list(self.MAX_SIZE)
            
            for key in rand_nums:
                self.map[key] = key
                map2[key] = key
                self.assertEqual(len(self.map), len(map2))

            count = 0

            for key in self.map:
                self.assertEqual(key, self.map[key])
                self.assertEqual(self.map[key], map2[key])
                self.assertTrue(self.map.contains_key(key))
                self.assertTrue(key in rand_nums)
                count += 1
                
            for key in map2.keys():
                self.assertEqual(key, self.map[key])

            myset = set()
            for n in rand_nums:
                myset.add(n)

            self.assertEqual(len(myset), count)
            self.assertEqual(len(map2), count)

    def testRandomRemove(self):
        for _ in range(self.LOOPS):
            self.map = HashTableQuadraticProbing()
            self.map.clear()

            keys_set = set()

            for i in range(self.MAX_SIZE):
                randomVal = random.randint(-self.MAX_RAND_NUM, self.MAX_RAND_NUM)
                keys_set.add(randomVal)
                self.map[randomVal] = 5
            
            self.assertEqual(len(self.map), len(keys_set))

            keys = self.map.keys()

            for key in keys:
                self.map.remove(key)

            self.assertTrue(not self.map)

    def testRemove(self):
        self.map = HashTableQuadraticProbing(7)

        self.map[11] = 0
        self.map[12] = 0
        self.map[13] = 0
        self.assertEqual(3, len(self.map))

        for i in range(1, 11):
            self.map[i] = 0

        self.assertEqual(13, len(self.map))

        for i in range(1, 11):
            self.map.remove(i)

        self.assertEqual(3, len(self.map))

        self.map.remove(11)
        self.map.remove(12)
        self.map.remove(13)

        self.assertEqual(0, len(self.map))

    def testRemoveComplex1(self):
        self.map = HashTableQuadraticProbing()

        o1 = HashObject(88, 1)
        o2 = HashObject(88, 2)
        o3 = HashObject(88, 3)
        o4 = HashObject(88, 4)

        self.map[o1] = 111
        self.map[o2] = 111
        self.map[o3] = 111
        self.map[o4] = 111

        self.map.remove(o2)
        self.map.remove(o3)
        self.map.remove(o1)
        self.map.remove(o4)

        self.assertEqual(0, len(self.map))

    def testRandomMapOperations(self):
        pymap = {}
        
        for _ in range(self.LOOPS):
            
            self.map.clear()
            pymap.clear()
            self.assertEqual(len(pymap), len(self.map))

            self.map = HashTableQuadraticProbing()

            probability1 = random.random()
            probability2 = random.random()

            nums = self.gen_rand_list(self.MAX_SIZE)
            for i in range(self.MAX_SIZE):

                r = random.random()

                key = nums[i]
                val = i

                if r < probability1:
                    pymap[key] = val
                    self.map[key] = val
                    self.assertEqual(len(pymap), len(self.map))
                    
                self.assertEqual(pymap.get(key, None), self.map[key])
                self.assertEqual(key in pymap, self.map.contains_key(key))
                self.assertEqual(len(pymap), len(self.map))

                if r > probability2:
                    self.assertEqual(pymap.pop(key, None), self.map.remove(key))

                self.assertEqual(pymap.get(key, None), self.map[key])
                self.assertEqual(key in pymap, self.map.contains_key(key))
                self.assertEqual(len(pymap), len(self.map))

    def testRandomIterator(self):
        pymap = {}
        
        for _ in range(self.LOOPS):
            self.map.clear()
            pymap.clear()
            self.assertEqual(len(self.map), len(pymap))

            probability = random.random()

            for _ in range(self.MAX_SIZE):
                index = random.randint(0, self.MAX_SIZE - 1)
                l1 = []
                l2 = []
                self.map[index] = l1
                pymap[index] = l2

                rand_val = random.randint(-self.MAX_SIZE, self.MAX_SIZE)

                if random.random() < probability:
                    if rand_val in l1: l1.remove(rand_val)
                    if rand_val in l2: l2.remove(rand_val)
                else:
                    l1.append(rand_val)
                    l2.append(rand_val)

                self.assertEqual(len(self.map), len(pymap))
                self.assertEqual(l1, l2)







    # Generate a list of random numbers
    def gen_rand_list(self, sz):
        lst = [random.randint(-self.MAX_RAND_NUM, self.MAX_RAND_NUM) for _ in range(sz)]
        return lst

    # Generate a list of unique random numbers
    def gen_unique_rand_list(self, sz):
        lst = random.sample(range(0, sz), sz)
        return lst


if __name__ == "__main__":
    unittest.main()
