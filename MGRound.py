import Queue
import numpy
from Customer import Customer

class MGRound:
	def __init__(self):
		self.ride_queue = Queue.Queue(1000)
		self.ride = Queue.Queue(30)
		self.load_time = 120 
		self.ride_time = 240
		self.unload_time = 30 
		self.op_cost = 0
		self.loading = True
		self.unloading = False
		self.inOperation = False
		self.tickets_collected = 0

	def queue_rider(self, cust):
		self.ride_queue.put(cust)

	def has_queue(self):
		if self.ride_queue.qsize() > 0:
			return True
		else:
			return False

	def load_rider(self):
		if self.has_queue() and not self.is_ride_full():
			self.tickets_collected += 8
			cust = self.ride_queue.get()
			cust.remove_tickets(8)
			self.ride.put(cust)

	def unload_rider(self):
		if(self.ride.qsize() > 0):
			return self.ride.get()

	def is_ride_full(self):
		if self.ride.qsize() == 30:
			return True
		else:
			return False

	def set_loading(self, bool_val):
		self.loading = bool_val

	def is_loading(self):
		return self.loading

	def set_running(self, bool_val):
		self.inOperation = bool_val

	def is_running(self):
		return self.inOperation

	def set_unloading(self, bool_val):
		self.unloading = bool_val

	def is_unloading(self):
		return self.unloading

	def get_load_time(self):
		return int(self.load_time)

	def get_ride_time(self):
		return self.ride_time

	def get_unload_time(self):
		return int(self.unload_time)
		
	def update_op_cost(self, i):
		if (i - 1800) % 3600 == 0:
			self.op_cost += 10

	def return_op_cost(self):
		return self.op_cost

	def ticket_count(self):
		return self.tickets_collected

	def get_queue_size(self):
		return self.ride_queue.qsize()