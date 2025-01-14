from models.sor_model import SORModel

class ResourceAllocationModel(SORModel):
    def __init__(self, red_beds, orange_beds, yellow_beds, green_beds, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.red_beds = red_beds
        self.orange_beds = orange_beds
        self.yellow_beds = yellow_beds
        self.green_beds = green_beds
        self.hospitalized = {
            'red': [],
            'orange': [],
            'yellow': [],
            'green': []
        }

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
        # Assign patients to beds based on priority
        pass

    def report(self):
        print("Resource Allocation Model Results:")
        print(f"Recoveries: {self.recoveries}, Deaths: {self.deaths}")
        print(f"Resources used: {self.resources_used}")
