import unittest
import random
from DoublyLinkedList import *

class DoublyLinkedListTest(unittest.TestCase):
    LOOPS = 10000
    TEST_SZ = 40
    NUM_NULLS = TEST_SZ // 5
    MAX_RAND_NUM = 250

    @classmethod
    def setUp(self):
        self._list = DoublyLinkedList()

    def testEmptyList(self):
        self.assertTrue(self._list.isEmpty())
        self.assertEqual(len(self._list), 0)

    def testRemoveFirstOfEmpty(self):
        self.assertRaises(RuntimeError, self._list.removeFirst)

    def testRemoveLastOfEmpty(self):
        self.assertRaises(RuntimeError, self._list.removeLast)

    def testPeekFirstOfEmpty(self):
        self.assertRaises(RuntimeError, self._list.peekFirst)
    
    def testPeekLastOfEmpty(self):
        self.assertRaises(RuntimeError, self._list.peekLast)

    def testAddFirst(self):
        self._list.addFirst(3)
        self.assertEqual(len(self._list), 1)
        self._list.addFirst(5)
        self.assertEqual(len(self._list), 2)

    def testAddLast(self):
        self._list.addLast(3)
        self.assertEqual(len(self._list), 1)
        self._list.addLast(5)
        self.assertEqual(len(self._list), 2)

    def testRemoveFirst(self):
        self._list.addFirst(3)
        self.assertEqual(self._list.removeFirst(), 3)
        self.assertTrue(self._list.isEmpty())

    def testRemoveLast(self):
        self._list.addLast(4)
        self.assertEqual(self._list.removeLast(), 4)
        self.assertTrue(self._list.isEmpty())
    
    def testPeekFirst(self):
        self._list.addFirst(4)
        self.assertEqual(self._list.peekFirst(), 4)
        self.assertEqual(len(self._list), 1)

    def testPeekLast(self):
        self._list.addLast(4)
        self.assertEqual(self._list.peekLast(), 4)
        self.assertEqual(len(self._list), 1)

    def testPeeking(self):
        # 5
        self._list.addFirst(5)
        self.assertTrue(self._list.peekFirst() == 5)
        self.assertTrue(self._list.peekLast() == 5)

        # 6 - 5
        self._list.addFirst(6)
        self.assertTrue(self._list.peekFirst() == 6)
        self.assertTrue(self._list.peekLast() == 5)

        # 7 - 6 - 5
        self._list.addFirst(7)
        self.assertTrue(self._list.peekFirst() == 7)
        self.assertTrue(self._list.peekLast() == 5)

        # 7 - 6 - 5 - 8
        self._list.addLast(8)
        self.assertTrue(self._list.peekFirst() == 7)
        self.assertTrue(self._list.peekLast() == 8)

        # 7 - 6 - 5
        self._list.removeLast()
        self.assertTrue(self._list.peekFirst() == 7)
        self.assertTrue(self._list.peekLast() == 5)

        # 7 - 6
        self._list.removeLast()
        self.assertTrue(self._list.peekFirst() == 7)
        self.assertTrue(self._list.peekLast() == 6)

        # 6
        self._list.removeFirst()
        self.assertTrue(self._list.peekFirst() == 6)
        self.assertTrue(self._list.peekLast() == 6)

    def testRemoving(self):
        self._list.add("a")
        self._list.add("b")
        self._list.add("c")
        self._list.add("d")
        self._list.add("e")
        self._list.add("f")
        self._list.remove("b")
        self._list.remove("a")
        self._list.remove("d")
        self._list.remove("e")
        self._list.remove("c")
        self._list.remove("f")
        self.assertEqual(0, len(self._list))

    def testRemoveAt(self):
        self._list.add(1)
        self._list.add(2)
        self._list.add(3)
        self._list.add(4)
        self._list.removeAt(0)
        self._list.removeAt(2)
        self.assertTrue(self._list.peekFirst() == 2)
        self.assertTrue(self._list.peekLast() == 3)
        self._list.removeAt(1)
        self._list.removeAt(0)
        self.assertEquals(len(self._list), 0)

    def testClear(self):
        self._list.add(22)
        self._list.add(33)
        self._list.add(44)
        self.assertEquals(len(self._list), 3)
        self._list.clear()
        self.assertEquals(len(self._list), 0)
        self._list.add(22)
        self._list.add(33)
        self._list.add(44)
        self.assertEquals(len(self._list), 3)
        self._list.clear()
        self.assertEquals(len(self._list), 0)

    def testRandomisedRemoving(self):
        another_list = []
        for _ in range(self.LOOPS):
            another_list.clear()
            self._list.clear()

            randNums = self.genRandList(self.TEST_SZ)
            for val in randNums:
                another_list.append(val)
                self._list.add(val)

            random.shuffle(randNums)

            for i in range(len(randNums)):
                rm_val = randNums[i]
                self.assertEqual(another_list.pop(another_list.index(rm_val)), self._list.remove(rm_val))
                self.assertEqual(len(another_list), len(self._list))

                iter1 = iter(another_list)
                iter2 = iter(self._list)
                while True:
                    val1 = next(iter1, None)
                    val2 = next(iter2, None)
                    if val1 is not None:
                        self.assertEqual(val1, val2)
                    else:
                        break
                
                iter1 = iter(another_list)
                iter2 = iter(self._list)
                while True:
                    val1 = next(iter1, None)
                    val2 = next(iter2, None)
                    if val1 is not None:
                        self.assertEqual(val1, val2)
                    else:
                        break
            
            for val in randNums:
                another_list.append(val)
                self._list.add(val)
            
            # Try removing elements whether or not they exist
            for i in range(len(randNums)):
                rm_val = self.MAX_RAND_NUM * random.random()
                self.assertEqual(rm_val if rm_val in another_list else None , self._list.remove(rm_val))
                self.assertEqual(len(another_list), len(self._list))
                iter1 = iter(another_list)
                iter2 = iter(self._list)
                while True:
                    val1 = next(iter1, None)
                    val2 = next(iter2, None)
                    if val1 is not None:
                        self.assertEqual(val1, val2)
                    else:
                        break

    def testRandomisedRemoveAt(self):
        another_list = []
        for _ in range(self.LOOPS):
            another_list.clear()
            self._list.clear()

            randNums = self.genRandList(self.TEST_SZ)

            for val in randNums:
                another_list.append(val)
                self._list.add(val)

            for _ in range(len(randNums)):
                rm_idx = int(len(self._list) * random.random())
                num1 = another_list.pop(rm_idx)
                num2 = self._list.removeAt(rm_idx)
                self.assertEqual(num1, num2)
                self.assertEqual(len(another_list), len(self._list))

                iter1 = iter(another_list)
                iter2 = iter(self._list)
                while True:
                    val1 = next(iter1, None)
                    val2 = next(iter2, None)
                    if val1 is not None:
                        self.assertEqual(val1, val2)
                    else:
                        break

    def testRandomisedIndexOf(self):
        another_list = []

        for i in range(self.LOOPS):
            another_list.clear()
            self._list.clear()

            randNums = self.getUniqueRandList(self.TEST_SZ)

            for val in randNums:
                another_list.append(val)
                self._list.add(val)

            random.shuffle(randNums)

            for i in range(len(randNums)):
                elem = randNums[i]
                index1 = another_list.index(elem)
                index2 = self._list.indexOf(elem)

                self.assertEqual(index1, index2)
                self.assertEqual(len(another_list), len(self._list))

                iter1 = iter(another_list)
                iter2 = iter(self._list)

                while True:
                    val1 = next(iter1, None)
                    val2 = next(iter2, None)
                    if val1 is not None:
                        self.assertEqual(val1, val2)
                    else:
                        break

    def genRandList(self, sz):
        another_list = []
        for _ in range(sz):
            another_list.append(random.random() * self.MAX_RAND_NUM)
        for _ in range(self.NUM_NULLS):
            another_list.append(None)
        random.shuffle(another_list)
        return another_list

    def getUniqueRandList(self, sz):
        lst = []
        for i in range(sz):
            lst.append(i)
        for _ in range(self.NUM_NULLS):
            lst.append(None)
        random.shuffle(lst)
        return lst
    

if __name__ == "__main__":
    unittest.main()