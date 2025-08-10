def outbreak(day):
    if day < 1:
        return False
    elif day == 1:
        return 6
    elif day == 2:
        return 20
    elif day == 3:
        return 75
    else:
        return outbreak(day-1) + outbreak(day-2) + outbreak(day-3)
def main():
    day = int(input("give a day: "))
    ans = outbreak(day)
    if day < 1:
        print("invalid day")
    else:
        print(f"total ppl with flu: {ans}")
main()
