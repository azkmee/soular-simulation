from chartcopy import compile_
from csv import writer
import numpy as np
from statistics import mean
import time
import seaborn as sns
import pandas as pd

sim_days = 20
sim_per_config = 5
price_battery = 20
price_panel = 30

##see if can use df here

#export data to csv containing config and penalty
def collect_data(cell,panel,penalty):
    filename = 'test.csv'
    cost = cell*price_battery + panel*price_panel
    with open(filename,'a+',newline='') as write_obj:
        write=writer(write_obj)
        write.writerow([cell,panel,mean(penalty),cost])

def init_excel():
    filename = 'test.csv'

    with open(filename,'w',newline='') as write_obj:
        write=writer(write_obj)
        write.writerow(['cells','panels','penalty', 'cost'])

def main():
    global sim_per_config
    init_excel()

    #try to cut down the sim
    p_store = np.ones(10) * 10

    for panels in range(25,50):
        for batt in range(10,40):
            p = np.full(batt,0)
            for _ in range(sim_per_config):
                p_v = compile_(batt,panels)
                print(panels, batt, p_v)
                p += p_v

            #average penalty in the config
            p = [j/sim_per_config for j in p]

            collect_data(batt,panels,p)

    time.sleep(5)
    data = pd.read_csv('test.csv')
    print(len(data))
    data['sum'] = 2*data['penalty'] + data['cost']
    data1 = data.pivot('cell','panels','sum')
    sns.heatmap(data1)


if __name__ == '__main__':
    main()