import os
import csv


parameter = ['time', 'total_ECCS_imf_(kg/s)', 'flow_rate_loop_1_(kg/s)', 'flow_rate_loop_2_(kg/s)',
             'flow_rate_loop_2_(kg/s)', 'water_level_1_(m)', 'water_level_2_(m)', 'water_level_3_(m)',
             'coolant_mass_loop_1_(kg)', 'coolant_mass_loop_2_(kg)', 'coolant_mass_loop_3_(kg)', 'Reactivity_($)',
             'PRZ_water_level_(m)', 'total_heat_power_2_(J)', 'saturation_temperature_(K)', 'total_power_(W)',
             'pump_velocity_loop_1_(rad/s)', 'pump_velocity_loop_2_(rad/s)',
             'pump_velocity_loop_3_(rad/s)', 'Pressure_(Pa)', 'cladding_temperature_1_(K)',
             'cladding_temperature_2_(K)', 'cladding_temperature_3_(K)', 'fuel_temperature_1_(K)',
             'fuel_temperature_2_(K)', 'fuel_temperature_3_(K)', 'secondary_side_pressure_(Pa)',
             'rate_flow_break_(kg/s)', 'BRU_A_flow_rate_loop_1_(kg/s)', 'BRU_A_flow_rate_loop_3_(kg/s)',
             'core_coolant_flow_rate_(kg/s)']

directory = os.listdir('input_data')
directory.sort()
n = 0
while True:
    try:
        mas = []
        with open('input_data/{}'.format(directory[0]), 'r') as f:
            i = f.readlines()
            mas.extend(i[n].split())

        for file in directory[1:]:
            with open('input_data/{}'.format(file), 'r') as f:
                i = f.readlines()
                mas.append(i[n].strip().split()[1])

        with open('transform_data/data.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(mas)

        if n % 100 == 0:
            print(n)
        n += 1
    except IndexError:
        with open('transform_data/parametr.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(parameter)
        break



