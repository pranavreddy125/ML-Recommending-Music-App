from node import Node
from queue import Queue
line = Queue()
while True:
    print("1) Add person\n 2) Call next\n 3) Next person\n 4) Line empty?\n 5) Exit")
    choice = int(input("give a number: "))
    if choice == 1:
        ans = input("enter a name: ")
        line.enqueue(ans)
    elif choice == 2:
        ppl = line.dequeue()
        print(f"{ppl} has been called")
    elif choice == 3:
        ppl = line.peek()
        print(f"{ppl} is in front of line")
    elif choice == 4:
        if line.is_empty():
            print("is empty")
        else:
            print('not empty')
    elif choice == 5:
        break
    else:
        print("invalid choice try again")