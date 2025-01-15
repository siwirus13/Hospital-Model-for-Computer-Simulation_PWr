from abc import ABC, abstractmethod
import random
from models.patient import Patient

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



    def generate_patients(self, amount):
        new_patients = []
        for time in range(amount):
            if random.random() < self.patient_prob:
                health_status = random.choices(
                    ['green', 'yellow', 'orange', 'red'],
                    weights=[0.35, 0.25, 0.25, 0.15],
                    k=1
                )[0]
                new_patients.append(Patient(health_status))
                print(f"New patient with health status {health_status} arrived.")
            else:
                break
        return new_patients

    def ambulanse(self,patient_prob, endtime):

        new_patients = 0
        for time in range(endtime):

            while True:
                if random.random() < patient_prob:
                    new_patients += 1

                else:
                    break
            return new_patients

    def assign_beds(self):
        while True:
            if len(self.hospitalized) < self.beds and self.waiting[:]:
                self.hospitalized.append(self.waiting.pop(0))
                print(f"Patient assigned to bed.")
            else:
                continue






    def state_change(self):
        # Aktualizowanie stanu pacjentów oczekujących
        for patient in self.waiting:
            patient.state_change()
            patient.waiting_time += 1
            if patient.health_status == 'red' and patient.waiting_time >= 10:
                self.deaths += 1
                self.waiting.remove(patient)
                print(f"Patient in waiting died after {patient.waiting_time} hours.")

        # Aktualizowanie stanu pacjentów hospitalizowanych
        for patient in self.hospitalized:
            patient.state_change()
            patient.hospital_time += 1
            if patient.health_status == 'green':
                self.recoveries += 1
                self.resources_used += 2  # Przykładowy koszt dla zielonego pacjenta
                self.hospitalized.remove(patient)
            elif patient.health_status == 'red' and patient.hospital_time >= 24:
                self.deaths += 1
                self.resources_used += 12  # Przykładowy koszt dla czerwonego pacjenta
                self.hospitalized.remove(patient)

    @abstractmethod
    def run(self):
        pass
