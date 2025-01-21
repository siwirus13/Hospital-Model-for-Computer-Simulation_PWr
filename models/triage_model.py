from models.SOR_model import SORModel

class TriageModel(SORModel):
    def __init__(self, endtime, patient_prob, hourly_patients=None, **kwargs):
        super().__init__(endtime, patient_prob, hourly_patients)
        self.beds = kwargs.get("beds")

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

        for patient in self.hospitalized[:]:
            patient.state_change()
            patient.hospital_time += 1

            if patient.health_status == 'green':
                self.recoveries += 1
                self.resources_used += 2
                self.hospitalized.remove(patient)
            elif patient.health_status == 'red' and patient.hospital_time >= 24:
                self.deaths += 1
                self.resources_used += 12
                self.hospitalized.remove(patient)

    def assign_beds(self):
        while len(self.hospitalized) < self.beds and self.waiting:
            self.hospitalized.append(self.waiting.pop(0))

    def report(self):
        print("Triage Results:")
        print(f"Recoveries: {self.recoveries}")
        print(f"Deaths: {self.deaths}")
        print(f"Still in hospital ||| waiting: {len(self.hospitalized)} ||| {len(self.waiting)}")
