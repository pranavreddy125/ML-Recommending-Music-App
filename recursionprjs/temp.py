def remove_until_target_at_front(names_queue,target):
    if names_queue.is_empty():
        raise RuntimeError("nothing to remove")
    while not names_queue.is_empty():
        ans = names_queue.peek_front()
        if ans == target:
            return names_queue
        else:
            names_queue.dequeue()
    raise RuntimeError("not in queue")
        
