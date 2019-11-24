import unittest
import random
import math
from bintrees import AVLTree
from AVLTreeRecursive import AVLTreeRecursive

class AVLTreeRecursiveTest(unittest.TestCase):
    MAX_RAND_NUM = 100000
    MIN_RAND_NUM = -100000
    TEST_SZ = 2500

    @classmethod
    def setUp(cls):
        cls.tree = AVLTreeRecursive()

    def testNullInsertion(self):
        self.assertFalse(self.tree.insert(None))

    def testNullRemoval(self):
        self.assertFalse(self.tree.remove(None))

    def testTreeContainsNull(self):
        self.assertFalse(self.tree.contains(None))

    def testLeftLeftCase(self):
        self.tree.insert(3)
        self.tree.insert(2)
        self.tree.insert(1)

        self.assertEqual(2, self.tree.root.value)
        self.assertEqual(1, self.tree.root.left.value)
        self.assertEqual(3, self.tree.root.right.value)

        self.assertIsNone(self.tree.root.left.left)
        self.assertIsNone(self.tree.root.left.right)
        self.assertIsNone(self.tree.root.right.left)
        self.assertIsNone(self.tree.root.right.right)

    def testLeftRightCase(self):
        self.tree.insert(3)
        self.tree.insert(1)
        self.tree.insert(2)

        self.assertEqual(2, self.tree.root.value)
        self.assertEqual(1, self.tree.root.left.value)
        self.assertEqual(3, self.tree.root.right.value)

        self.assertIsNone(self.tree.root.left.left)
        self.assertIsNone(self.tree.root.left.right)
        self.assertIsNone(self.tree.root.right.left)
        self.assertIsNone(self.tree.root.right.right)

    def testRightRightCase(self):
        self.tree.insert(1)
        self.tree.insert(2)
        self.tree.insert(3)

        self.assertEqual(2, self.tree.root.value)
        self.assertEqual(1, self.tree.root.left.value)
        self.assertEqual(3, self.tree.root.right.value)

        self.assertIsNone(self.tree.root.left.left)
        self.assertIsNone(self.tree.root.left.right)
        self.assertIsNone(self.tree.root.right.left)
        self.assertIsNone(self.tree.root.right.right)

    def testRightLeftCase(self):
        self.tree.insert(1)
        self.tree.insert(3)
        self.tree.insert(2)

        self.assertEqual(2, self.tree.root.value)
        self.assertEqual(1, self.tree.root.left.value)
        self.assertEqual(3, self.tree.root.right.value)

        self.assertIsNone(self.tree.root.left.left)
        self.assertIsNone(self.tree.root.left.right)
        self.assertIsNone(self.tree.root.right.left)
        self.assertIsNone(self.tree.root.right.right)

    def testRandomisedBalanceFactor(self):
        for _ in range(self.TEST_SZ):
            self.tree.insert(self.rand_val())
            self.assertTrue(self.validateBalanceFactorValues(self.tree.root))

    def testTreeHeight(self):
        for n in range(1, self.TEST_SZ + 1):
            self.tree.insert(self.rand_val())
            height = self.tree.height()
            # Get an upper bound on what the maximum height of
            # an AVL tree should be. Values were taken from:
            # https://en.wikipedia.org/wiki/AVL_tree#Comparison_to_other_structures
            c = 1.441
            b = -0.329
            upperBound = c * (math.log(n + 2.0) / math.log(2) + b)
            self.assertTrue(height < upperBound)    

    def testRandomisedValueInsertion(self):
        pytree = AVLTree()
        for _ in range(self.TEST_SZ):
            v = self.rand_val()
            self.tree.insert(v)
            pytree.insert(v, v)
            self.assertEqual(len(self.tree), len(pytree))
            self.assertTrue(self.tree.validateBSTInvariant(self.tree.root))

    def validateBalanceFactorValues(self, node):
        if node is None:
            return True
        if node.bf > 1 or node.bf < -1:
            return False
        return self.validateBalanceFactorValues(node.left) and self.validateBalanceFactorValues(node.right)

    def testRandomRemove(self):
        pytree = AVLTree()
        for i in range(self.TEST_SZ):
            size = i
            lst = self.gen_rand_list(size)
            for value in lst:
                self.tree.insert(value)
                pytree.insert(value, value)
            
            random.shuffle(lst)

            for j, value in enumerate(lst):
                pytree.remove(value)
                self.tree.remove(value)
                self.assertEqual(len(pytree), len(self.tree))
                self.assertEqual(size - j - 1, len(self.tree))
        self.assertTrue(not self.tree)


    def gen_rand_list(self, sz):
        lst = []
        for i in range(sz):
            lst.append(i)
        random.shuffle(lst)
        return lst

    def rand_val(self):
        return random.randint(self.MIN_RAND_NUM, self.MAX_RAND_NUM)



if __name__ == "__main__":
    unittest.main()