def parser(filename):
    with open(filename,'r') as f:
        lines = [line.rstrip('\n') for line in f]
        header = lines[0]
        start_row, start_col = header.split()   # gives ["5","4"]
        start_row = int(start_row)
        start_col = int(start_col)
    return lines