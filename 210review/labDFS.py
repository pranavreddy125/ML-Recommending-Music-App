def rec_dfs(row, col):
    val = grid[row][col]
    if row<0 or row>=len(grid) or col<0 or col>= len(grid[0]):
        return
    if val != 1:
        return
    else:
        grid[row][col] = 2
        rec_dfs(row-1,col)
        rec_dfs(row+1,col)
        rec_dfs(row,col-1)
        rec_dfs(row,col+1)
#recursive ^
rows = int(input("enter rows: "))
cols = int(input("enter cols: "))
grid = []
for i in range(rows):
    row = list(map(int, input().split()))   #map fn
    grid.append(row)
start_row = int(input("Enter starting row: "))  #coord
start_col = int(input("Enter starting column: "))
rec_dfs(start_row,start_col)
for row in grid:
    print(row)