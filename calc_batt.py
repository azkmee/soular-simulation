#daily use - expected daily usage of electricity in wH
#days_idle - number of days expected to not charged from solar
#min_dod - minimum charge to avoid deterioration of battery
#batt_cap - capacity of one battery
#solar_power - power capacity of a solar panel in W ??
#eff_system - efficiency of system
#eff_solar - solar panel efficiency


def get_batt(daily_use, days_idle, min_dod, batt_cap, solar_power, eff_sys = 0.8, eff_solar = 0.8):
    total_energy_needed = daily_use * days_idle / eff_sys / (1-min_dod)
    number_batt = total_energy_needed/batt_cap
    number_solar = total_energy_needed / eff_solar / (solar_power * 5) #hrs of sun

    return (ceil(number_batt), ceil(number_solar))

