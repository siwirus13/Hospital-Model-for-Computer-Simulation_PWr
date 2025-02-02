from models.SOR_model import SORModel
from models.patient import Patient
import csv
import os

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

    def report(self, filename="resource_allocation_results.csv", sim_index=1):
        file_exists = os.path.exists(filename)

        with open(filename, mode="a" if file_exists else "w", newline="") as file:
            writer = csv.writer(file)

            if not file_exists:
                # Create headers only for the first simulation
                writer.writerow(["Simulation index"] + [f"Sim {sim_index}"])
                writer.writerow(["Recoveries"] + [self.recoveries])
                writer.writerow(["Deaths"] + [self.deaths])
                writer.writerow(["Hospitalized (Green)"] + [len(self.hospitalized['green'])])
                writer.writerow(["Hospitalized (Yellow)"] + [len(self.hospitalized['yellow'])])
                writer.writerow(["Hospitalized (Orange)"] + [len(self.hospitalized['orange'])])
                writer.writerow(["Hospitalized (Red)"] + [len(self.hospitalized['red'])])
                writer.writerow(["Total Hospitalized"] + [
                    len(self.hospitalized['green']) + len(self.hospitalized['yellow']) +
                    len(self.hospitalized['orange']) + len(self.hospitalized['red'])
                ])
                writer.writerow(["Waiting"] + [len(self.waiting)])
                writer.writerow([])
                writer.writerow(["Simulation Parameters"])
                writer.writerow(["Patient Probability"] + [self.patient_prob])
                writer.writerow(["End Time"] + [self.endtime])
                writer.writerow(["Bed Distribution (R, O, Y, G)"] + [self.beds])
            else:
                # Read the existing CSV and update values
                with open(filename, mode="r", newline="") as read_file:
                    rows = list(csv.reader(read_file))

                rows[0].append(f"Sim {sim_index}")  # Simulation index row
                rows[1].append(self.recoveries)  # Recoveries row
                rows[2].append(self.deaths)  # Deaths row
                rows[3].append(len(self.hospitalized['green']))  # Green beds
                rows[4].append(len(self.hospitalized['yellow']))  # Yellow beds
                rows[5].append(len(self.hospitalized['orange']))  # Orange beds
                rows[6].append(len(self.hospitalized['red']))  # Red beds
                rows[7].append(len(self.hospitalized['green']) + len(self.hospitalized['yellow']) +
                               len(self.hospitalized['orange']) + len(self.hospitalized['red']))  # Total hospitalized
                rows[8].append(len(self.waiting))  # Waiting
                rows[11].append(self.patient_prob)  # Patient Probability
                rows[12].append(self.endtime)  # End Time
                rows[13].append(self.beds)  # Bed distribution

                with open(filename, mode="w", newline="") as write_file:
                    writer = csv.writer(write_file)
                    writer.writerows(rows)

        print(f"Results appended to {filename}")
