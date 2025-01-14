from models.sor_model import SORModel

class TriageModel(SORModel):
    def __init__(self, beds, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.beds = beds

    def run(self):
        for time in range(self.endtime):
            self.generated_patients.extend(self.generate_patients())
            self.state_change()
            self.assign_beds()
        self.report()

    def state_change(self):
        # Implement logic for state change
        pass

    def assign_beds(self):
        while len(self.hospitalized) < self.beds and self.waiting:
            self.hospitalized.append(self.waiting.pop(0))

    def report(self):
        print("Triage Results:")
        print(f"Recoveries: {self.recoveries}, Deaths: {self.deaths}")
        print(f"Resources used: {self.resources_used}")

