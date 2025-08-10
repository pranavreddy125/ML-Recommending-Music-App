# 1) Define a simple maze
grid = [
    list("HHHHHHH"),
    list("H     H"),
    list("H HHH H"),
    list("H     H"),
    list("HHHHHHH"),
]

# 2) Function to print the grid
def print_grid(grid_):
    for row in grid_:
        print(''.join(row))


# 3) Recursive flood-fill
def flood_fill(grid_, row, col):
    num_row = len(grid_)
    num_col = len(grid_[0])
    if row < 0 or row>=num_row:
        return None
    if col < 0 or col>=num_col:
        return None
    if grid_[row][col] != ' ':
        return None
    else:
        grid_[row][col] = '~'
    flood_fill(grid_, row-1, col)   # up
    flood_fill(grid_, row,   col+1) # right
    flood_fill(grid_, row+1, col)   # down
    flood_fill(grid_, row,   col-1) # left


# 4) Main logic
def main():
    print("Before flood:")
    print_grid(grid)

    start_r, start_c = 1, 1
    flood_fill(grid, start_r, start_c)

    print("After flood:")
    print_grid(grid)

if __name__ == "__main__":
    main()
