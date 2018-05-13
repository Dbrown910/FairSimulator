import Queue
from Customer import Customer

class Booth:
    def __init__(self, exp):       
        self.in_progress = False   
        self.queue_len = 0
        self.queue = Queue.Queue(1000)
        self.profit = 0
        if not exp:
            self.tickets_selling = 0
            self.ticket_cost = 0.25
            self.transaction_time = 0
        if exp:
            self.tickets_selling = 200
            self.ticket_cost = 50
            self.transaction_time = 15

    def add_customer(self, Customer):
        self.queue.put(Customer)
        self.queue_len += 1

    def service_customer(self):
        self.queue_len -= 1
        return self.queue.get()

    def trans_in_progress(self, bool_val):
        self.in_progress = bool_val

    def servicing(self):
        return self.in_progress

    def set_cost(self, price):
        self.ticket_cost = price

    def inc_time(self):
        self.transaction_time += 1

    def add_profit(self, amt):
        self.profit += amt
    
    def get_profit(self):
        return self.profit

    def get_queue_len(self):
        return self.queue_len
    
