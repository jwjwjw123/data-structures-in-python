"""
A doubly linked list implementation

"""
class DoublyLinkedList:
    class Node:
        def __init__(self, data, prev, next):
            self.data = data
            self.prev = prev
            self.next = next

        def __str__(self):
            return str(self.data)
    
    def __init__(self):
        self.size = 0
        self.head = None
        self.tail = None

    def clear(self):
        trav = self.head
        while trav != None:
            next = trav.next
            trav.prev = trav.next = None
            trav.data = None
            trav = next
        self.head = self.tail = trav = None
        self.size = 0

    def __len__(self):
        return self.size
    
    def isEmpty(self):
        return self.size == 0

    def add(self, elem):
        self.addLast(elem)

    def addLast(self, elem):
        if self.isEmpty():
            self.head = self.tail = self.Node(elem, None, None)
        else:
            self.tail.next = self.Node(elem, self.tail, None)
            self.tail = self.tail.next
        self.size += 1

    def addFirst(self, elem):
        if self.isEmpty():
            self.head = self.tail = self.Node(elem, None, None)
        else:
            self.head.prev = self.Node(elem, None, self.head)
            self.head = self.head.prev
        self.size += 1

    def peekFirst(self):
        if self.isEmpty():
            raise RuntimeError("Empty List")
        return self.head.data

    def peekLast(self):
        if self.isEmpty():
            raise RuntimeError("Empty List")
        return self.tail.data

    def removeFirst(self):
        # Throw error if empty 
        if self.isEmpty():
            raise RuntimeError("Empty List")
        # Save the data to return later
        data = self.head.data
        # Shift head pointer to next node
        self.head = self.head.next
        self.size -= 1

        if self.isEmpty():
            self.tail = None
        else:
            self.head.prev = None
        
        return data

    def removeLast(self):
        if self.isEmpty():
            raise RuntimeError("Empty List")
        
        data = self.tail.data
        self.tail = self.tail.prev
        self.size -= 1

        if self.isEmpty():
            self.head = None
        else:
            # Delete the reference to the remove node
            self.tail.next = None

        return data

    def removeNode(self, node):
        # if the node to be removed is at either the head or the tail
        # remove them independently
        if node.prev == None:
            return self.removeFirst()
        if node.next == None:
            return self.removeLast()
        
        # Make the prev node points to the next node
        node.prev.next = node.next
        # Make the next node points to the prev node
        node.next.prev = node.prev

        data = node.data
        # Memory cleanup
        node.prev = node.next = None
        node = None
        self.size -= 1

        return data

    def removeAt(self, index):
        if index < 0 or index >= self.size:
            raise IndexError
        trav = None
        # Traverse from the front of the list
        if index < self.size // 2:
            trav = self.head
            for _ in range(index):
                trav = trav.next
        # Traverse from the back of the list
        else:
            trav = self.tail
            for _ in range(self.size - index - 1):
                trav = trav.prev
        return self.removeNode(trav)

    def remove(self, data):
        trav = self.head

        while trav is not None:
            if trav.data == data:
                return self.removeNode(trav)
            trav = trav.next

    def indexOf(self, elem):
        trav = self.head
        idx = 0

        while trav is not None:
            if trav.data == elem:
                return idx
            idx += 1
            trav = trav.next

        return -1

    def contains(self, elem):
        return self.indexOf(elem) != -1

    def __iter__(self):
        # To be used as pointer for iterator
        self._trav = self.head
        return self

    def __next__(self):
        if self._trav is not None:
            data = self._trav.data
            self._trav = self._trav.next
            return data
        else:
            raise StopIteration

    def __str__(self):
        trav = self.head
        result = "["
        while trav is not None:
            result += str(trav.data) + ", "
            trav = trav.next
        result = result[0:-2]
        result += "]"
        return result



