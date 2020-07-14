from chartcopy import compile_
from csv import writer
import numpy as np
from statistics import mean
import time
import seaborn as sns
import pandas as pd
import scipy.stats as st

sim_days = 365 * 3
#sim_per_config = 5
price_battery = 74
price_panel = 400
price_per_kwh = 26.13

##see if can use df here

#export data to csv containing config and penalty
def collect_data(cell,panel,penalty1, penalty2, sum_d):
    filename = 'test2.csv'
    cost = cell*price_battery + panel*price_panel
    with open(filename,'a+',newline='') as write_obj:
        write=writer(write_obj)
        write.writerow([cell,panel,mean(penalty1),mean(penalty2),cost, sum_d*price_per_kwh])

def init_excel():
    filename = 'test2.csv'

    with open(filename,'w',newline='') as write_obj:
        write=writer(write_obj)
        write.writerow(['cells','panels','penalty_v', 'penalty_p', 'cost', 'sum_d'])

def low_var_demand_gen():
    demand = []
    num_house = 5
    c = 0.4275538254258593
    s = 0.3170056615664818
    loc = -3.185672416927618
    scale = 8.550998664138763
    for i in range(sim_days):
        demand.append(sum(st.powerlognorm.rvs(c=c, s=s, loc=loc, scale=scale, size=num_house)))
    return demand

def main():
    #global sim_per_config
    init_excel()
    for i in range(3):
        #get new set of demand rv for every run
        d = low_var_demand_gen()
        #try to cut down the sim
        #p_store = np.ones(10) * 10

        for panels in range(40,56):
            for batt in range(35,50):
                p1 = np.full(batt,0.0)
                p2 = np.full(batt,0.0)
                #for _ in range(sim_per_config):
                cha, p_v, p_p = compile_(batt,panels, d, sim_days)
                print(panels, batt, cha, p_p)
                #p1 += p_v
                #p2 += p_p

                #average penalty in the config
                #p1 = [j/sim_per_config for j in p1]
                #p2 = [j/sim_per_config for j in p2]

                collect_data(batt,panels,p_v,p_p, sum(d))

    '''
    time.sleep(5)
    data = pd.read_csv('test.csv')
    print(len(data))
    data['sum'] = 2*data['penalty'] + data['cost']
    data1 = data.pivot('cells','panels','sum')
    sns.heatmap(data1)
    '''

if __name__ == '__main__':
    main()