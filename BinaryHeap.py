"""
A min priority queue implementation using a binary heap.

"""

class BinaryHeap:
    def __init__(self, elems=None):
        # The number of elements currently inside the heap
        self.heapSize = 0
        # The internal capacity of the heap
        self.heapCapacity = 0
        # Construct a priority queue using heapify in O(n) time
        if elems: 
            self.heapSize = self.heapCapacity = len(elems)
            self.heap = []
            for i in range(self.heapSize):
                self.heap.append(elems[i])
            # Heapify process, O(n)
            for i in range(max(0, self.heapSize//2 - 1), -1, -1):
                self.sink(i)
        else:
            self.heap = []

    def __bool__(self):
        return not self.heapSize == 0

    def clear(self):
        for i in range(self.heapCapacity):
            self.heap[i] = None
        self.heapSize = 0

    def __len__(self):
        return self.heapSize

    def peek(self):
        if not self:
            return None
        return self.heap[0]
    
    def poll(self):
        return self.removeAt(0)

    def contains(self, elem):
        # Linear scan to check containment
        for i in range(self.heapSize):
            if self.heap[i] == elem:
                return True
        return False

    def add(self, elem):
        if elem is None:
            raise ValueError
        
        if self.heapSize < self.heapCapacity:
            self.heap[self.heapSize] = elem
        else:
            self.heap.append(elem)
            self.heapCapacity += 1
        
        self.swim(self.heapSize)
        self.heapSize += 1
    
    # Tests if the value of node i <= node j
    # This method assumes i and j are valid indices, O(1)
    def less(self, i, j):
        node1 = self.heap[i]
        node2 = self.heap[j]
        return node1 <= node2

    # Perform bottom up node swim, O(log(n))
    def swim(self, k):
        # Grab the index of the next parent node WRT k
        parent = (k - 1) // 2

        # Keep swimming while we have not reached the 
        # root and while we're less than our parent
        while k > 0 and self.less(k, parent):
            self.swap(parent, k)
            k = parent

            # Grab the index of the next parent node WRT k
            parent = (k - 1) // 2

    # Top down node sink, O(log(n))
    def sink(self, k):
        while True:
            left = 2 * k + 1 #  Left node
            right = 2 * k + 2 #  Right node
            smallest = left #  Assume left is the smallest node of the two children

            # Find which is smaller left or right
            # If right is smaller set smallest to be right
            if right < self.heapSize and self.less(right, left):
                smallest = right

            # Stop if we're outside the bounds of the tree
            # or stop early if we cannot sink k anymore
            if left >= self.heapSize or self.less(k, smallest):
                break

            # Move down the tree following the smallest node
            self.swap(smallest, k)
            k = smallest

    # Swap two nodes. Assume i and j are valid, O(1)
    def swap(self, i, j):
        elem_i = self.heap[i]
        elem_j = self.heap[j]

        self.heap[i] = elem_j
        self.heap[j] = elem_i

    def remove(self, elem):
        if elem is None:
            return False
        # Linear removal via search, O(n)
        for i in range(self.heapSize):
            if elem == self.heap[i]:
                return self.removeAt(i)
    
    # Removes a node at particular index, O(log(n))
    def removeAt(self, i):
        if not self:
            return None

        self.heapSize -= 1
        removed_data = self.heap[i]
        self.swap(i, self.heapSize)

        # Obliterate the value
        self.heap[self.heapSize] = None

        # Check if the last element was removed
        if i == self.heapSize:
            return removed_data
        elem = self.heap[i]

        # Try sinking element
        self.sink(i)

        # If sinking did not work, try swimming
        if self.heap[i] == elem:
            self.swim(i)

        return removed_data

    # Recursively check if this heap is a min heap 
    # This method is just for testing purposes to make
    # sure the heap invariant is still being maintained 
    # Call this method with k=0 to start at the root
    def isMinHeap(self, k):
        # If we are outside the bounds of the heap return true
        if k >= self.heapSize:
            return True
        
        left = 2 * k + 1
        right = 2 * k + 2

        # Make sure that the current node k is less than 
        # both of its children left, and right if they exist
        # return false otherwise to indicate an invalid heap
        if left < self.heapSize and not self.less(k, left):
            return False

        if right < self.heapSize and not self.less(k, right):
            return False

        # Recurse on both children to make sure they are also valid heaps
        return self.isMinHeap(left) and self.isMinHeap(right)

    def __str__(self):
        return str(self.heap)

