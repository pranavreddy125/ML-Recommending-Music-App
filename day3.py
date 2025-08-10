#lab2
# linkedstack.py

class Node:
    def __init__(self, entry):
        """
        A single node in a linked stack. 
        entry: whatever data this node holds (for us, a Function object).
        next: reference to the node underneath in the stack (initially None).
        """
        self.entry = entry
        self.next = None
