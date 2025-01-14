class Patient:
    def __init__(self, health_status, waiting_time=0, hospital_time=0):
        self.health_status = health_status
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
##Still in progress
