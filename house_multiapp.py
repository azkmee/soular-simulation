import random
import numpy as np

fan_prob = 0.6
tv_prob = 0.3
light_prob = 1

fan_watt = 70
tv_watt = 80
light_watt = 5

fan_volt = 24
tv_volt = 12
light_volt = 12


#convert time to one hot encoding
def time_to_arr(time):
    use = np.zeros([24])
    for i in time:
        use[i] = 1
    return use

class House:
    def __init__(self,family_size):
        #time_to_arr converts time active into a one off array
        light_use = time_to_arr([6,7,17,18,19,20,21,22])*family_size #assume 1 guy 1 bulb
        fan_use = time_to_arr([11,12,13,14,15,16,17])
        tv_use = time_to_arr([17,18,19,20])
        
        self.light_watt = 5
        self.appliance_all = {'fan':[fan_prob, fan_watt, fan_use, fan_volt],
                               'tv': [tv_prob, tv_watt,tv_use, tv_volt ],
                               'light':[light_prob, light_watt,light_use, light_volt]}
        self.appliance_list = []

        #selecting appliance
        for i in self.appliance_all:
            if (random.random()<self.appliance_all[i][0]):
                self.appliance_list.append(i)
        
    def get_demand(self):
        no_app = len(self.appliance_list)
        demand = np.zeros([no_app,24])

        #collect 1 day demand charge
        for index, i in enumerate(self.appliance_list):
            #watt/volt * appliance usage to get
            demand[index] = [x*self.appliance_all[i][1]/self.appliance_all[i][3] for x in self.appliance_all[i][2]]
        total = np.zeros([24])
        for i in range(0,24):
            for j in range(no_app):
                total[i] += demand[j,i]
        print(total)
        return total


house = House(5)
house.get_demand()

'''
future development

random variable for usage of appliances(done)
link duration of usage to data vis/trends
'''
