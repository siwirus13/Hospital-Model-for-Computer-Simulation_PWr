from abc import ABC, abstractmethod

class SORModel(ABC):
    def __init__(self, endtime, patient_prob):
        self.endtime = endtime
        self.patient_prob = patient_prob
        self.hospitalized = []
        self.waiting = []
        self.recoveries = 0
        self.deaths = 0
        self.resources_used = 0
        self.generated_patients = []

    def generate_patients(self):
        new_patients = []
        while True:
            if random.random() < self.patient_prob:
                health_status = random.choices(
                    ['green', 'yellow', 'orange', 'red'],
                    weights=[0.35, 0.25, 0.25, 0.15],
                    k=1
                )[0]
                new_patients.append(Patient(health_status))
            else:
                break
        return new_patients

    @abstractmethod
    def run(self):
        pass
