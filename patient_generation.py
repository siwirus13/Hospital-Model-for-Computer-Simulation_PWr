from models.patient import Patient
import random

class PatientGenerator:
    def __init__(self,seed, patient_prob, endtime):
        self.patient_prob = patient_prob
        self.seed = seed
        random.seed(seed)
        self.endtime = endtime
        self.all_patients = 0
        self.patients_by_hour = {}

    def generate_all_patients(self):
        for hour in range(self.endtime):
            self.patients_by_hour[hour] = self.generate_patients_for_hour()
        for time in range(self.endtime):
            new_patients = self.patients_by_hour[time]
            self.all_patients += len(new_patients)
        print(f"For seed == {self.seed}, endtime == {self.endtime} and patient probabilty == {self.patient_prob}: \nTotal patients == {self.all_patients}")
        return self.patients_by_hour


    def generate_patients_for_hour(self):
        num_patients = 0
        while random.random() < self.patient_prob:
            num_patients += 1
        return [
            Patient(
                health_status=random.choices(
                    ['green', 'yellow', 'orange', 'red'],
                    weights=[0.35, 0.25, 0.25, 0.15],
                    k=1
                )[0]
            )
            for _ in range(num_patients)
        ]
