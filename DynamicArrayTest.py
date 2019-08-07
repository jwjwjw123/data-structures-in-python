import unittest
from DynamicArray import *

class DynamicArrayTest(unittest.TestCase):
    @classmethod
    def setUp(cls):
        self._list = DynamicArray()

    def testEmptyList(self):
        self.assertTrue(self._list.isEmpty())

    def testRemovingEmpty(self):
        self.assertRaises(IndexError, self._list.removeAt, 0)

    def testIndexOutOfBounds(self):
        self._list.add(-56)
        self._list.add(-53)
        self._list.add(-55)
        self.assertRaises(IndexError, self._list.removeAt, 3)

    def testIndexOutOfBounds2(self):
        for _ in range(1000):
            self._list.add(789)
        self.assertRaises(IndexError, self._list.removeAt, 1000)
    
    def testIndexOutOfBounds3(self):
        for _ in range(1000):
            self._list.add(789)
        self.assertRaises(IndexError, self._list.removeAt, -1)

    def testIndexOutOfBounds4(self):
        for _ in range(15):
            self._list.add(123)
        self.assertRaises(IndexError, self._list.removeAt, -66)

    def testRemoving(self):
        strs = {"a", "b", "c", "d", "e", None, "g", "h"}
        for s in strs:
            self._list.add(s)
        self.assertTrue(self._list.remove("c"))
        self.assertFalse(self._list.remove("c"))
        self.assertTrue(self._list.remove("h"))
        self.assertTrue(self._list.remove(None))
        self.assertTrue(self._list.remove("a"))
        self.assertFalse(self._list.remove("a"))
        self.assertFalse(self._list.remove("h"))
        self.assertFalse(self._list.remove(None))

    def testRemoving2(self):
        strs = {"a", "b", "c", "d"} 
        for s in strs:
            self._list.add(s)
        
        self.assertTrue(self._list.remove("a"))
        self.assertTrue(self._list.remove("b"))
        self.assertTrue(self._list.remove("c"))
        self.assertTrue(self._list.remove("d"))
        self.assertFalse(self._list.remove("a"))
        self.assertFalse(self._list.remove("b"))
        self.assertFalse(self._list.remove("c"))
        self.assertFalse(self._list.remove("d"))

    def testIndexOutOfNullElement(self):
        strs = ["a", "b", None, "d"]
        for s in strs:
            self._list.add(s)
        self.assertEqual(self._list.indexOf(None), 2)

    def testAddingElements(self):
        elems = [1, 2, 3, 4, 5, 6, 7]
        for i in range(len(elems)):
            self._list.add(elems[i])
        
        for i in range(len(elems)):
            self.assertEqual(self._list[i], elems[i])
        
    def testAddAndRemove(self):
        for _ in range(55):
            self._list.add(44)
        for _ in range(55):
            self._list.remove(44)
        self.assertTrue(self._list.isEmpty())

        for _ in range(55):
            self._list.add(44)
        for _ in range(55):
            self._list.removeAt(0)
        self.assertTrue(self._list.isEmpty())

        for _ in range(155):
            self._list.add(44)
        for _ in range(155):
            self._list.remove(44)
        self.assertTrue(self._list.isEmpty())

        for _ in range(155):
            self._list.add(44)
        for _ in range(155):
            self._list.removeAt(0)
        self.assertTrue(self._list.isEmpty())

    def testAddSetRemove(self):
        for i in range(55):
            self._list.add(44)
        for i in range(55):
            self._list[i] = 33    
        for i in range(55):
            self._list.remove(33)
        self.assertTrue(self._list.isEmpty())

        for i in range(55):
            self._list.add(44)
        for i in range(55):
            self._list[i] = 33
        for i in range(55):
            self._list.removeAt(0)
        self.assertTrue(self._list.isEmpty())

        for i in range(155):
            self._list.add(44)
        for i in range(155):
            self._list[i] = 33    
        for i in range(155):
            self._list.remove(33)
        self.assertTrue(self._list.isEmpty())

        for i in range(155):
            self._list.add(44)
        for i in range(155):
            self._list[i] = 33
        for i in range(155):
            self._list.removeAt(0)
        self.assertTrue(self._list.isEmpty())


    def testSize(self):
        self._list = DynamicArray()
        elems = [-76, 45, 66, 3, None, 54, 33]
        sz = 1
        for i in range(len(elems)):
            self._list.add(elems[i])
            self.assertEqual(len(self._list), sz)
            sz += 1


if __name__ == '__main__':
    unittest.main()