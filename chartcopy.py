import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.animation import FuncAnimation
from house_multiapp import House
from battery import Battery
from csv import writer
import math
from statistics import mean
import scipy.stats as st

import sys

#PER DAY SIM
days_sim = 365 * 3

num_cell = 16
default_charge = 0.50 #state of charge in %
num_house = 4

number_panels = 42
sun_h = 5
panel_power_h = 2.4/sun_h * 1.6#2.4 kwh/m2 from report

cell_charge = [default_charge for i in range(num_cell)]

#for charging
#day_time = [9,10,11,12,13,14,15,16]

#houses = {}

#today_charge = []

#initialize house and battery at the start

def init_batt(cell):
    global battery
    
    battery = Battery(cell,charge_init=default_charge)

#charge based on scoring
def del_charge2(charge):
    global battery
    
    #discharging
    if (charge<0):
        battery.discharging(abs(charge))

    #charging
    elif (charge>0):
        battery.charging(abs(charge))
    
    #UNCOMMENT BELOW
    return battery.get_battery_details()

#REPLACE WITH EXPECTED CHARGE FROM 5HOURS OF CHARGING(CAN VARY EFFICIENCY/IRRIDIANCE)

def solar_charge(): #insert formula of solar charging based on t
    #assume 5 hrs of charging from 11-1600hrs with power harvested as percentage
    #of max capacity (efficiency accounted for)
    irr = np.array([0.3, 0.3, 0.3, 0.2, 0.2])

    return sum(irr) * panel_power_h

#get demand at time t
#GET DAY DEMAND, FROM RANDOM VAR
#can incorporate with the analysis
#hard code var first, to include with *arg later
#calculated in kWh q
import scipy.stats as st
def village_discharge():
    c = 0.4275538254258593
    s = 0.3170056615664818
    loc = -3.185672416927618
    scale = 8.550998664138763

    

    today_charge = st.powerlognorm.rvs(c=c, s=s, loc=loc, scale=scale)
    #print(today_charge[t])
    return today_charge

#for animation function
#EVERY FRAME IS PER DAY
def animation_frame(i):
    global bar_chart

    #if new day NO NEED
    #if i%48==0:
        #get_today_usage()
        
    #time = math.floor(i/2)%24
    #charge = solar_charge(time)
    #discharge = village_discharge(time)
    #diff = charge + discharge
    '''
    if i%2==0:
        diff = solar_charge(time,number_panels)
    else:
        diff = village_discharge(time)
    '''
    #update cell charge
    today_charge = sum([solar_charge() for _ in range(number_panels)])
    today_discharge = sum([village_discharge() for j in range(num_house)])
    diff = today_charge - today_discharge
    print(today_charge, today_discharge,diff)
    updated_charge, p_village, p_p = del_charge2(diff)
    print(p_p)
    #export to csv
    #collect_data(updated_charge)
    for k, b in enumerate(bar_chart):
        b.set_height(updated_charge[k])

    if (i==days_sim): sys.exit()

#low_var_demand = [village_discharge() for i in range(days_sim)]

#NOT YET USED
def compile_(ncell, npanels, demand_low_var, days_sim_):
    global battery
    init_batt(ncell)

    #interval = 20 * 48

    for i in range(days_sim_):
        today_charge = sum([solar_charge() for _ in range(npanels)])
        today_discharge = demand_low_var[i] #house declare from sourc of demand
        diff = today_charge - today_discharge
        del_charge2(diff)

    _, penalty1, penalty2 = battery.get_battery_details()
    
    return (_,penalty1, penalty2)
    #returns penalty in array

    


def main():
    global bar_chart    
    #initialize houses and batteries
    #init_house(num_house)
    init_batt(num_cell)

    fig = plt.figure()
    bar_chart = plt.bar(np.arange(num_cell),cell_charge, align='center',alpha=0.5)
    plt.ylim(0,1.5)
    anim = FuncAnimation(fig, animation_frame, blit=False ,interval= 1)
    plt.show()

if __name__ == '__main__':
    #a,b = compile_(ncell=1,npanels=2)
    #print(a.b)
    main()                
        
'''
future work
how many charges can a battery store
work on exporting multiple data to csv
replace bar with line
'''
