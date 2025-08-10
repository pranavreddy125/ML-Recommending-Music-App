from node import Node
class Stack:
    def __init__(self):
        self.top = None
    def push(self,value):
        new = Node(value,self.top)
        self.top = new
    def peek(self):
        if self.top is None:
            raise ValueError("no items in stack")
        else:
            return self.top.value
    def pop(self):
        if self.top is None:
            raise ValueError("no items in stack")
        else:
            ans = self.top.value
            self.top = self.top.next
            return ans
    def is_empty(self):
        if self.top is None:
            return True
        else:
            return False