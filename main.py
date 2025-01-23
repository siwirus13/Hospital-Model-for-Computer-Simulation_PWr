from simulation import Simulation
from patient_generation import PatientGenerator

def main():
    seed = 80
    patient_prob = 0.9
    endtime = 3
    beds = 10
    beds_colors = [10, 10, 10, 10]

    all_patients=PatientGenerator(seed, patient_prob, endtime).generate_all_patients()
    print("\n")
    sim = Simulation(seed, patient_prob, endtime, all_patients)
    sim.run('Triage', beds=beds)
    print("\n")
    sim.run('Resource Allocation', red_beds=beds_colors[0], orange_beds=beds_colors[1], yellow_beds=beds_colors[2], green_beds=beds_colors[3])

if __name__ == "__main__":
    main()
