#t1 return list w even num in reverse order
input_ = input("give a list seperated by commas ex 2,4,5: ").split(',')
new = []
for i in input_:
    x = int(i.strip())
    new.append(x)
    #new is clean list
newer = []  #even
for i in new:
    if i % 2 == 0:
        newer.append(i)
    else:
        pass
    #reverse
print(newer[::-1])  #just one : removes last element not reverse

##recursive fn frint num from n down to 1
def count_down(n):
    if n <= 1:
        print('1')
    else:
        print(n)
        count_down(n-1)

#rec fn same but inna list
def build_down(n):
    lister = []
    if n < 1:
        return []
    elif n == 1:
        return [1]
    else:
        return [n] + build_down(n-1)