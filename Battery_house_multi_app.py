import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.animation import FuncAnimation
from house_multiapp import House
from battery_score import Battery
from csv import writer
import math

import sys

num_cell = 20
default_charge = 40*1200/100 #in battery
cell_spread = num_cell # distribute between cells when (dis)charging
num_house = 10

number_panels = 3
perhour_charge = 200*number_panels

cell_charge = [default_charge for i in range(num_cell)]

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
    for i in range(len(houses)):
        collect_charge[i] = houses[i].get_demand()
        
    #sum all the charges required from all appliances at each hour
    today_charge = np.sum(collect_charge,axis=0)

def randomness():
    return random.randint(-10,10)

#method of charging - charging one charge at a time
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

#charge based on scoring
def del_charge2(charge):
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

#export data to csv
def collect_data(step_charge):
    filename = 'test.csv'

    with open(filename,'a+',newline='')as write_obj:
        write=writer(write_obj)
        write.writerow(step_charge)
   

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
init_batt(num_cell)

#get_today_usage()

fig = plt.figure()
bar_chart = plt.bar(np.arange(num_cell),cell_charge, align='center',alpha=0.5)
plt.ylim(0,100)
anim = FuncAnimation(fig, animation_frame, blit=False ,interval= 1)
plt.show()

'''
future work
how many charges can a battery store
work on exporting multiple data to csv
replace bar with line
'''
