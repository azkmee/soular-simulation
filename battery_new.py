##trying to compress to one code. code for charging is working but code for charge_list is not


import math
import numpy as np

class Battery():
    def __init__(self,num_cell,charge_init,min_charge=30,max_charge=95):
        self.min_charge = min_charge
        self.max_charge = max_charge
        self.num_cell = num_cell
        
        self.last_activity = np.zeros(num_cell) ##
        self.charge = [3,1,1,3,3,4,3,3,3,3]
        self.charge_score = np.full((num_cell),0)##
        self.discharge_score = np.full((num_cell),0)##
        self.penalty_village = np.full((num_cell),0)
        self.penalty_panels = np.full((num_cell),0)

    #penalize for low lowscore, for selection later
    def score_discharge(self):
        for index,charge in enumerate(self.charge):
            self.discharge_score[index]=(charge-self.min_charge)

    def score_charge(self):
        for index,charge in enumerate(self.charge):
            self.charge_score[index]=(self.max_charge-charge)

    #return a sorted list of battery id to (dis)charge based on how far it from threshold
    #num refers to how many batteries you want to (dis)charge consecutively
    def charge_list(self,charges):
        
        sorted_list = sorted(range(len(self.charge_score)),key=lambda i:self.charge_score[i],reverse=True)

        everycell = math.floor(charges/len(sorted_list))
        remain = charges%len(sorted_list)
        print('remain = ',remain)

        del_charge = np.full(self.num_cell,0)
        del_charge = [i+everycell for i in del_charge]
        print ('del_charge = ',del_charge)
        for i in sorted_list:
            del_charge[i] += 1
            remain -=1
            print('remain=',remain)
            if remain==0:
                break
                
        print(del_charge)
    
    
    def discharge_list(self,num):
        return_list = sorted(range(len(self.discharge_score)),key=lambda i:self.discharge_score[i],reverse=True)[:num]        
        #print(return_list)
        return return_list
    
    #arr input list of battery id to (dis)charge - currently, its the full array
    #charges is the amount of charge to (dis)charge
    #charge will be divided equally whenever possible
    #the rest of charges will be distributed to highest score
    def charge_(self,arr, charges):
        everycell = math.floor(charges/len(arr))
        remain = charges%len(arr)
        print('remain = ',remain)

        del_charge = np.full(self.num_cell,0)
        del_charge = [i+everycell for i in del_charge]
        print ('del_charge = ',del_charge)
        for i in arr:
            del_charge[i] += 1
            remain -=1
            print('remain=',remain)
            if remain==0:
                break
                
        print(del_charge)

    def discharge_(self,arr,charges):
        everycell = math.floor(charges/len(arr))
        remain = charges%len(arr)
        print('remain = ',remain)

        del_charge = np.full(self.num_cell,0)
        del_charge = [i+everycell for i in del_charge]
        print ('del_charge = ',del_charge)
        for i in arr:
            del_charge[i] += 1
            remain -=1
            print('remain=',remain)
            if remain==0:
                break
                
        print(del_charge)
    #shortened (dis)charge function
    def charging(self, target_num,charges):
        #print(self.charge)
        self.score_charge() ##update battery score
        batt_list = self.charge_list(target_num)
        self.charge_(batt_list,charges)
        #print(self.charge)

    def discharging(self, target_num,charges):
        #print(self.charge)
        self.score_discharge() ##update battery score
        batt_list = self.discharge_list(target_num)
        self.discharge_(batt_list,charges)
        #print(self.charge)

    #get charge left
    def get_charge(self):
        return self.charge

new_batt = Battery(10,50)
new_batt.charge_list(59)

'''
to use command:

initialize with number of cells
new_batt=Battery(10)

to charge battery(number of cell to distribute,charge)
new_batt.charging(3,20)
new_batt.discharging(3,20)

to get charge level
new_batt.get_charge()
'''


#next plan
#weight on scoring
