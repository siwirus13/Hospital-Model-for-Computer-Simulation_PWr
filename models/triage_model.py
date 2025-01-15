
from models.SOR_model import SORModel
from models.patient import Patient

class TriageModel(SORModel):
    def __init__(self, beds, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.beds = beds

    def run(self):

        for time in range(self.endtime):
            self.generated_patients.extend(self.generate_patients(self.ambulanse(self.patient_prob, self.endtime)))
            for patient in self.generated_patients[:]:
                self.waiting.append(patient)
                self.generated_patients.remove(patient)
            self.state_change()
            self.assign_beds()
        self.report()

    def assign_beds(self):
        while len(self.hospitalized) < self.beds and self.waiting:
            self.hospitalized.append(self.waiting.pop(0))

    # def state_change(self):
    #     Define the state change logic here, because it is different from the one in resource_allocation_model.py, so it shouldn't be inherited from SORModel
   


    def report(self):
        print("Triage Results:")
        print(f"Recoveries: {self.recoveries}, Deaths: {self.deaths}, Still in hospital: {len(self.waiting)+len(self.hospitalized)}")
        print(f"Resources used: {self.resources_used}")

