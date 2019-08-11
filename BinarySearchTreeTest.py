import unittest
import random
from collections import deque
from BinarySearchTree import BinarySearchTree

class TestTreeNode:
    def __init__(self, data, left, right):
        self.data = data
        self.left = left
        self.right = right
    
    @staticmethod
    def add(node, data):
        if node == None:
            node = TestTreeNode(data, None, None)
        else:
            # Place lower elem values on left
            if data < node.data:
                node.left = TestTreeNode.add(node.left, data)
            else:
                node.right = TestTreeNode.add(node.right, data)
        return node

    @staticmethod
    def preOrder(lst, node):
        if node is None:
            return

        lst.append(node.data)

        if node.left is not None:
            TestTreeNode.preOrder(lst, node.left)
        if node.right is not None:
            TestTreeNode.preOrder(lst, node.right)

    @staticmethod
    def inOrder(lst, node):
        if node is None:
            return

        if node.left is not None:
            TestTreeNode.inOrder(lst, node.left)
        lst.append(node.data)
        if node.right is not None:
            TestTreeNode.inOrder(lst, node.right)

    @staticmethod
    def postOrder(lst, node):
        if node is None:
            return
        if node.left is not None:
            TestTreeNode.postOrder(lst, node.left)
        if node.right is not None:
            TestTreeNode.postOrder(lst, node.right)
        lst.append(node.data)

    @staticmethod    
    def levelOrder(lst, node):
        q = deque([])
        if node is not None:
            q.append(node)
        while q:
            node = q.popleft()
            lst.append(node.data)
            if node.left is not None:
                q.append(node.left)
            if node.right is not None:
                q.append(node.right)



