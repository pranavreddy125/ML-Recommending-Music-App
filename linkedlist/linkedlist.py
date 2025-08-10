from node import Node
class LinkedList:
    def __init__(self):
        self.head = None
        self._length = 0
    def length(self):
        return self._length
    def insert(self,index, entry):  #front back middle
        if index < 0 or index > self._length:
            raise RuntimeError("invlaid index")
        elif index == 0:        #front
            old = self.head
            new_node = Node(entry)
            self.head = new_node
            self.head.next = old
            self._length += 1
        elif index == self._length: #to the back
            new_node = Node(entry)
            if self.head is None:
                self.head = new_node
            else:
                curr = self.head
                while curr.next is not None: #get to back of list
                    curr = curr.next
                    curr.next = new_node
            self._length += 1
        else:
            new_node = Node(entry)
            curr = self.head
            for i in range(index-1):    #if 1-5 w/o 3, then land on 2 not 4
                curr = curr.next
            old = curr.next #old is pointing to 4
            new_node = old  #now new node is pointing at 4
            curr.next = new_node
            self._length +=1
    def remove(self,index):
        if index < 0 or index>self.length:
            raise RuntimeError("invalid index")
        elif index == 0:
            self.head = self.head.next
        else:
            for i in range(index-1):
                curr = curr.next
            remove = curr.next
            curr.next = remove.next
            self._length -=1
    def get_entry(self,index):
        if index < 0 or index>self.length:
            raise RuntimeError("invalid index")
        else:
            curr = self.head
            for i in range(index):
                curr = curr.next
            return curr.value
    def set_entry(self,index,entry):
        if index < 0 or index>self.length:
            raise RuntimeError("invalid index")
        else:
            curr = self.head
            for i in range(index):
                curr = curr.next
            ans = curr.value
            curr.value = entry
    def clear(self):
        self.head = None
        self._length = 0





