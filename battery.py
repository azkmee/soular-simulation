import math
import numpy as np
'''
to use class object:

initialize with number of batteries and initial charge
new_batt=Battery(10,50)

to (dis)charge battery,
new_batt.charging(charges)
new_batt.discharging(discharges)

to get charge level
new_batt.get_charge()
'''
class Battery():
    def __init__(self,num_cell,charge_init,min_charge=30,max_charge=95):
        self.min_charge = min_charge
        self.max_charge = max_charge
        self.num_cell = num_cell
        self.capacity = 125
        '''np.array([\
                np.float(35),np.float(76),np.float(34),\
                        np.float(22),np.float(67),np.float(85),\
                                np.float(34),np.float(34),np.float(45),\
                                        np.float(56)]) #'''
        self.charge = np.full(num_cell,np.float(charge_init))
        self.penalty_village = np.full((num_cell),0)
        self.penalty_panels = np.full((num_cell),0)


    def charging(self,charges):
        charge_score = np.full(self.num_cell,0)
#       penalizing for low score. higher score = further current charge from threshold
        for index,charge in enumerate(self.charge):
            charge_score[index]=(self.max_charge-charge)  
#       sort battery index
        sorted_list = sorted(range(len(charge_score)),key=lambda i:charge_score[i],reverse=True)
#       print('sorted list', sorted_list)
#       sort out charges to assign to each batteries
        everycell = math.floor(charges/len(sorted_list))
        remain = charges%len(sorted_list)
#       print('remain = ',remain)

        del_charge = np.full(self.num_cell,0)
        del_charge = [i+everycell for i in del_charge]
#       print ('del_charge = ',del_charge)
        if remain != 0:
            for i in sorted_list:
                del_charge[i] += 1
                remain -=1
#               print('remain=',remain)
                if remain==0:
                    break
                
        self.charge += np.array(del_charge)/self.capacity*100
        self.penalty_panels += np.array([int(i>self.max_charge) for i in self.charge])


    def discharging(self,charges):
        charge_score = np.full(self.num_cell,0)
#       penalizing for low score. higher score = further current charge from threshold
        for index,charge in enumerate(self.charge):
            charge_score[index]=(charge - self.min_charge)
#       sort battery index
        sorted_list = sorted(range(len(charge_score)),key=lambda i:charge_score[i],reverse=True)    
#       print(sorted_list)

        everycell = math.floor(charges/len(sorted_list))
        remain = charges%len(sorted_list)
#       print('sorted list', sorted_list)
#       sort out charges to assign to each batteries

        del_charge = np.full(self.num_cell,0)
        del_charge = [i+everycell for i in del_charge]
#       print ('del_charge = ',del_charge)
        if remain != 0:
            for i in sorted_list:
                del_charge[i] += 1
                remain -=1
#               print('remain=',remain)
                if remain==0:
                    break

        self.charge -= np.array(del_charge)/self.capacity*100
        self.penalty_village += np.array([int(i<self.min_charge) for i in self.charge])
    
    def get_charge_penalties(self):
        return (self.charge,self.penalty_village,self.penalty_panels)
 

new_batt = Battery(10,50)
new_batt.discharging(60)


