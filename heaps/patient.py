from basic import Minheap
from deeper import HospitalManager
hospital = HospitalManager()
with open("patient.txt", 'r') as file:
    for line in file:
        parts = line.split(',')
        name = parts[0].strip()
        severity = int(parts[1].strip())
        hospital.patient_adder(name,severity)
while True:
    print("Menu\n 1) Add New Patient\n 2) See Next Patient\n 3) Treat Next Patient\n 4) Show Waiting List\n 5) Exit")
    input_choice = input("Enter a choice: ")

    if input_choice == "1":
        name = input("give you name: ")
        severity = int(input("enter severity level ex. 1 for most severe and 3 for least: "))
        hospital.patient_adder(name,severity)
        print("patient added...")
    elif input_choice == "2":
        ans = hospital.see_next()
        print(f"next patient : {ans}")
        pass
    elif input_choice == "3":
        ans = hospital.treat()
        print(f"treated : {ans}")
    elif input_choice == "4":
        ans = hospital.show_list()
        print(f"full list : {ans}")
    elif input_choice == "5":
        print("Exiting program.")
        break
    else:
        print("Invalid choice, try again.")