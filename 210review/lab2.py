#fn, one to one, onto````           basically finished
#put into list
input_ = input("give a input mapping: ").split()#splits str at spaces and puts into a list
mapping_ = []
#mapping_.append(input_) #put into list
for pair in input_:     #input_[0] = (3,A) so iterating thru each pair
    x = pair.strip('()') #take away ()
    ans_ = x.split(',') # '3,a' -> ['3','a']
    tup = (int(ans_[0]), ans_[1])
    mapping_.append(tup)
#fn
#use a set bc it has no duplicates
def fn_check():
    dupl = set()
    fn_ = True
    for i in mapping_:
        if i[0] in dupl:
            fn_ = False
        else:
            dupl.add(i[0])  #tracking inputs
#one to one
def onee():
    one_ = set()
    is_one = True
    for i in mapping_:
        if i[1] in one_:
            is_one = False
            break
        print("is not one to one")
        else:
            one_.add(i[1]) #tracking outputs
        print("is one to one")
#on to
def onto():
    one_to = set()
    codo = {'a','b','c','d'}
    is_one_to = False
    for i in mapping_:
        one_to.add(i[1]) #all outputs in set
    if codo.issubset(one_to):
        is_one_to = True
        print("is on to")
    else:
        is_one_to = False
        print("is not on to")
def main():
    ans1 = fn_check()
    ans2 = onee()
    ans3 = onto()
    print(f"{ans1},{ans2},{ans3}")
main()

'''
# input and formatting
input_ = input("give a input mapping: ").split()
mapping_ = []

for pair in input_:
    x = pair.strip('()')
    ans_ = x.split(',')
    tup = (int(ans_[0]), ans_[1])
    mapping_.append(tup)

# function check
def fn_check():
    dupl = set()
    for i in mapping_:
        if i[0] in dupl:
            return False
        dupl.add(i[0])
    return True

# one-to-one check
def onee():
    one_ = set()
    for i in mapping_:
        if i[1] in one_:
            return False
        one_.add(i[1])
    return True

# onto check
def onto():
    one_to = set()
    codo = {'a', 'b', 'c', 'd'}
    for i in mapping_:
        one_to.add(i[1])
    return codo.issubset(one_to)

# main logic
def main():
    ans1 = fn_check()
    if not ans1:
        print("is not a function")
        return

    print("is a function")

    ans2 = onee()
    print("is one to one" if ans2 else "is not one to one")

    ans3 = onto()
    print("is on to" if ans3 else "is not on to")

main()
'''