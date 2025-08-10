#rec power fn
def rec_power(base,expo):
    if expo < 0:
        raise ValueError("value too small")
    elif expo == 0:
        return 1
    else:
        return base * rec_power(base,expo-1)
def main():
    base = int(input("give a base: "))
    expo = int(input("give a exponent: "))
    ans = rec_power(base,expo)
    print(f'{base} to the {expo} is {ans}')
main()