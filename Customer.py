import numpy

class Customer:
    def __init__(self):
        self.tickets = 0
        self.wait_time = 0
        self.waiting = False
        self.early = False

    def add_tickets(self, ticket_num):
        self.tickets += ticket_num

    def remove_tickets(self, ticket_num):
        self.tickets -= ticket_num

    def get_tickets(self):
        return self.tickets

    def get_wait_status(self):
        return self.waiting

    def set_waiting(self, bool_val):
        self.waiting = bool_val

    def set_early(self):
        self.early = True

    def inc_wait_time(self):
        self.wait_time += 1

    def get_wait_time(self):
        return self.wait_time

    def request_tickets(self):
        return numpy.random.normal(100, 30)
          
        
