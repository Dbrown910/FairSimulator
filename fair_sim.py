import numpy
import Queue
import random
from Booth import Booth
from Customer import Customer
from MGRound import MGRound
from RollerCoaster import RollerCoaster
from GameStalls import GameStalls

mgr_total_tix = []
rc_total_tix = []
stalls_total_tix = []
mgr_qsize = []
rc_qsize= []
stalls_op_cost = []
exp_booth_profit = []
cash_booth_profit = []
num_of_fairgoers = []
avg_fairgoers = []


def fair_day():
    early_arrivals = {}
    early_queue = Queue.Queue(250)
    num_early_arrivals = int(numpy.random.normal(200, 20))
    cash_booth = Booth(False)
    express_booth = Booth(True)
    
    
    wait_to_enter = True
    exp_serve_time = 0
    cash_wait_time = 0
    cash_serve_time = 0
    tix_to_buy = 0
    exp_curr_customer = Customer()
    cash_curr_customer = Customer()
    next_arrival = 0
    
    fairgrounds = []  
    mgr = MGRound()
    rc = RollerCoaster()
    stalls = GameStalls()
    mgr_clock = 0
    rc_clock = 0
    stalls_clock = 0

    #simulate early arrivals from 9:30 to 10:30
    j = 0
    while j < num_early_arrivals:
        time_arrived = int(numpy.random.normal(1800, 900))
        while time_arrived > 3600 or time_arrived < 0:
            time_arrived = int(numpy.random.normal(1800, 900))
        early_arrivals[time_arrived] = True
        j += 1


    #9:30 waiting period begins. 10:00 Fair opens, day begins
    for i in range(1,30601):

        #simulate arrivals
        if fair_open(i) and wait_to_enter:
            clear_early_queue(early_queue, cash_booth, express_booth)
            wait_to_enter = False;
        if i >= 5400:
            mgr.update_op_cost(i)
            rc.update_op_cost(i)
            stalls.update_op_cost(i)
            check_num_people(i, len(fairgrounds) + mgr.ride_queue.qsize() + rc.ride_queue.qsize() + len(stalls.ride))
        if i <= 3600:
            try:
                if early_arrivals[i] and wait_to_enter:
                    c = Customer()
                    c.set_early()
                    early_queue.put(c)
                elif early_arrivals[i]:          
                    early_choose_booth(cash_booth, express_booth)
            except KeyError:
                continue
        elif i == 3601:
            next_arrival = numpy.random.poisson(240) + i
        elif i > 3601 or i <= 23400:
            if i == next_arrival:
                standard_choose_booth(cash_booth, express_booth)
                next_arrival = numpy.random.poisson(240) + i
        else:
            continue
 
        #simulate ticket purchases
        if express_booth.get_queue_len() > 0 and not express_booth.servicing():
            express_booth.trans_in_progress(True)
            exp_curr_customer = express_booth.service_customer()
            exp_curr_customer.set_waiting(True)
        
        if express_booth.servicing():
            exp_curr_customer.inc_wait_time()  
            if exp_curr_customer.get_wait_time() == 15:
                express_booth.trans_in_progress(False)
                express_booth.add_profit(50)
                exp_curr_customer.set_waiting(False)
                exp_curr_customer.add_tickets(200)
                fairgrounds.append(exp_curr_customer)

        if cash_booth.get_queue_len() > 0 and not cash_booth.servicing():
            tix_to_buy = int(cash_curr_customer.request_tickets())
            cash_wait_time = 120 + int(tix_to_buy / 10)
            cash_booth.trans_in_progress(True)
            cash_curr_customer = cash_booth.service_customer()
            cash_curr_customer.set_waiting(True)

        if cash_booth.servicing():
            cash_curr_customer.inc_wait_time()
            if cash_curr_customer.get_wait_time() == cash_wait_time:
                cash_booth.trans_in_progress(False)
                cash_booth.add_profit(tix_to_buy * 0.25)
                cash_curr_customer.set_waiting(False)
                cash_curr_customer.add_tickets(tix_to_buy)
                fairgrounds.append(cash_curr_customer)

        #send customers to fair attractions 
        for k in range(0, len(fairgrounds)):
            ride_choice = random.randrange(0,100)
            curr_customer = fairgrounds[k]
            if curr_customer is None:
                del fairgrounds[:]
                break

            if curr_customer.get_tickets() >= 16:
                if ride_choice < 40:
                    rc.queue_rider(curr_customer)
                elif ride_choice >= 40 and ride_choice < 75:
                    if not stalls.is_full():
                        stalls.add_player(fairgrounds[k])
                    else:
                        if curr_customer.get_tickets() > 16:
                            if ride_choice > 59:
                                mgr.queue_rider(fairgrounds[k])
                            else:
                                rc.queue_rider(fairgrounds[k])
                                continue
                        elif curr_customer.get_tickets() < 16 and curr_customer.get_tickets() > 8:
                            mgr.queue_rider(fairgrounds[k])
                else:
                    mgr.queue_rider(fairgrounds[k])
            elif curr_customer.get_tickets >= 8:
                if ride_choice < 58 and not stalls.is_full():
                    stalls.add_player(curr_customer)
                else:
                    mgr.queue_rider(fairgrounds[k])
            else:
                if not stalls.is_full():
                        stalls.add_player(curr_customer)

            if k == len(fairgrounds) -1:
                del fairgrounds[:]

        #update merry go round
        if mgr.is_loading():
            if mgr_clock >= mgr.get_load_time(): 
                for x in range(0,30):
                    mgr.load_rider()
                mgr.set_loading(False)
                mgr.set_running(True) 
                mgr_clock = -1
            else: 
                mgr_clock += 1

        if mgr.is_running():
            if mgr_clock >= mgr.get_ride_time():
                mgr.set_running(False)
                mgr.set_unloading(True)
                mgr_clock = -1
            else:
                mgr_clock += 1

        if mgr.is_unloading():
            if mgr_clock >= mgr.get_unload_time():
                for x in range(0,30):
                    fairgrounds.append(mgr.unload_rider())
                mgr.set_unloading(False)
                mgr.set_loading(True)
                mgr_clock = -1
            else:
                mgr_clock += 1

        #update stalls
        if stalls.is_open():
            if stalls_clock >= stalls.get_wait_time() and stalls.get_num_players() > 1:
                stalls.set_open(False)
                stalls_clock = 0
            else:
                stalls_clock += 1

        if not stalls.is_open():
            if stalls_clock >= stalls.get_ride_time():
                stalls.add_tickets(stalls.get_num_players())
                stalls.remove_players(fairgrounds)
                if not stalls.is_full():
                    stalls.set_open(True)
                stalls_clock = 0
            else:
                stalls_clock += 1

        #update roller coaster
        if rc.is_loading():
            if not rc.is_loaded():
                for x in range(0,60):
                    rc.load_rider()
                rc.set_loaded(True)
            if rc_clock >= rc.get_load_time(): 
                rc.set_loading(False)
                rc.set_running(True) 
                rc_clock = 0
            else: 
                rc_clock += 1


        if rc.is_running(): 
            if rc_clock >= rc.get_ride_time():
                rc.set_running(False)
                rc.set_unloading(True)
                rc_clock = 0
            else:
                rc_clock += 1

        if rc.is_unloading():
            if rc_clock >= rc.get_unload_time():
                for x in range(0,60):
                    fairgrounds.append(rc.unload_rider())
                rc.set_unloading(False)
                rc.set_loaded(False)
                rc.set_loading(True)
                rc_clock = 0
            else:
                rc_clock += 1

    exp_booth_profit.append(express_booth.get_profit())
    cash_booth_profit.append(cash_booth.get_profit())
    mgr_total_tix.append(mgr.ticket_count())
    stalls_total_tix.append(stalls.ticket_count()) 
    rc_total_tix.append(rc.ticket_count()) 
    mgr_qsize.append(mgr.ride_queue.qsize())
    stalls_op_cost.append(stalls.return_op_cost())
    rc_qsize.append(rc.ride_queue.qsize()) 
    avg_fairgoers.append(calc_avg(num_of_fairgoers))


