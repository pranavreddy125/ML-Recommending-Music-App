from basic import Minheap

class HospitalManager:      #so do self.
    def __init__(self):
        self.hospital = Minheap()

    def patient_adder(self, name, severity):
        self.hospital.insert((name, severity))  

    def see_next(self):
        if self.hospital.is_empty():
            return "No patients left"
        return self.hospital.peek_min()

    def treat(self):
        if self.hospital.is_empty():
            return "No patients left"
        return self.hospital.pop()

    def show_list(self):
        if self.hospital.is_empty():
            return "No patients left"
        return self.hospital._heap  # no () here bc not method
