#bool matrix mult 
len_input = int(input("enter size ex. 3: "))
width_input = int(input("enter size ex. 3: "))
user_input_a = input("enter input left to right w commas: ").split(',')
user_input_b = input("enter input left to right w commas: ").split(',')
# 1 0 1, 0 1 0, 0 0 0 
print(user_input_a)
a = []
for group in user_input_a:
    x = group.strip()
    ans = x.split()
    #int
    int_row = []
    for i in ans:
        int_row.append(int(i))
    a.append(int_row)
print(a)
#b 
b = []

for group in user_input_b:
    y = group.strip()
    answer = y.split()
    #int
    int_rows = []
    for i in ans:
        int_rows.append(int(i))
    b.append(int_rows)
print(b)
#MATRIX CHECK - col in a = rows in b
num_rows_b = len(b)
num_col_a = len(a[0]) #getting num of elements, can use a[1] etc
if num_rows_b != num_col_a:
    print("invalid matrix mult")
    exit()
else:
    newest = []
    for i in range(len(a)): #rows of a
        new_row = []
        for j in range(len(b[0])): #col of b
            val = 0
            for k in range(len(b)):
                val = val or ((a[i][k] and b[k][j]))  #memorize for bool mult
            new_row.append(val)
        newest.append(new_row)
for row in newest:
    print(row)
        
