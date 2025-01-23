import random

class Patient:
    def __init__(self, health_status, waiting_time=0, hospital_time=0):
        self.health_status = health_status  # 'green', 'yellow', 'orange', 'red'
        self.waiting_time = waiting_time
        self.hospital_time = hospital_time

    def worsen(self):
        if self.health_status == 'green':
            self.health_status = 'yellow'
        elif self.health_status == 'yellow':
            self.health_status = 'orange'
        elif self.health_status == 'orange':
            self.health_status = 'red'

    def improve(self):
        if self.health_status == 'red':
            self.health_status = 'orange'
        elif self.health_status == 'orange':
            self.health_status = 'yellow'
        elif self.health_status == 'yellow':
            self.health_status = 'green'

    def state_change(self):
        base_prob_worsen = {'green': 0.1, 'yellow': 0.2, 'orange': 0.4, 'red': 0.7}
        base_prob_improve = {'green': 0.3, 'yellow': 0.2, 'orange': 0.15, 'red': 0.1}

        waiting_factor = min(1.0, self.waiting_time / 10)
        hospital_factor = min(1.0, self.hospital_time / 10)

        prob_worsen = base_prob_worsen[self.health_status] + 0.1 * waiting_factor
        prob_improve = base_prob_improve[self.health_status] + 0.1 * hospital_factor

        total_prob = prob_worsen + prob_improve
        prob_worsen /= total_prob
        prob_improve /= total_prob

        random_value = random.random()
        if random_value < prob_worsen:
            self.worsen()

        elif random_value < prob_worsen + prob_improve:
            self.improve()
