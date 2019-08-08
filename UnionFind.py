"""
UnionFind/Disjoint Set data structure implementation

"""

class UnionFind:
    def __init__(self, size):
        if size <= 0:
            raise ValueError

        # Tracks the number of components in the union find
        self.size = self.numComponents = size
        
        # Link to itself (self root)
        self.id = [i for i in range(self.size)]
        
        # Each component is originally of size one
        self.sz = [1 for i in range(self.size)]

    # Find which component/set 'p' belongs to, takes amortized constant time.
    def find(self, p):
        # Find the root of the component/set
        root = p
        while root != self.id[root]:
            root = self.id[root]
        
        # Compress the path leading back to the root.
        # Doing this operation is called "path compression"
        # and is what gives us amortized time complexity
        while p != root:
            next = self.id[p]
            self.id[p] = root
            p = next

        return root

    # This is an alternative recursive function for the find method
    # def find(self, p):
    #     if p == self.id[p]:
    #         return p
    #     return self.id[p] = self.find(self.id[p])

    # Return whether or not the elements 'p' and
    # 'q' are in the same components/set.
    def connected(self, p, q):
        return self.find(p) == self.find(q)

    # Return the size of the components/set 'p' belongs to
    def componentSize(self, p):
        return self.sz[self.find(p)]

    # Return the number of elements in this UnionFind/Disjoint set
    def __len__(self):
        return self.size

    # Returns the number of remaining components/sets
    def components(self):
        return self.numComponents

    # Unify the components/sets containing the elements 'p' and 'q'
    def unify(self, p, q):
        root1 = self.find(p)
        root2 = self.find(q)

        # These elements are already in the same group
        if root1 == root2:
            return

        # Merge smaller component/set into the larger one.
        if self.sz[root1] < self.sz[root2]:
            self.sz[root2] += self.sz[root1]
            self.id[root1] = root2
        else:
            self.sz[root1] += self.sz[root2]
            self.id[root2] = root1

        # Since the roots found are different we know that the
        # number of components/sets have decreased by one
        self.numComponents -= 1
    









