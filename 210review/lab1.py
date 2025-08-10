list1 = []      #good 7/5 done and/or/xor
list2 = []
def add_fn(list1, list2):
    ans = []
    counter = 0
    while counter < len(list1):
        if list1[counter] == '1' and list2[counter] == '1':
            ans.append('1')
            counter += 1
        else:
            ans.append('0')
            counter += 1
    return ans
def or_fn(list1,list2):
    ans = []
    counter = 0
    while counter < len(list1):
        if list1[counter] == '0' and list2[counter] == '0':
            ans.append('0')
            counter += 1
        else:
            ans.append('1')
            counter += 1
    return ans
def xor_fn(list1,list2):
    ans = []
    counter = 0
    while counter < len(list1):
        if list1[counter] == '1' and list2[counter] == '0':
            ans.append('1')
            counter += 1
        elif list1[counter] == '0' and list2[counter] == '1':
            ans.append('1')
            counter += 1
        else:
            ans.append('0')
            counter += 1
    return ans
def main():
    input1 = input("give a bitwise input: ")
    input2 = input("give a bitwise input: ")
    for bit in input1:
        list1.append(bit)
    for bit in input2:
        list2.append(bit)
    ans_1 = add_fn(list1,list2)
    ans_2 = or_fn(list1,list2)
    ans_3 = xor_fn(list1,list2)
    print(f"AND = {''.join(ans_1)}, OR = {''.join(ans_2)}, XOR = {''.join(ans_3)}")
main()