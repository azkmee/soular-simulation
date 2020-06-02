import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.animation import FuncAnimation
from house_multiapp import House
from battery import Battery
from csv import writer
import math
from statistics import mean

import sys

num_cell = 5
default_charge = 50 #state of charge
num_house = 10

number_panels = 3
panel_voltage = 24
perhour_charge = 200/panel_voltage #change to current

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

#update the demand for electricity today in today_charge
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

#charge based on scoring
def del_charge2(charge):
    global battery
    
    #discharging
    if (charge<0):
        battery.discharging(abs(charge))

    #charging
    elif (charge>0):
        battery.charging(abs(charge))
    
    #return battery.get_charge_penalties()

def solar_charge(t,panels): #insert formula of solar charging based on t
    
    if (t in day_time):
        return perhour_charge * panels#+ randomness()
    else: return 0

#get demand at time t
def village_discharge(t):
    #print(today_charge[t])
    return int(today_charge[t])*-1



#for animation function
#each our is per 2 frame. One frame for charging, the other for discharging
def animation_frame(i):
    global bar_chart

    #if new day
    if i%48==0:
        get_today_usage()
        
    time = math.floor(i/2)%24
    #charge = solar_charge(time)
    #discharge = village_discharge(time)
    #diff = charge + discharge
    if i%2==0:
        diff = solar_charge(time,number_panels)
    else:
        diff = village_discharge(time)

    #update cell charge
    updated_charge, p_village, p_panels = del_charge2(diff)
    #export to csv
    #collect_data(updated_charge)
    print(time, updated_charge)
    print(p_village,p_panels)
    for k, b in enumerate(bar_chart):
        b.set_height(updated_charge[k])

    if (i==(48*20)): sys.exit()

def compile_(ncell, npanels):
    global battery
    init_house(num_house)
    init_batt(ncell)

    interval = 20 * 48

    for i in range(interval):
        if i%48 == 0:
            get_today_usage()
        
        time = math.floor(i/2)%24

        if time%2 == 0:
            diff = solar_charge(time, npanels)
        else:
            diff = village_discharge(time)
        del_charge2(diff)

    updated_charge, p_village, p_panels = battery.get_charge_penalties()
    
    return p_village,p_panels


def main():
    global bar_chart    
    #initialize houses and batteries
    init_house(num_house)
    init_batt(num_cell)

    fig = plt.figure()
    bar_chart = plt.bar(np.arange(num_cell),cell_charge, align='center',alpha=0.5)
    plt.ylim(0,100)
    anim = FuncAnimation(fig, animation_frame, blit=False ,interval= 1)
    plt.show()

if __name__ == '__main__':
    a,b = compile_(ncell=1,npanels=2)
    print(a.b)
    #main()                
        
'''
future work
how many charges can a battery store
work on exporting multiple data to csv
replace bar with line
'''
