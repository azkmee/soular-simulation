# soular-simulation

This is part of the capstone project under simulation model to find the recommended configuration for battery and solar panel

This file contain 3 main python files.

battery.py - incharge of the charging and discharging of battery
per_config_run.py - simulation run that takes in the configuration and return penalties of configuration
configuration.py - compile penalties for every configuration ran.

To run this program, you need an input file which contains the distribution of energy distribution for each hour per month in an excel file. 
This can be obtained by fitting a distribution curve to existing data. That can be found here: https://www.kaggle.com/muhdazmi2/london-electric/notebook

This folder also contains samples of data distribution obtained from energy usage from London dataset. The files are named data_dist_A.csv