class BinarySearchTreeTest(unittest.TestCase):
    LOOPS = 1000

    def testIsEmpty(self):
        tree = BinarySearchTree() 
        self.assertTrue(not tree)

        tree.add("Hello World!")
        self.assertFalse(not tree)

    def testSize(self):
        tree = BinarySearchTree()
        # Tree should look like:
        #        M
        #      J  S
        #    B   N Z
        #  A
        
        # No tree
        self.assertEqual(len(tree), 0)

        # Layer One
        tree.add("M")
        self.assertEqual(len(tree), 1)

        # Layer Two
        tree.add("J")
        self.assertEqual(len(tree), 2)
        tree.add("S")
        self.assertEqual(len(tree), 3)

        # Layer Three
        tree.add("B")
        self.assertEqual(len(tree), 4)
        tree.add("N")
        self.assertEqual(len(tree), 5)
        tree.add("Z")
        self.assertEqual(len(tree), 6)

        # Layer 4
        tree.add("A")
        self.assertEqual(len(tree), 7)

    def testHeight(self):
        tree = BinarySearchTree()
        # Tree should look like:
        #        M
        #      J  S
        #    B   N Z
        #  A

        # No tree
        self.assertEqual(tree.height(), 0)

        # Layer One
        tree.add("M")
        self.assertEqual(tree.height(), 1)

        # Layer Two
        tree.add("J")
        self.assertEqual(tree.height(), 2)
        tree.add("S")
        self.assertEqual(tree.height(), 2)

        # Layer Three
        tree.add("B")
        self.assertEqual(tree.height(), 3)
        tree.add("N")
        self.assertEqual(tree.height(), 3)
        tree.add("Z")
        self.assertEqual(tree.height(), 3)

        # Layer 4
        tree.add("A")
        self.assertEqual(tree.height(), 4)

    def testRemove(self):
        # Try removing an element which doesn't exist
        tree = BinarySearchTree()
        tree.add('A')
        self.assertEqual(len(tree), 1)
        tree.remove('B')
        self.assertEqual(len(tree), 1)

        # Try removing an element which does exist
        tree.add('B')
        self.assertEqual(len(tree), 2)
        tree.remove('B')
        self.assertEqual(len(tree), 1)
        self.assertEqual(tree.height(), 1)

        # Try removing the root
        tree.remove('A')
        self.assertEqual(len(tree), 0)
        self.assertEqual(tree.height(), 0)

    def testContains(self):
        # Set up tree
        tree = BinarySearchTree()

        tree.add('B')
        tree.add('A')
        tree.add('C')

        # Try looking for an element which doesn't exist
        self.assertFalse(tree.contains('D'))

        # Try looking for an element which exists in the root
        self.assertTrue(tree.contains('B'))

        # Try looking for an element which exists as the left child of the root
        self.assertTrue(tree.contains('A'))

        # Try looking for an element which exists as the right child of the root
        self.assertTrue(tree.contains('C'))

    def testRuntimeErrorPreOrder(self):
        bst = BinarySearchTree("preorder")

        bst.add(1)
        bst.add(2)
        bst.add(3)

        iter(bst)

        bst.add(0)
        self.assertRaises(RuntimeError, next, bst)

    def testRuntimeErrorInOrder(self):
        bst = BinarySearchTree("inorder")

        bst.add(1)
        bst.add(2)
        bst.add(3)

        iter(bst)

        bst.add(0)
        self.assertRaises(RuntimeError, next, bst)

    def testRuntimeErrorPostOrder(self):
        bst = BinarySearchTree("postorder")

        bst.add(1)
        bst.add(2)
        bst.add(3)

        iter(bst)

        bst.add(0)
        self.assertRaises(RuntimeError, next, bst)

    def testRuntimeErrorLevelOrder(self):
        bst = BinarySearchTree("levelorder")

        bst.add(1)
        bst.add(2)
        bst.add(3)

        iter(bst)

        bst.add(0)
        self.assertRaises(RuntimeError, next, bst)

    def testRuntimeErrorRemovingPreOrder(self):
        bst = BinarySearchTree("preorder")

        bst.add(1)
        bst.add(2)
        bst.add(3)

        iter(bst)

        bst.remove(2)
        self.assertRaises(RuntimeError, next, bst)

    def testRuntimeErrorRemovingInOrder(self):
        bst = BinarySearchTree("inorder")

        bst.add(1)
        bst.add(2)
        bst.add(3)

        iter(bst)

        bst.remove(2)
        self.assertRaises(RuntimeError, next, bst)

    def testRuntimeErrorRemovingPostOrder(self):
        bst = BinarySearchTree("postorder")

        bst.add(1)
        bst.add(2)
        bst.add(3)

        iter(bst)

        bst.remove(2)
        self.assertRaises(RuntimeError, next, bst)

    def testRuntimeErrorRemovingLevelOrder(self):
        bst = BinarySearchTree("levelorder")

        bst.add(1)
        bst.add(2)
        bst.add(3)

        iter(bst)
        bst.remove(2)

        self.assertRaises(RuntimeError, next, bst)

    def randomRemoveTests(self):
        for i in range(self.LOOPS):
            size = i
            tree = BinarySearchTree()
            lst = self.genRandList(size)
            for idx, value in enumerate(lst):
                tree.add(value)
                self.assertEqual(len(tree), idx+1)
            random.shuffle(lst)
            for j in range(size):
                value = lst[j]
                self.assertTrue(tree.contains(value))

            # Remove all the elements we just placed in the tree
            for j in range(size):
                value = lst[j]
                tree.remove(value)
                self.assertFalse(tree.contains(value))
                self.assertEqual(len(tree), size-j-1)

            self.assertFalse(tree)

    def validateTreeTraversal(self, traverse, input):
        out = []
        expected = []
        testTree = None
        tree = BinarySearchTree(traverse=traverse)

        # Construct Binary tree and test tree
        for value in input:
            testTree = TestTreeNode.add(testTree, value)
            tree.add(value)
        
        # Generate the expected output for the particular traversal
        if traverse == "preorder":
            TestTreeNode.preOrder(expected, testTree)
        elif traverse == "inorder":
            TestTreeNode.inOrder(expected, testTree)
        elif traverse == "postorder":
            TestTreeNode.postOrder(expected, testTree)
        elif traverse == "levelorder":
            TestTreeNode.levelOrder(expected, testTree)
        
        # Get traversal output
        iter(tree)
        while True:
            curr = next(tree, None)
            if curr is not None:
                out.append(curr)
            else:
                break

        # The output and the expected size should be the same
        if len(out) != len(expected):
            return False

        # Compare output to expected
        for i in range(len(out)):
            if expected[i] != out[i]:
                return False
        
        return True

    def testPreOrderTraversal(self):
        for i in range(self.LOOPS):
            myInput = self.genRandList(i)
            self.assertTrue(self.validateTreeTraversal("preorder", myInput))

    def testInOrderTraversal(self):
        for i in range(self.LOOPS):
            myInput = self.genRandList(i)
            self.assertTrue(self.validateTreeTraversal("inorder", myInput))

    def testPostOrderTraversal(self):
        for i in range(self.LOOPS):
            myInput = self.genRandList(i)
            self.assertTrue(self.validateTreeTraversal("postorder", myInput))

    def testLevelOrderTraversal(self):
        for i in range(self.LOOPS):
            myInput = self.genRandList(i)
            self.assertTrue(self.validateTreeTraversal("levelorder", myInput))



    def genRandList(self, sz):
        lst = random.sample(range(0, sz), sz)
        return lst

if __name__ == "__main__":
    unittest.main()



