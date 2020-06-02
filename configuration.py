from chart import compile_
from csv import writer
import numpy as np
from statistics import mean

sim_days = 20
sim_per_config = 5

#export data to csv containing config and penalty
def collect_data(cell,panel,penalty1,penalty2):
    filename = 'test.csv'

    with open(filename,'a+',newline='') as write_obj:
        write=writer(write_obj)
        write.writerow([cell,panel,mean(penalty1),mean(penalty2)])

def init_excel():
    filename = 'test.csv'

    with open(filename,'w',newline='') as write_obj:
        write=writer(write_obj)
        write.writerow(['cells','panels','village penalty','panels penalty'])

def main():
    global sim_days, sim_per_config
    init_excel()

    for panels in range(1,20):
        for batt in range(1,50):
            p_village = np.full(batt,0)
            p_panels = np.full(batt,0)
            for _ in range(sim_per_config):
                p_v, p_p = compile_(batt,panels)
                print(panels, batt, p_panels, p_p, p_v)
                p_village += p_v
                p_panels += p_p

            p_village = [j/sim_per_config for j in p_village]
            p_panels = [j/sim_per_config for j in p_panels]

            collect_data(batt,panels,p_village,p_panels)

if __name__ == '__main__':
    main()