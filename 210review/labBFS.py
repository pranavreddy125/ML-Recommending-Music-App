#do user input- like lab 3, given grid change all neighbors to 2 if 1 before
rows = int(input("Enter number of rows: "))
cols = int(input("Enter number of columns: "))

print("Enter the grid row by row (e.g. 1 0 1):")
grid = []
for _ in range(rows):
    row = list(map(int, input().split()))
    grid.append(row)

start_row = int(input("Enter starting row: "))  #coord
start_col = int(input("Enter starting column: "))
#queue - fifo
queue = [(start_row,start_col)]
while queue is not None:
    row,col = queue.pop(0)  #unpacks properly
    if 0 <= row < len(grid) and 0 <= col < len(grid[0]) and grid[row][col] == 1: #grid is j var name
        grid[row][col] = 2  # ^ bounds check
        queue.append((row-1, col)) #up
        queue.append((row + 1, col))  # down
        queue.append((row, col - 1))  # left
        queue.append((row, col + 1))

