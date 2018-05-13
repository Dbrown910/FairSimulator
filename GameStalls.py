import Queue
import numpy
import random
from Customer import Customer

class GameStalls:
	def __init__(self):
		self.ride = []
		self.ride_time = numpy.random.normal(30, 5) 
		self.wait_time = 10
		self.op_cost = 0
		self.inOperation = True
		self.tickets_collected = 0

	def add_player(self, cust):
		cust.remove_tickets(1)
		self.ride.append(cust)

	def remove_players(self, fg):
		for i, cust in enumerate(self.ride):
			leave = random.randrange(0,99)
			if leave > 50:
				fg.append(cust)
				self.ride.remove(cust)

	def is_full(self):
		if len(self.ride) >= 25:
			return True
		else:
			return False

	def set_open(self, bool_val):
		self.inOperation = bool_val

	def is_open(self):
		return self.inOperation

	def get_wait_time(self):
		return int(self.wait_time)

	def get_ride_time(self):
		return self.ride_time
		
	def update_op_cost(self, i):
		if(i - 1800) % 3600 == 0:
			self.op_cost += (len(self.ride) / 5) * 10

	def return_op_cost(self):
		return self.op_cost

	def add_tickets(self, ticket_num):
		self.tickets_collected += ticket_num

	def ticket_count(self):
		return self.tickets_collected

	def get_num_players(self):
		return len(self.ride)