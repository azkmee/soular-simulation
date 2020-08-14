import math
import numpy as np
'''
to use class object:

initialize with number of batteries and initial charge(in percentage batt)
new_batt=Battery(10,0.5)

to (dis)charge battery,
new_batt.charging(charges)
new_batt.discharging(discharges)

to get battery details
new_batt.get_battery_details()
returns charge array and penalty array
'''

class Battery():
    def __init__(self,num_cell,charge_init,min_charge=0.30,max_charge=0.95):
        self.capacity = 60 * 12 /1000 #Ah x V = Kwatthr

        self.min_charge = min_charge * self.capacity
        self.max_charge = max_charge * self.capacity #or full?
        self.num_cell = num_cell
        self.charge = np.full(num_cell,np.float(charge_init*self.capacity))
        self.penalty_village = np.full((num_cell),0.0)
        self.penalty_panels = np.full((num_cell),0.0)


    def charging(self,charges):        
        #accumulate penalty my taking charges that didnt make it
        #equal distribution of charges
        self.charge += np.array(charges/self.num_cell)
        self.penalty_panels += np.array([max(0,i-self.max_charge) for i in self.charge])
        self.charge = [min(i,self.capacity) for i in self.charge] #limits charge, possible to penalize


    def discharging(self,charges):
       
        #update charge
        self.charge -= np.array(charges/self.num_cell)
        self.penalty_village += np.array([max(0.0,self.min_charge-i) for i in self.charge])
        self.charge = [max(i,0.0) for i in self.charge]
    
    def get_battery_details(self):
        soc = [float(i/self.capacity) for i in self.charge]
        #print(soc, self.charge, self.penalty_panels)
        return (soc,self.penalty_village, self.penalty_panels)
 


