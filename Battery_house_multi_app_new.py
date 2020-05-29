import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.animation import FuncAnimation
from house_multiapp import House
from battery_score import Battery
from csv import writer
import math
from statistics import mean

import sys

num_cell = 20
default_charge = 50 #state of charge
num_house = 3

number_panels = 3
perhour_charge = 200*number_panels

#cell_charge = [default_charge for i in range(num_cell)]

#for charging
day_time = [9,10,11,12,13,14,15,16]

houses = {}

today_charge = []

#initialize house and battery at the start
def init_house(num_house):
    for i in range(num_house):
        fam_size = random.randint(1,5)
        houses[i] = House(fam_size)

def init_batt(cell):
    global battery
    
    battery = Battery(cell,charge_init=default_charge)

#update the demand for electricity today
def get_today_usage():
    global today_charge
    
    #initialize array for charge
    collect_charge = np.zeros((num_house,24))

    #collect charge per house per hour
    for i in range(len(houses)):
        collect_charge[i] = houses[i].get_demand()
        
    #sum all the charges required from all houses at each hour
    today_charge = np.sum(collect_charge,axis=0)

def randomness():
    return random.randint(-10,10)

'''#method of charging - charging one charge at a time
'implement diff charging'
def del_charge(charge):

    if charge < 0:
        active_cell = cell_charge.index(max(cell_charge))
        change = -1
    else:
        active_cell = cell_charge.index(min(cell_charge))
        change = 1

    for i in range(abs(charge)):
        cell_charge[active_cell] = cell_charge[active_cell] + change

        if active_cell == num_cell-1:
            active_cell = 0
        else: active_cell += 1
    return cell_charge
'''
#charge based on scoring
def del_charge2(charge,cell_spread):
    global battery
    
    #discharging
    if (charge<0):
        battery.discharging(cell_spread,abs(charge))

    #charging
    elif (charge>0):
        battery.charging(cell_spread,abs(charge))
    
    return battery.get_charge()

def solar_charge(t): #insert formula of solar charging based on t
    
    if (t in day_time):
        return perhour_charge +randomness()
    else: return 0

#get demand at time t
def village_discharge(t):
    #print(today_charge[t])
    return int(today_charge[t])*-1

#export data to csv containing config and penalty
def collect_data(cell,panel,penalty1,penalty2):
    filename = 'test.csv'

    with open(filename,'a+',newline='')as write_obj:
        write=writer(write_obj)
        write.writerow([cell,panel,mean(penalty1),mean(penalty2)])

def init_excel():
    filename = 'test.csv'

    with open(filename,'w',newline='')as write_obj:
        write=writer(write_obj)
        write.writerow(['cells','panels','village penalty','panels_panelty'])

#for animation function
#each our is per 2 frame. One frame for charging, the other for discharging
def animation_frame(i):
    
    #if new day
    if i%48==0:
        get_today_usage()
        
    time = math.floor(i/2)%24
    #charge = solar_charge(time)
    #discharge = village_discharge(time)
    #diff = charge + discharge
    if i%2==0:
        diff = solar_charge(time)
    else:
        diff = village_discharge(time)

    #update cell charge
    updated_charge = del_charge2(diff)
    #export to csv
    #collect_data(updated_charge)
    print(time, updated_charge)
    for k, b in enumerate(bar_chart):
        b.set_height(updated_charge[k])

    if (i==(48*5)): sys.exit()

    
#initialize houses
init_house(num_house)
init_excel()

cell_range = range(1,51)
panel_range = range(1,15)

simulation_days = 5

for cell in cell_range:
    for panel in panel_range:
        init_batt(cell)

        perhour_charge=panel*200
        
        #48 intervals in a day. One frame for charging, the other for discharging
        for i in range(simulation_days*48):
            
            #if new day
            if i%48==0:
                get_today_usage()
                
            time = math.floor(i/2)%24

            if i%2==0:
                diff = solar_charge(time)
            else:
                diff = village_discharge(time)

            #update battery charges
            del_charge2(diff,cell)

        collect_data(cell,panel,battery.penalty_village,battery.penalty_panels)
                
                
        
'''
future work
how many charges can a battery store
work on exporting multiple data to csv
replace bar with line
'''
