import unittest
from UnionFind import *

class UnionFindTest(unittest.TestCase):
    def testNumComponents(self):
        uf = UnionFind(5)
        self.assertEqual(uf.components(), 5)

        uf.unify(0, 1)
        self.assertEqual(uf.components(), 4)

        uf.unify(1, 0)
        self.assertEqual(uf.components(), 4)

        uf.unify(1, 2)
        self.assertEqual(uf.components(), 3)

        uf.unify(0, 2)
        self.assertEqual(uf.components(), 3)

        uf.unify(2, 1)
        self.assertEqual(uf.components(), 3)

        uf.unify(3, 4)
        self.assertEqual(uf.components(), 2)

        uf.unify(4, 3)
        self.assertEqual(uf.components(), 2)

        uf.unify(1, 3)
        self.assertEqual(uf.components(), 1)

        uf.unify(4, 0)
        self.assertEqual(uf.components(), 1)

    def testComponentSize(self):
        uf = UnionFind(5)
        self.assertEqual(uf.componentSize(1), 1)
        self.assertEqual(uf.componentSize(2), 1)
        self.assertEqual(uf.componentSize(0), 1)
        self.assertEqual(uf.componentSize(3), 1)
        self.assertEqual(uf.componentSize(4), 1)

        uf.unify(0, 1)
        self.assertEqual(uf.componentSize(0), 2)
        self.assertEqual(uf.componentSize(1), 2)
        self.assertEqual(uf.componentSize(2), 1)
        self.assertEqual(uf.componentSize(3), 1)
        self.assertEqual(uf.componentSize(4), 1)

        uf.unify(1, 0)
        self.assertEqual(uf.componentSize(0), 2)
        self.assertEqual(uf.componentSize(1), 2)
        self.assertEqual(uf.componentSize(2), 1)
        self.assertEqual(uf.componentSize(3), 1)
        self.assertEqual(uf.componentSize(4), 1)

        uf.unify(1, 2)
        self.assertEqual(uf.componentSize(0), 3)
        self.assertEqual(uf.componentSize(1), 3)
        self.assertEqual(uf.componentSize(2), 3)
        self.assertEqual(uf.componentSize(3), 1)
        self.assertEqual(uf.componentSize(4), 1)

        uf.unify(0, 2)
        self.assertEqual(uf.componentSize(0), 3)
        self.assertEqual(uf.componentSize(1), 3)
        self.assertEqual(uf.componentSize(2), 3)
        self.assertEqual(uf.componentSize(3), 1)
        self.assertEqual(uf.componentSize(4), 1)

        uf.unify(2, 1)
        self.assertEqual(uf.componentSize(0), 3)
        self.assertEqual(uf.componentSize(1), 3)
        self.assertEqual(uf.componentSize(2), 3)
        self.assertEqual(uf.componentSize(3), 1)
        self.assertEqual(uf.componentSize(4), 1)

        uf.unify(3, 4)
        self.assertEqual(uf.componentSize(0), 3)
        self.assertEqual(uf.componentSize(1), 3)
        self.assertEqual(uf.componentSize(2), 3)
        self.assertEqual(uf.componentSize(3), 2)
        self.assertEqual(uf.componentSize(4), 2)

        uf.unify(4, 3)
        self.assertEqual(uf.componentSize(0), 3)
        self.assertEqual(uf.componentSize(1), 3)
        self.assertEqual(uf.componentSize(2), 3)
        self.assertEqual(uf.componentSize(3), 2)
        self.assertEqual(uf.componentSize(4), 2)

        uf.unify(1, 3)
        self.assertEqual(uf.componentSize(0), 5)
        self.assertEqual(uf.componentSize(1), 5)
        self.assertEqual(uf.componentSize(2), 5)
        self.assertEqual(uf.componentSize(3), 5)
        self.assertEqual(uf.componentSize(4), 5)

        uf.unify(4, 0)
        self.assertEqual(uf.componentSize(0), 5)
        self.assertEqual(uf.componentSize(1), 5)
        self.assertEqual(uf.componentSize(2), 5)
        self.assertEqual(uf.componentSize(3), 5)
        self.assertEqual(uf.componentSize(4), 5)

    def testConnectivity(self):
        sz = 7
        uf = UnionFind(sz)
        for i in range(sz):
            self.assertTrue(uf.connected(i, i))

        uf.unify(0, 2)

        self.assertTrue(uf.connected(0, 2))
        self.assertTrue(uf.connected(2, 0))

        self.assertFalse(uf.connected(0, 1))
        self.assertFalse(uf.connected(3, 1))
        self.assertFalse(uf.connected(6, 4))
        self.assertFalse(uf.connected(5, 0))

        for i in range(sz):
            self.assertTrue(uf.connected(i, i))

        uf.unify(3, 1)

        self.assertTrue(uf.connected(0, 2))
        self.assertTrue(uf.connected(2, 0))
        self.assertTrue(uf.connected(1, 3))
        self.assertTrue(uf.connected(3, 1))
    
        self.assertFalse(uf.connected(0, 1))
        self.assertFalse(uf.connected(1, 2))
        self.assertFalse(uf.connected(2, 3))
        self.assertFalse(uf.connected(1, 0))
        self.assertFalse(uf.connected(2, 1))
        self.assertFalse(uf.connected(3, 2))
    
        self.assertFalse(uf.connected(1, 4))
        self.assertFalse(uf.connected(2, 5))
        self.assertFalse(uf.connected(3, 6))

        for i in range(sz):
            self.assertTrue(uf.connected(i, i))
        
        uf.unify(2, 5)

        self.assertTrue(uf.connected(0, 2))
        self.assertTrue(uf.connected(2, 0))
        self.assertTrue(uf.connected(1, 3))
        self.assertTrue(uf.connected(3, 1))
        self.assertTrue(uf.connected(0, 5))
        self.assertTrue(uf.connected(5, 0))
        self.assertTrue(uf.connected(5, 2))
        self.assertTrue(uf.connected(2, 5))
    
        self.assertFalse(uf.connected(0, 1))
        self.assertFalse(uf.connected(1, 2))
        self.assertFalse(uf.connected(2, 3))
        self.assertFalse(uf.connected(1, 0))
        self.assertFalse(uf.connected(2, 1))
        self.assertFalse(uf.connected(3, 2))
    
        self.assertFalse(uf.connected(4, 6))
        self.assertFalse(uf.connected(4, 5))
        self.assertFalse(uf.connected(1, 6))

        for i in range(sz):
            self.assertTrue(uf.connected(i, i))
        
        # Connect everything
        uf.unify(1, 2)
        uf.unify(3, 4)
        uf.unify(4, 6)

        for i in range(sz):
            for j in range(sz):
                self.assertTrue(uf.connected(i, j))

    def testSize(self):
        uf = UnionFind(5)
        self.assertEqual(len(uf), 5)
        uf.unify(0, 1)
        uf.find(3)
        self.assertEquals(len(uf), 5)
        uf.unify(1, 2)
        self.assertEquals(len(uf), 5)
        uf.unify(0, 2)
        uf.find(1)
        self.assertEquals(len(uf), 5)
        uf.unify(2, 1)
        self.assertEquals(len(uf), 5)
        uf.unify(3, 4)
        uf.find(0)
        self.assertEquals(len(uf), 5)
        uf.unify(4, 3)
        uf.find(3)
        self.assertEquals(len(uf), 5)
        uf.unify(1, 3)
        self.assertEquals(len(uf), 5)
        uf.find(2)
        uf.unify(4, 0)
        self.assertEquals(len(uf), 5)

    def testBadUnionFindCreation(self):
        self.assertRaises(ValueError, UnionFind, -1)
        self.assertRaises(ValueError, UnionFind, -3463)
        self.assertRaises(ValueError, UnionFind, 0)


if __name__ == "__main__":
    unittest.main()
