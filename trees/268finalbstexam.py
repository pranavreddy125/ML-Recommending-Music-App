#exam problem final 268
new_list = LinkedList()
def matches(the_bst,keys):
    try:
        ans = the_bst.search(keys)
        return ans
    except KeyError:
        return None
    
while head is not None:
    value = head.entry
    ans = matches(the_bst,value)
    if ans is not None:
        new_list.insert(ans)
    head = head.next










def matches(the_bst, keys):
    try:
        ans = the_bst.search(keys)
        return ans
    except KeyError:
        return None
new = LinkedList()
cur_node = keys.entry
while cur_node is not None:
    value = head.entry
    ans = matches(the_bst,value)
    if ans is None:
        return
    else:
        new.insert(ans)


def matches(the_bst,keys):
    try:
        ans = the_bst.search(keys)
        if ans is not None:
            return True
        else:
            False
    except ValueError:
new = LinkedList()

while head is not None:
    prev = head.entry
    ans = matches(the_bst, prev)
    if ans is None:
        pass
    else:
        new.insert(ans)



