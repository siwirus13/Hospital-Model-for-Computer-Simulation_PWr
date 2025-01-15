from models.triage_model import TriageModel
from models.resource_allocation_model import ResourceAllocationModel
import random

class Simulation:
    def __init__(self, seed, patient_prob, endtime):
        random.seed(seed)
        self.patient_prob = patient_prob
        self.endtime = endtime

    def run(self, model_type, **kwargs):
        if model_type == 'Triage':
            model = TriageModel(*kwargs.values(), self.endtime, self.patient_prob)
        elif model_type == 'Resource Allocation':
            model = ResourceAllocationModel(*kwargs.values(), self.endtime, self.patient_prob)
        else:
            raise ValueError("Invalid model type.")
        model.run()

