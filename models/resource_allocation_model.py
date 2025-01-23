from models.SOR_model import SORModel
from models.patient import Patient

class ResourceAllocationModel(SORModel):
    def __init__(self, endtime, patient_prob, hourly_patients=None, **kwargs):
        super().__init__(endtime, patient_prob, hourly_patients)
        self.beds = {
            'red': kwargs.get("red_beds"),
            'orange': kwargs.get("orange_beds"),
            'yellow': kwargs.get("yellow_beds"),
            'green': kwargs.get("green_beds")
        }
        self.hospitalized = {
            'red': [],
            'orange': [],
            'yellow': [],
            'green': []
        }

    def run(self):
        for time in range(self.endtime):
            self.hospital_changes()
            new_patients = self.get_patients_for_hour(time)
            self.waiting.extend(new_patients)
            self.assign_beds()
        self.report()

    def hospital_changes(self):
        for patient in self.waiting[:]:
            patient.state_change()
            patient.waiting_time += 1

            if patient.health_status == 'red' and patient.waiting_time >= 10:
                self.deaths += 1
                self.waiting.remove(patient)

        for status, patients in self.hospitalized.items():
            for patient in patients[:]:
                patient.state_change()
                patient.hospital_time += 1

                if patient.health_status == 'green':
                    self.recoveries += 1
                    patients.remove(patient)
                elif patient.health_status == 'red' and patient.hospital_time >= 24:
                    self.deaths += 1
                    patients.remove(patient)

    def assign_beds(self): 
        for patient in self.waiting[:]:
            status = patient.health_status

            if len(self.hospitalized[status]) < self.beds[status]:
                self.hospitalized[status].append(patient)
                self.waiting.remove(patient)

    def report(self):

        print("Resource Allocation Results:")
        print(f"Recoveries: {self.recoveries}")
        print(f"Deaths: {self.deaths}")
        print(f"Still in hospital ||| waiting: {len(self.hospitalized['green']) + len(self.hospitalized['orange']) + len(self.hospitalized['yellow'])+ len(self.hospitalized['red'])} ||| {len(self.waiting)}")