def fair_open(x):
    if x == 1800:
        return True
    else:
        return False

def clear_early_queue(early_queue, c_booth, e_booth):
    line_choice = 0
    num_queue_elements = early_queue.qsize()
    for x in range(0, num_queue_elements):
        line_choice = random.randrange(0,100)
        if line_choice < 80:
            e_booth.add_customer(early_queue.get())
        #10 because average wait time for 1 person is 2 minutes
        elif c_booth.get_queue_len() > 10 and c_booth.get_queue_len() > (e_booth.get_queue_len() * 2):
            line_choice = random.randrange(0,100)
            if line_choice > 20:
                e_booth.add_customer(early_queue.get())
            else:
                c_booth.add_customer(early_queue.get())
        else:
            c_booth.add_customer(early_queue.get())

def early_choose_booth(c_booth, e_booth):
    line_choice = 0
    line_choice = random.randrange(0,100)
    if line_choice < 80:
        c = Customer()
        c.set_early()
        e_booth.add_customer(c)
    #10 because average wait time for 1 person is 2 minutes
    elif c_booth.get_queue_len() > 10 and c_booth.get_queue_len() > (e_booth.get_queue_len() * 2):
        line_choice = random.randrange(0,100)
        if line_choice < 20:
            c = Customer()
            c.set_early()
            e_booth.add_customer(c)
        else:
            c = Customer()
            c.set_early()
            c_booth.add_customer(c)
    else:
        c = Customer()
        c.set_early()
        c_booth.add_customer(c)

def standard_choose_booth(c_booth, e_booth):
    line_choice = 0
    line_choice = random.randrange(0,100)
    if line_choice < 10:
        c = Customer()
        c.set_early()
        e_booth.add_customer(c)
    #10 because average wait time for 1 person is 2 minutes
    elif c_booth.get_queue_len() > 10 and c_booth.get_queue_len() > (e_booth.get_queue_len() * 2):
        line_choice = random.randrange(0,100)
        if line_choice > 20:
            c = Customer()
            c.set_early()
            e_booth.add_customer(c)
        else:
            c = Customer()
            c.set_early()
            c_booth.add_customer(c)
    else:
        c = Customer()
        c.set_early()
        c_booth.add_customer(c)

def check_num_people(i, num_people):
        if(i - 1800) % 900 == 0:
            num_of_fairgoers.append(num_people)
  
def calc_avg(param):
    return sum(param) / len(param)


for y in range(0,50):
    fair_day()
print "AVERAGES"
print "Express booth profit: $" + str(calc_avg(exp_booth_profit))
print "Cash booth profit : $" + str(calc_avg(cash_booth_profit))
print "Merry Go Round tickets: " + str(calc_avg(mgr_total_tix))
print "Games & Stall tickets: " + str(calc_avg(stalls_total_tix))
print "Roller Coaster tickets: " + str(calc_avg(rc_total_tix))
print "Merry Go Round avg end queue size: " + str(calc_avg(mgr_qsize))
print "Roller Coaster avg end queue size: " + str(calc_avg(rc_qsize))
print "Games & Stall op cost: $" + str(calc_avg(stalls_op_cost))
print "Average number of fair goers: " + str(calc_avg(avg_fairgoers))

