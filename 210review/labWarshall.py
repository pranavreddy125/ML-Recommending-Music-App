row_input = int(input("enter num of rows: "))
col_input = int(input("enter num of cols: "))
matrix = []
for i in range(row_input):
    row = list(map(int,input().split()))
    matrix.append(row)
print("printing initial matrix")
for row in matrix:
    print(row)
for k in range(row_input):  #middle node
    for i in range(row_input):  #first node
        for j in range(row_input):  #last node
            if matrix[i][k] == 1 and matrix[k][j] == 1:
                matrix[i][j] = 1
print("printing final matrix")
for row in matrix:
    print(row)