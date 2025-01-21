from abc import ABC, abstractmethod

class SORModel(ABC):
    def __init__(self, endtime, patient_prob, hourly_patients=None):
        self.endtime = endtime
        self.patient_prob = patient_prob
        self.waiting = []
        self.hospitalized = []
        self.recoveries = 0
        self.deaths = 0
        self.resources_used = 0
        self.hourly_patients = hourly_patients or {}

    def get_patients_for_hour(self, time):
        return self.hourly_patients.get(time, [])

    @abstractmethod
    def run(self):
        pass
