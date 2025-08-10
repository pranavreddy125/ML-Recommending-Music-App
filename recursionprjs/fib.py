def fib(int,mode):
    if int < 0:
        raise ValueError("int cant b below 0")
    elif int == 0:
        return 0
    elif int == 1:
        return 1
    else:
        return fib(int-1) + fib(int-2)
