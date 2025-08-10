#not node based by array based --- j a list
class Minheap():
    def __init__(self):
        self._heap = []
    def insert(self,entry):
        self._heap.append(entry)
        self._upheap(len(self._heap)-1) #index entry was placed at
    def __len__(self):
        return len(self._heap)
    
    def pop(self): 
        if not self.heap:
            raise ValueError('no values in heap to look at')
        min_val = self.heap[0]
        end = self._heap.pop()
        if self._heap:
            self.heap[0] = end
            self._downheap(0)
            return min_val

    def peek_min(self):
        if not self._heap:
            raise ValueError('no values in heap to look at')
        return self._heap[0]
    def _upheap(self,index):
        if index == 0:
            return
        parent = (index-1)//2
        if self._heap[index] < self._heap[parent]:
            temp = self._heap[index]    #apple banana
            self._heap[index] = self._heap[parent]
            self._heap[parent] = temp
            self._upheap(parent)
    def _downheap(self,index):
        len_ = len(self._heap)
        left = 2*index + 1
        right = 2*index + 2
        smallest = index
        if left < len_ and self._heap[left] < self._heap[smallest]: #does it exists and is the left smmaller then the curr smallest
            smallest = left
        if right < len_ and self._heap[right] < self._heap[smallest]:
            smallest = right
        if smallest != index:
            temp = self._heap[index]    #manual swap again
            self._heap[index] = self._heap[smallest]
            self._heap[smallest] = temp
            self._downheap(smallest)



