from models.SOR_model import SORModel
import csv
import os

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

    def report(self, filename="triage_results.csv", sim_index=1):
        file_exists = os.path.exists(filename)

        with open(filename, mode="a" if file_exists else "w", newline="") as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow(["Simulation index"] + [f"Sim {sim_index}"])
                writer.writerow(["Recoveries"] + [self.recoveries])  # Make sure this appears in the first write
                writer.writerow(["Deaths"] + [self.deaths])
                writer.writerow([])
                writer.writerow(["Simulation Parameters"])
                writer.writerow(["Patient Probability"] + [self.patient_prob])
                writer.writerow(["End Time"] + [self.endtime])
                writer.writerow(["Total Beds"] + [self.beds])
            else:
                with open(filename, mode="r", newline="") as read_file:
                    rows = list(csv.reader(read_file))

                rows[0].append(f"Sim {sim_index}")  # First row: Simulation index
                rows[1].append(self.recoveries)  # Second row: Recoveries (Make sure this is on row 1)
                rows[2].append(self.deaths)  # Third row: Deaths
                rows[5].append(self.patient_prob)  # Patient Probability
                rows[6].append(self.endtime)  # End Time
                rows[7].append(self.beds)  # Total Beds

                with open(filename, mode="w", newline="") as write_file:
                    writer = csv.writer(write_file)
                    writer.writerows(rows)

        print(f"Results appended to {filename}")



