from models.triage_model import TriageModel
from models.resource_allocation_model import ResourceAllocationModel



class Simulation:
    def __init__(self, seed, patient_prob, endtime, hourly_patients):
        self.seed = seed
        self.patient_prob = patient_prob
        self.endtime = endtime
        self.hourly_patients = hourly_patients
        self.waiting = []
        self.hospitalized = []

    def run(self, model_type, **kwargs):
        if model_type == 'Triage':
            model = TriageModel(self.endtime, self.patient_prob, self.hourly_patients, **kwargs)
        elif model_type == 'Resource Allocation':
            model = ResourceAllocationModel(self.endtime, self.patient_prob, self.hourly_patients, **kwargs)
        else:
            raise ValueError("Invalid model type.")
        model.run()
