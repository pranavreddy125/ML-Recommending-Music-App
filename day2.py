#patient class
class Patient:
    def __init__(self,name,age,priority):
        self.name = name
        self.age = age
        self.priority = priority
    def desribe(self):
        return f"{self.name} (age {self.age}) - Priority: {self.priority}"

def main():
    p1 = Patient("Alice", 30, 2)
    p2 = Patient("Bob", 65, 1)
    p3 = Patient("Charlie", 22, 3)
    patients = [p1, p2, p3]
    sort = sorted(patients, key=lambda patient: patient.priority)
    for p in sort:
        print(p.desribe())
    
main()











class Patient:
    def __init__(self, name, doc, prio):
        self.name = name
        self.doc = doc
        self.prio = prio
    def summary(self):
        return f"Patient: {self.name} | Doctor: {self.doc} | Priority: {self.prio}"
def main():
    p1 = Patient("peter", "reddy", 2)
    p2 = Patient("Bob", "reddy", 1)
    p3 = Patient("maya", "reddy", 3)
    patients = [p1,p2,p3]
    sorter = sorted(patients,key=lambda patient: patient.prio)
    for i in sorter:
        print(i.summary())