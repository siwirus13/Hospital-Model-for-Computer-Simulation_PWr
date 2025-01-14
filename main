from simulation import Simulation

def main():
    sim = Simulation(seed=80, patient_prob=0.99, endtime=500)
    sim.run('Triage', beds=40)
    sim.run('Resource Allocation', red_beds=10, orange_beds=10, yellow_beds=10, green_beds=10)

if __name__ == "__main__":
    main()
