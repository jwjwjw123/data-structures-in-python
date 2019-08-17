import unittest
import random
from HashTableSeparateChaining import HashTableSeparateChaining

class HashObject:
    def __init__(self, hash, data):
        self.hash = hash
        self.data = data

    def __eq__(self, other):
        if not isinstance(other, HashObject):
            return NotImplemented
        return self.hash == other.hash and self.data == other.data

    def __hash__(self):
        return self.hash

class HashTableSeparateChainingTest(unittest.TestCase):
    LOOPS = random.randint(25000, 75000)
    MAX_SIZE = random.randint(1, 750)
    MAX_RAND_NUM = random.randint(1, 350)

    @classmethod
    def setUp(cls):
        cls.map = HashTableSeparateChaining()

    def testNullKey(self):
        with self.assertRaises(ValueError):
            self.map[None] = 5

    def testIllegalCreation1(self):
        with self.assertRaises(ValueError):
            HashTableSeparateChaining(-3, 0.5)

    def testIllegalCreation2(self):
        with self.assertRaises(ValueError):
            HashTableSeparateChaining(5, float('inf'))

    def testIllegalCreation3(self):
        with self.assertRaises(ValueError):
            HashTableSeparateChaining(6, -0.5)

    def testLegalCreation(self):
        HashTableSeparateChaining(6, 0.9)

    def testUpdatingValue(self):
        self.map[1] = 1
        self.assertTrue(1 == self.map[1])

    def testIterator(self):
        map2 = {}
        for _ in range(self.LOOPS):
            self.map.clear()
            map2.clear()
            self.assertTrue(not self.map)

            self.map = HashTableSeparateChaining()

            rand_nums = self.genRandList(self.MAX_SIZE)

            for key in rand_nums:
                self.map[key] = key
                map2[key] = key

            count = 0
            for key in self.map:
                self.assertEqual(key, self.map[key])
                self.assertEqual(self.map[key], map2[key])
                self.assertTrue(key in self.map)
                self.assertTrue(key in rand_nums)
                count += 1

            for key in map2:
                self.assertEqual(key, self.map[key])
            
            mySet = set()
            for n in rand_nums:
                mySet.add(n)
            
            self.assertEqual(len(mySet), count)
            self.assertEqual(len(map2), count)

    def testRandomRemove(self):
        for _ in range(self.LOOPS):
            myMap = HashTableSeparateChaining()
            myMap.clear()
            # Add some random values
            keys_set = set()
            for _ in range(self.MAX_SIZE):
                randomVal = random.randint(-self.MAX_RAND_NUM, self.MAX_RAND_NUM)
                keys_set.add(randomVal)
                myMap[randomVal] = 5

            self.assertEqual(len(myMap), len(keys_set))

            keys = myMap.keys()
            for key in keys:
                myMap.remove(key)
            
            self.assertTrue(not myMap)


    def testRemove(self):
        myMap = HashTableSeparateChaining()

        # Add three elements
        myMap[11] = 0
        myMap[12] = 0
        myMap[13] = 0
        self.assertEqual(3, len(myMap))

        # Add ten more
        for i in range(1, 11):
            myMap[i] = 0
        self.assertEqual(13, len(myMap))

        # Remove ten
        for i in range(1, 11):
            myMap.remove(i)
        self.assertEqual(3, len(myMap))

        # remove three
        myMap.remove(11)
        myMap.remove(12)
        myMap.remove(13)
        self.assertEqual(0, len(myMap))

    def testRemoveComplex1(self):
        myMap = HashTableSeparateChaining()
        o1 = HashObject(88, 1)
        o2 = HashObject(88, 2)
        o3 = HashObject(88, 3)
        o4 = HashObject(88, 4)
    
        myMap[o1] = 111
        myMap[o2] = 111
        myMap[o3] = 111
        myMap[o4] = 111
    
        myMap.remove(o2)
        myMap.remove(o3)
        myMap.remove(o1)
        myMap.remove(o4)
    
        self.assertEqual(0, len(myMap))

    def testRandomMapOperations(self):
        pymap = {}
        for _ in range(self.LOOPS):
            self.map.clear()
            pymap.clear()
            self.assertEqual(len(pymap), len(self.map))

            self.map = HashTableSeparateChaining()

            prob1 = random.random()
            prob2 = random.random()
            nums = self.genRandList(self.MAX_SIZE)
            for i in range(self.MAX_SIZE):
                r = random.random()

                key = nums[i]
                val = i

                if r < prob1:
                    pymap[key] = val
                    self.map[key] = val
                
                self.assertEqual(pymap.get(key, None), self.map[key])
                self.assertEqual(key in pymap, key in self.map)
                self.assertEqual(len(pymap), len(self.map))

                if r > prob2:
                    self.map.remove(key)
                    pymap.pop(key, None)

                self.assertEqual(pymap.get(key, None), self.map[key])
                self.assertEqual(key in pymap, key in self.map)
                self.assertEqual(len(pymap), len(self.map))




    # Generate a list of random numbers
    def genRandList(self, sz):
        lst = [random.randint(-self.MAX_RAND_NUM, self.MAX_RAND_NUM) for _ in range(sz)]
        return lst
    
    # Generate a list of unique random numbers
    def genUniqueRandList(self, sz):
        lst = random.sample(range(0, sz), sz)
        return lst







if __name__ == "__main__":
    unittest.main()

    # myMap = HashTableSeparateChaining()
    # o1 = HashObject(88, 1)
    # o2 = HashObject(88, 2)
    # o3 = HashObject(88, 3)
    # o4 = HashObject(88, 4)

    # myMap[o1] = 112
    # myMap[o2] = 113
    # myMap[o3] = 114
    # myMap[o4] = 115
    


    # myMap.remove(o2)
    # myMap.remove(o3)
    # myMap.remove(o1)
    # myMap.remove(o4)
    
    # print(myMap[o4])