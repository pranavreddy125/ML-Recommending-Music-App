from node import Node
class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
    def enqueue(self,target):
        if self.rear is None and self.front is None:
            new = Node(target,self.rear)
            self.rear = new
            self.front = new
        else:
            new = Node(target,self.rear)
            self.rear.next = new #queues are left to right
            self.rear = new
    def dequeue(self):
        if self.rear is None and self.front is None:
            raise ValueError("no values in queue to remove")
        else:
            ans = self.front.value
            self.front = self.front.next
            if self.rear is None and self.front is None:
                self.rear = None
            return ans
    def peek(self):
        if self.front is None and self.rear is None:
            raise ValueError("no values in queue")
        else:
            ans = self.front.value
            return ans
    def is_empty(self):
        if self.front is None and self.rear is None:
            return True
        else:
            return False
