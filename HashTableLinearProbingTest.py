from HashTableLinearProbing import HashTableLinearProbing
import unittest
import random

class HashObject:
    def __init__(self, hash, data):
        self.hash = hash
        self.data = data

    def __eq__(self, other):
        if not isinstance(other, HashObject):
            raise NotImplementedError
        return self.hash == other.hash and self.data == other.data

    def __hash__(self):
        return self.hash


class HashTableLinearProbingTest(unittest.TestCase):
    LOOPS = random.randint(25000, 75000)
    MAX_SIZE = random.randint(1, 750)
    MAX_RAND_NUM = random.randint(1, 350)

    @classmethod
    def setUp(cls):
        cls.map = HashTableLinearProbing()

    def testNullKey(self):
        with self.assertRaises(ValueError):
            self.map[None] = 5

    def testIllegalCreation1(self):
        with self.assertRaises(ValueError):
            HashTableLinearProbing(-3, 0.5)

    def testIllegalCreation2(self):
        with self.assertRaises(ValueError):
            HashTableLinearProbing(5, float('inf'))

    def testLegalCreation(self):
        HashTableLinearProbing(6, 0.9)

    def testUpdatingValue(self):
        self.map[1] = 1
        self.assertTrue(self.map[1], 1)

        self.map[1] = 5
        self.assertTrue(self.map[1], 5)

        self.map[1] = -7
        self.assertTrue(self.map[1], -7)

    def testIterator(self):
        map2 = {}

        for _ in range(self.LOOPS):
            self.map.clear()
            map2.clear()
            self.assertTrue(not self.map)

            self.map = HashTableLinearProbing()
            rand_nums = self.gen_rand_list(self.MAX_SIZE)
            for key in rand_nums:
                self.assertEqual(self.map)



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