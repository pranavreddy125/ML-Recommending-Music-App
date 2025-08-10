from node import Node
class BinaryTree:
    def __init__(self):
        self._root = None
    def add(self,entry):
        #base case
        if self.root is None:
            self.root = Node(entry)
        else:
            self._rec_add(entry,self._root)
    def _rec_add(self,entry,node):
        if node.left is None:
            self._root = Node(entry)
        else:
            self._rec_add(entry, self._root)
    def search(self,target):
        return self._rec_search(target,self._root)
    def _rec_search(self,target,cur_node):
        if cur_node is None:
            return False
        elif cur_node == target:
            return True
        else:
            in_lst = self._rec_search(self,target,cur_node.left)
            in_rst = self._rec_search(self,target,cur_node.right)
            return in_lst or in_rst
    def count(self):
        return self.rec_count_node(self._root)
    def _rec_count_node(self,cur_node):
        if cur_node is None:
            return 0
        left_ct = self._rec_count_node(cur_node.left)
        right_ct = self._rec_count_node(cur_node.right)
        return 1 + left_ct + right_ct
