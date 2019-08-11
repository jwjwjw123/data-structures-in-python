"""
This file contains an implementation of a Binary Search Tree (BST) Any 
comparable data is allowed within this tree (numbers, strings, comparable 
Objects, etc...). Supported operations include adding, removing, height, and 
containment checks. Furthermore, multiple tree traversal Iterators are provided 
including: 1) Preorder traversal 2) Inorder traversal 3) Postorder traversal 4 
Levelorder traversal

"""
from collections import deque

class BinarySearchTree:
    
    def __init__(self, traverse="preorder"):
        # Tracks the number of nodes in this BST
        self.nodeCount = 0

        # This BST is a rooted tree so we maintain a handle on the root node
        self.root = None

        # The ways in which you can traverse the tree:
        # preorder, inorder, postorder and levelorder
        self.traverse = traverse

        self.isIterating = False
    
    # Internal node containing node references 
    # and the actual node data
    class Node:
        def __init__(self, left, right, elem):
            self.left = left
            self.right = right
            self.data = elem
            
    # Check if this binary tree has nodes
    def __bool__(self):
        return not self.nodeCount == 0

    # Get the number of nodes in this binary tree
    def __len__(self):
        return self.nodeCount

    # Add an element to this binary tree.
    def add(self, elem):
        currentNode = self.root
        if currentNode is None:
            self.root = self.Node(None, None, elem)
        else:
            while True:
                if elem < currentNode.data:
                    if currentNode.left is None:
                        currentNode.left = self.Node(None, None, elem)
                        break
                    else:
                        currentNode = currentNode.left
                else:
                    if currentNode.right is None:
                        currentNode.right = self.Node(None, None, elem)
                        break
                    else:
                        currentNode = currentNode.right
        self.nodeCount += 1
        
    # Remove the first instance from this binary tree if it exists, O(n)
    def remove(self, elem):
        currentNode = self.root
        parentNode = None
        while currentNode is not None:
            # find the node
            if elem < currentNode.data:
                parentNode = currentNode
                currentNode = currentNode.left
            elif elem > currentNode.data:
                parentNode = currentNode
                currentNode = currentNode.right
            # we found the node
            else:
                # replace the node with the smallest value of the right node
                if currentNode.left is not None and currentNode.right is not None:
                    currentNode.value = self.findMin(currentNode.right)
                    currentNode.right.remove(currentNode.data)
                # root node case
                elif parentNode is None:
                    if currentNode.left is not None:
                        self.root = currentNode.left
                        currentNode.data = currentNode.left.data
                        currentNode.right = currentNode.left.right
                        currentNode.left = currentNode.left.left
                    elif currentNode.right is not None:
                        self.root = currentNode.right
                        currentNode.data = currentNode.right.data
                        currentNode.left = currentNode.right.left
                        currentNode.right = currentNode.right.right
                    else:
                        currentNode.value = None
                        self.root = None
                elif parentNode.left == currentNode:
                    if currentNode.left is not None:
                        parentNode.left = currentNode.left
                    else:
                        parentNode.left = currentNode.right
                elif parentNode.right == currentNode:
                    if currentNode.left is not None:
                        parentNode.right = currentNode.left
                    else:
                        parentNode.right = currentNode.right
                self.nodeCount -= 1
                break

    # Helper method to find the leftmost node (which has the smallest value)
    def findMin(self, node):
        currentNode = node
        while currentNode.left is not None:
            currentNode = currentNode.left
        return currentNode.data

    # Returns true if the element exists in the tree
    def contains(self, elem):
        currentNode = self.root
        while currentNode is not None:
            if elem < currentNode.data:
                currentNode = currentNode.left
            elif elem > currentNode.data:
                currentNode = currentNode.right
            else:
                return True
        return False

    # Computes the height of the tree, O(n)
    def height(self):
        arr = deque([])
        if self.root is not None:
            arr.append(self.root)
        depth = 0
        while arr:
            temp = deque([])
            currentNode = arr.popleft()
            if currentNode.left is not None:
                temp.append(currentNode.left)
            if currentNode.right is not None:
                temp.append(currentNode.right)
            depth += 1
            arr = temp
        return depth

    def __iter__(self):
        self.expectedNodeCount = self.nodeCount
        self.isIterating = True

        if self.traverse == "preorder":
            self.stack1 = deque([])
            self.stack2 = deque([])
            self.stack1.append(self.root)
            while self.stack1:
                node = self.stack1.pop()
                if node is not None:
                    self.stack2.append(node.data)
                    if node.right is not None:
                        self.stack1.append(node.right)
                    if node.left is not None:
                        self.stack1.append(node.left)
            return iter(self.stack2)

        elif self.traverse == "inorder":
            self.stack1 = deque([])
            self.stack2 = deque([])
            current = self.root
            while True:
                if current is not None:
                    self.stack1.append(current)
                    current = current.left
                
                elif self.stack1:
                    current = self.stack1.pop()
                    self.stack2.append(current.data)
                    current = current.right
                
                else:
                    break
            return iter(self.stack2)

        elif self.traverse == "postorder":
            self.stack1 = deque([])
            self.stack2 = deque([])
            self.stack1.append(self.root)
            while self.stack1:
                node = self.stack1.pop()
                if node is not None:
                    self.stack2.append(node.data)
                    if node.left is not None:
                        self.stack1.append(node.left)
                    if node.right is not None:
                        self.stack1.append(node.right)
            return iter(self.stack2)

        elif self.traverse == "levelorder":
            self.stack1 = deque([])
            self.stack2 = deque([])
            self.stack1.append(self.root)
            while self.stack1:
                node = self.stack1.popleft()
                if node is not None:
                    self.stack2.append(node.data)
                    if node.left is not None:
                        self.stack1.append(node.left)
                    if node.right is not None:
                        self.stack1.append(node.right)
            return iter(self.stack2)

    def __next__(self):
        if not self.isIterating:
            raise TypeError("Object is not iterable")
        elif self.expectedNodeCount != self.nodeCount:
            raise RuntimeError("Changed size during iteration")
        elif len(self.stack2) == 0:
            raise StopIteration
        elif self.traverse == "preorder":
            return self.stack2.popleft()
        
        elif self.traverse == "inorder":
            return self.stack2.popleft()
        
        elif self.traverse == "postorder":
            return self.stack2.pop()

        elif self.traverse == "levelorder":
            return self.stack2.popleft()
        
                

    


