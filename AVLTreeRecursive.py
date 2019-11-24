class AVLTreeRecursive:
    class Node:
        def __init__(self, value):
            self.bf = self.height = 0
            self.left = self.right = None
            self.value = value

    def __init__(self):
        self.root = None
        self.node_count = 0

    def height(self):
        if self.root is None: return 0
        return self.root.height

    def __len__(self):
        return self.node_count

    def __bool__(self):
        return self.node_count != 0

    def contains(self, value):
        return self.__contains(self.root, value)

    def __contains(self, node, value):
        if node is None: return False

        if value < node.value: return self.__contains(node.left, value)
        if value > node.value: return self.__contains(node.right, value)

        return True

    def insert(self, value):
        if value is None: return False
        if not self.__contains(self.root, value):
            self.root = self.__insert(self.root, value)
            self.node_count += 1
            return True
        return False

    def __insert(self, node, value):
        if node is None: return self.Node(value)

        if value < node.value:
            node.left = self.__insert(node.left, value)
        else:
            node.right = self.__insert(node.right, value)

        self.update(node)

        return self.balance(node)

    def update(self, node):
        leftNodeHeight = -1 if node.left is None else node.left.height
        rightNodeHeight = -1 if node.right is None else node.right.height

        node.height = 1 + max(leftNodeHeight, rightNodeHeight)

        node.bf = rightNodeHeight - leftNodeHeight

    def balance(self, node):
        # Left heavy subtree
        if node.bf == -2:
            if node.left.bf <= 0:
                return self.leftLeftCase(node)
            else:
                return self.leftRightCase(node)
        # Right heavy subtree
        elif node.bf == 2:
            if node.right.bf >= 0:
                return self.rightRightCase(node)
            else:
                return self.rightLeftCase(node)
        # Node either has a balance factor of 0, +1, or -1 which is fine
        return node
        
    def leftLeftCase(self, node):
        return self.rightRotation(node)

    def leftRightCase(self, node):
        node.left = self.leftRotation(node.left)
        return self.leftLeftCase(node)

    def rightRightCase(self, node):
        return self.leftRotation(node)

    def rightLeftCase(self, node):
        node.right = self.rightRotation(node.right)
        return self.rightRightCase(node)

    def leftRotation(self, node):
        newParent = node.right
        node.right = newParent.left
        newParent.left = node
        self.update(node)
        self.update(newParent)
        return newParent

    def rightRotation(self, node):
        newParent = node.left
        node.left = newParent.right
        newParent.right = node
        self.update(node)
        self.update(newParent)
        return newParent

    def remove(self, value):
        if value is None:
            return False
        if self.contains(value):
            self.root = self.__remove(self.root, value)
            self.node_count -= 1
            return True
        return False
                
    def __remove(self, node, value):
        if node is None:
            return None
        # Dig into the left subtree, the value we are looking
        # for is smaller than the current value
        if value < node.value:
            node.left = self.__remove(node.left, value)
        # Dig into the right subtree, the value we are looking
        # for is larger than the current value
        elif value > node.value:
            node.right = self.__remove(node.right, value)
        # Found the node we wish to remove
        else:
            # This is the case with only a left subtree or
            # no subtree at all. In this situation, we just
            # swap the node we wish to remove with its left child.
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            # When removing a node from a binary tree with two links the
            # successor of the node being removed can either be the largest
            # value in the left subtree or the smallest value in the right
            # subtree. As a heuristic, we will remove from the subtree with
            # the greater height in the hope that this may help with balancing.
            else:
                # Choose to remove from left subtree
                if node.left.height > node.right.height:
                    # Swap the value of the successor into the node.
                    successorValue = self.find_max(node.left)
                    node.value = successorValue

                    # Find the largest node in the left subtree
                    node.left = self.__remove(node.left, successorValue)
                # Choose to remove from right subtree
                else:
                    # Swap the value of the successor into the node
                    successorValue = self.find_min(node.right)
                    node.value = successorValue

                    # Go into the right subtree and remove the leftmost
                    # we found and swap data with. This prevents us from having
                    # two nodes in our tree with the same value
                    node.right = self.__remove(node.right, successorValue)

        self.update(node)
        return self.balance(node)

    def find_min(self, node):
        while node.left is not None:
            node = node.left
        return node.value

    def find_max(self, node):
        while node.right is not None:
            node = node.right
        return node.value

    def __iter__(self):
        self.stack = []
        self.stack.append(self.root)
        self.trav = self.root
        return self

    def __next__(self):
        while self.trav is not None and self.trav.left is not None:
            self.stack.append(self.trav.left)
            self.trav = self.trav.left
        
        node = self.stack.pop()

        if node.right is not None:
            self.stack.append(node.right)
            self.trav = node.right

        return node.value

    def validateBSTInvariant(self, node):
        if node is None: return True

        val = node.value
        isValid = True

        if node.left is not None: 
            isValid = isValid and node.left.value < val
        if node.right is not None:
            isValid = isValid and node.right.value > val

        return isValid and self.validateBSTInvariant(node.left) and self.validateBSTInvariant(node.right)


