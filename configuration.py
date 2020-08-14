from per_config_run import compile_
from csv import writer
import numpy as np
from statistics import mean
import time
import seaborn as sns
import pandas as pd
import scipy.stats as st
import math

year_sim = 1
sim_days = 360 * 24 * year_sim
price_battery = 74
price_panel = 720 #1.80/w
price_per_kwh = 0.2613

#file to get distribution from
data_dist = pd.read_csv('data_dist_20_B.csv')
#output file name
filename = 'output_test.csv'
num_house = 5

#export data to csv containing config and penalty
def collect_data(cell,panel,penalty1, penalty2, sum_d):
    cost = cell*price_battery + panel*price_panel
    with open(filename,'a+',newline='') as write_obj:
        write=writer(write_obj)
        write.writerow([cell,panel,mean(penalty1),mean(penalty2),cost, sum_d*price_per_kwh])

def init_excel():
    with open(filename,'w',newline='') as write_obj:
        write=writer(write_obj)
        write.writerow(['cells','panels','penalty_v', 'penalty_p', 'cost', 'sum_d'])

def demand_gen_multi_dist():
    # i=0
    demand = []
    for year in range(year_sim):
        for month in range(12):
            for day in range(30):   
                for hour in range(24):
                    _, dist, params = data_dist.iloc[2*month+hour]
                    parame = [float(i) for i in params.strip('[]').split(',')]
                    arg = parame[:-2]
                    loc = parame[-2]
                    scale = parame[-1]

                    
                    eqn = eval('st.' + dist +'.rvs(loc=loc, scale=scale, *arg, size=num_house)')
                    while math.isinf(sum(eqn)):
                        eqn = eval('st.' + dist +'.rvs(loc=loc, scale=scale, *arg, size=num_house)')
                    demand.append(sum(eqn))
    return(demand)

def main():
    init_excel()
    sim_run = 1
    for i in range(sim_run):
        d = demand_gen_multi_dist()

#two options for for loop, 1. wider range. 2. narrower range after initial analysis

        for panels in range(20,101,20):
            for batt in range(70,251,40):
        # for panels in range(40,80, 5):
        #     for batt in range(70, 201, 10):
                p1 = np.full(batt,0.0)
                p2 = np.full(batt,0.0)
                cha, p_v, p_p = compile_(batt,panels, d, sim_days)
                print(panels, batt, cha, p_p)

                collect_data(batt,panels,p_v,p_p, sum(d))

if __name__ == '__main__':
    main()