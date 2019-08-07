from BinaryHeap import *
import unittest
import heapq
import random

class BinaryHeapTest(unittest.TestCase):
    LOOPS = 1000
    MAX_SZ = 100

    def testEmpty(self):
        q = BinaryHeap()
        self.assertEqual(len(q), 0)
        self.assertTrue(not q)
        self.assertEqual(q.poll(), None)
        self.assertEqual(q.peek(), None)

    def testHeapProperty(self):
        q = BinaryHeap()
        nums = [3, 2, 5, 6, 7, 9, 4, 8, 1]

        # Try manually creating heap
        for n in nums:
            q.add(n)

        for i in range(1, 10):
            self.assertTrue(i == q.poll())

        q.clear()

        # Try heapify constructor
        q = BinaryHeap(elems=nums)
        for i in range(1, 10):
            self.assertTrue(i == q.poll())

    def testHeapify(self):
        for i in range(1, self.LOOPS):
            lst = self.genRandList(i)
            pq = BinaryHeap(elems=lst)
            pq2 = []
            for x in lst:
                heapq.heappush(pq2, x)
        
            self.assertTrue(pq.isMinHeap(0))
            while pq2:
                self.assertEqual(pq.poll(), heapq.heappop(pq2))

    def testClear(self):
        strs = ["aa", "bb", "cc", "dd", "ee"]
        q = BinaryHeap(strs)
        q.clear()
        self.assertEqual(len(q), 0)
        self.assertTrue(not q)

    def testContainment(self):
        strs = ["aa", "bb", "cc", "dd", "ee"]
        q = BinaryHeap(strs)
        q.remove("aa")
        self.assertFalse(q.contains("aa"))
        q.remove("bb")
        self.assertFalse(q.contains("bb"))
        q.remove("cc")
        self.assertFalse(q.contains("cc"))
        q.remove("dd")
        self.assertFalse(q.contains("dd"))
        q.remove("ee")
        self.assertFalse(q.contains("ee"))

    def testContainmentRandomised(self):
        for i in range(self.LOOPS):
            randNums = self.genRandList(100)
            built_in_pq = []
            pq = BinaryHeap()
            for j in range(len(randNums)):
                heapq.heappush(built_in_pq, randNums[j])
                pq.add(randNums[j])

            for j in range(len(randNums)):
                randVal = randNums[j]
                self.assertEqual(pq.contains(randVal), randVal in built_in_pq)
                pq.remove(randVal)
                built_in_pq.remove(randVal)
                self.assertEqual(pq.contains(randVal), randVal in built_in_pq)

    def sequentialRemoving(self, arr, removeOrder):
        self.assertEqual(len(arr), len(removeOrder))
        pq = BinaryHeap(arr)
        built_in_pq = []
        for val in arr:
            heapq.heappush(built_in_pq, val)
        
        self.assertTrue(pq.isMinHeap(0))

        for i in range(len(removeOrder)):
            elem = removeOrder[i]

            self.assertTrue(pq.peek() == built_in_pq[0])
            self.assertEqual(pq.remove(elem), built_in_pq.pop(built_in_pq.index(elem)))
            self.assertTrue(len(pq) == len(built_in_pq))
            self.assertTrue(pq.isMinHeap(0))

        self.assertTrue(not pq)

    def testRemoving(self):
        arr = [1, 2, 3, 4, 5, 6, 7]
        removeOrder = [1, 3, 6, 4, 5, 7, 2]
        self.sequentialRemoving(arr, removeOrder)

        arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        removeOrder = [7, 4, 6, 10, 2, 5, 11, 3, 1, 8, 9]
        self.sequentialRemoving(arr, removeOrder)

        arr = [8, 1, 3, 3, 5, 3]
        removeOrder = [3, 3, 5, 8, 1, 3]
        self.sequentialRemoving(arr, removeOrder)

        arr = [7, 7, 3, 1, 1, 2]
        removeOrder = [2, 7, 1, 3, 7, 1]
        self.sequentialRemoving(arr, removeOrder)

        arr = [32, 66, 93, 42, 41, 91, 54, 64, 9, 35]
        removeOrder = [64, 93, 54, 41, 35, 9, 66, 42, 32, 91]
        self.sequentialRemoving(arr, removeOrder)

    def testRemovingDuplicates(self):
        arr = [2, 7, 2, 11, 7, 13, 2]
        pq = BinaryHeap(arr)

        self.assertTrue(pq.peek() == 2)
        pq.add(3)

        self.assertTrue(pq.poll() == 2)
        self.assertTrue(pq.poll() == 2)
        self.assertTrue(pq.poll() == 2)
        self.assertTrue(pq.poll() == 3)
        self.assertTrue(pq.poll() == 7)
        self.assertTrue(pq.poll() == 7)
        self.assertTrue(pq.poll() == 11)
        self.assertTrue(pq.poll() == 13)

    def testRandomisedPolling(self):
        for i in range(self.LOOPS):
            sz = i
            randNums = self.genRandList(sz)
            pq1 = []
            pq2 = BinaryHeap()

            # Add all the elements to both priority queues
            for val in randNums:
                heapq.heappush(pq1, val)
                pq2.add(val)

            while pq1:
                self.assertTrue(pq2.isMinHeap(0))
                self.assertEqual(len(pq1), len(pq2))
                self.assertEqual(pq1[0], pq2.peek())
                self.assertEqual(pq1[0] in pq1, pq2.contains(pq2.peek()))

                v1 = heapq.heappop(pq1)
                v2 = pq2.poll()

                self.assertEqual(v1, v2)
                self.assertEqual(pq1[0] if len(pq1) > 0 else None, pq2.peek())
                self.assertEqual(len(pq1), len(pq2))
                self.assertTrue(pq2.isMinHeap(0))

    def testRandomisedRemoving(self):
        for i in range(self.LOOPS):
            sz = i
            randNums = self.genRandList(sz)
            pq1 = []
            pq2 = BinaryHeap()

            # Add all the elements to both priority queues
            for val in randNums:
                heapq.heappush(pq1, val)
                pq2.add(val)

            random.shuffle(randNums)
            index = 0
            
            while pq1:
                removeNum = randNums[index]
                index += 1

                self.assertTrue(pq2.isMinHeap(0))
                self.assertEqual(len(pq1), len(pq2))
                self.assertEqual(pq1[0], pq2.peek())
                pq1.remove(removeNum)
                heapq.heapify(pq1)
                pq2.remove(removeNum)
                self.assertEqual(pq1[0] if len(pq1) > 0 else None, pq2.peek())
                self.assertEqual(len(pq1), len(pq2))
                self.assertTrue(pq2.isMinHeap(0))

    def testPQReusability(self):
        SZs = self.genUniqueRandList(self.LOOPS)

        PQ = []
        pq = BinaryHeap()

        for sz in SZs:
            pq.clear()
            PQ.clear()

            nums = self.genRandList(sz)
            for n in nums:
                pq.add(n)
                heapq.heappush(PQ, n)

            random.shuffle(nums)

            for i in range(sz//2):
                # Sometimes add a new number into the BinaryHeap
                if (0.25 < random.random()):
                    randNum = int(random.random() * 10000)
                    heapq.heappush(PQ, randNum)
                    pq.add(randNum)

                removeNum = nums[i]

                self.assertTrue(pq.isMinHeap(0))
                self.assertEqual(len(PQ), len(pq))
                self.assertEqual(PQ[0], pq.peek())

                PQ.remove(removeNum)
                heapq.heapify(PQ)
                pq.remove(removeNum)

                self.assertEqual(PQ[0], pq.peek())
                self.assertEqual(len(PQ), len(pq))
                self.assertTrue(pq.isMinHeap(0))





    # Generate a list of random numbers
    def genRandList(self, sz):
        lst = []
        for _ in range(sz):
            lst.append(int(random.random() * self.MAX_SZ))
        return lst
    
    # Generate a list of unique random numbers
    def genUniqueRandList(self, sz):
        lst = []
        for i in range(sz):
            lst.append(i)
        random.shuffle(lst)
        return lst

if __name__ == "__main__":
    unittest.main()