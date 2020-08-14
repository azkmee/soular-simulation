import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.animation import FuncAnimation
from battery import Battery
import math
from statistics import mean
import scipy.stats as st
import sys
import pandas as pd

#PER DAY SIM
days_sim = 24*365

# num_cell = 100
# x = 0.50 #state of charge in %
default_charge = 0.3
# number_panels = 85
# sun_h = 5
panel_power_h = 0.400 #2.4/sun_h * 1.6#2.4 kwh/m2 from report

# cell_charge = [default_charge for i in range(num_cell)]
solar_efficiency = np.zeros(24)
solar_efficiency[11]=0.8
solar_efficiency[12]=0.8
solar_efficiency[13]=0.8
solar_efficiency[14]=0.8
solar_efficiency[15]=0.8

#initialize house and battery at the start

def init_batt(cell):
    global battery
    
    battery = Battery(cell,charge_init=default_charge)

#charge
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

def compile_(ncell, npanels, demand_low_var, days_sim_):
    global battery
    init_batt(ncell)

    #interval = 20 * 48

    for i in range(days_sim_):
        time = i%24
        hour_charge = solar_efficiency[time] * npanels * panel_power_h
        hour_discharge = demand_low_var[i] 
        diff = hour_charge - hour_discharge
        del_charge2(diff)
        #print(diff)

    _, penalty1, penalty2 = battery.get_battery_details()
    
    return (_,penalty1, penalty2)
    #returns penalty in array
