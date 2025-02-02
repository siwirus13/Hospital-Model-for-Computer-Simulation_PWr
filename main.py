from simulation import Simulation
from patient_generation import PatientGenerator

def main():
    seed = 81
    endtime = 12000 # TU NIEWIELE ZMIENIAĆ
    
    beds_colors_arr = [[2, 2, 2, 4]]
    patient_probs = [0.25, 0.5, 0.75]
    total_beds = [20, 50, 100, 200] # TU ZMIENIAĆ WSZYSTKO


    for pat_prob in patient_probs: # DEFINIUJEMY PATIENT PROBS
        for beds in total_beds: # DEFINIUJEEMY TOTAL BEDS
            all_patients = PatientGenerator(seed, pat_prob, endtime).generate_all_patients()
            sim = Simulation(seed, pat_prob, endtime, all_patients)
            sim.run('Triage', beds=beds)
            for beds_colors in beds_colors_arr: # DEFINIUJEMY ROZDKŁAD ŁÓŻEK
                sim.run('Resource Allocation', red_beds=beds_colors[0], orange_beds=beds_colors[1], yellow_beds=beds_colors[2],green_beds=beds_colors[3])
if __name__ == "__main__":
    main()
