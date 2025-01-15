from simulation import Simulation
import logging
import csv
from pathlib2 import Path

def main2():
    sim = Simulation(seed=80, patient_prob=0.9, endtime=10)
    sim.run('Triage', beds=40)
    # sim.run('Resource Allocation', red_beds=10, orange_beds=10, yellow_beds=10, green_beds=10)
main2()
