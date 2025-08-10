
from binarynode import BinaryNode
#never did 1/2 child cases
class BST:
    def __init__(self):
        self._root = None

    def add(self, item):
        if self._root is None:
            self._root = BinaryNode(item)
        else:
            self._rec_add(item,self._root)
        
    def _rec_add(self,item,cur_node):       ###fix
        if item < cur_node.entry:
            if cur_node.left is None:
                cur_node.left = BinaryNode(item)
            else:
                self._rec_add(item,cur_node.left)
        if item > cur_node.entry:
            if cur_node.right is None:
                cur_node.right = BinaryNode(item)
            else:
                self._rec_add(item,cur_node.right)
        else:
            self._root = BinaryNode(item)

    def search(self, key):
        return self._rec_search(key, self._root)

    def _rec_search(self, key, cur_node):
        if cur_node is None:
            return False
        if cur_node.entry == key:
            return True
        if cur_node.entry > key:
            return self._rec_search(key,cur_node.left) 
        if cur_node.entry < key:
            return self._rec_search(key,cur_node.right) 
    def remove(self,key):
        if key is None:
            raise ValueError("nothing to remove")
        return self._rec_remove(key,self._root)
    def _rec_remove(self,key,cur_node):
        # 1) Empty subtree – nothing to delete
        if cur_node is None:
            return None

    # 2) Descend left or right until you find the node
        if key < cur_node.entry:
            cur_node.left  = self._rec_remove(key, cur_node.left)
            return cur_node
        elif key > cur_node.entry:
            cur_node.right = self._rec_remove(key, cur_node.right)
            return cur_node

    # 3) cur_node.entry == key → this is the node to delete

    # --- 0-child case (leaf) ---
    # neither left nor right exist → simply remove it
        if cur_node.left is None and cur_node.right is None:
            return None

    # --- 1-child cases ---
    # exactly one child exists → splice that child up
        if cur_node.left is None:
        # only right child
            return cur_node.right
        if cur_node.right is None:
        # only left child
            return cur_node.left

    # --- 2-child case ---
    # find in-order successor: smallest node in right subtree
        succ = cur_node.right
        while succ.left is not None:
            succ = succ.left
    # copy its value into this node
        cur_node.entry = succ.entry
    # then delete the successor node from the right subtree
        cur_node.right = self._rec_remove(succ.entry, cur_node.right)
        return cur_node
    def copy(self):
        new_tree = BST()
        new_tree._root = self._rec_copy(self._root)
        return new_tree
    def _rec_copy(self,node):
        if node is None:
            return None
        new_node = BinaryNode(node.entry)
        new_node.left = self._rec_copy(node.left)
        new_node.right = self._rec_copy(node.right)
        return new_node
    def preorder(self,ans):
        self._rec_preorder(self._root,ans)
    def _rec_preorder(self,cur_node,ans):
        if cur_node is not None:
            ans(cur_node.entry)
            self._rec_preorder(cur_node.left,ans)
            self._rec_preorder(cur_node.right,ans)



