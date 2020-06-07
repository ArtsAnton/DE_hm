import time
from kafka import KafkaProducer
from json import dumps


parameter = ['time', 'total_ECCS_imf', 'flow_rate_loop_1', 'flow_rate_loop_2',
             'flow_rate_loop_2', 'water_level_1', 'water_level_2', 'water_level_3', 'coolant_mass_loop_1',
             'coolant_mass_loop_2', 'coolant_mass_loop_3', 'Reactivity', 'PRZ_water_level_(m)', 'total_heat_power_2',
             'saturation_temperature', 'total_power', 'total_ECCS_imf', 'pump_velocity_loop_1', 'pump_velocity_loop_2',
             'pump_velocity_loop_3', 'Pressure', 'cladding_temperature_1', 'cladding_temperature_2',
             'cladding_temperature_3', 'fuel_temperature_1', 'fuel_temperature_2', 'fuel_temperature_3',
             'secondary_side_pressure', 'rate_flow_break', 'BRU_A_flow_rate_loop_1', 'BRU_A_flow_rate_loop_3',
             'core_coolant_flow_rate']


def message(list_1, list_2):
    mes = {list_1[i]: list_2[i] for i in range(len(list_1))}
    return mes


def generator(file_name="transform_data/data.csv"):
    producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda m: dumps(m).encode('utf-8'))
    line = [0]
    with open(file_name, "r") as text:
        while True:
            prev_step = line[0]
            try:
                line = list(map(float, text.readline().split(",")))
                if float(round(line[0], 1)) == 0:
                    producer.send('input_data_message', value=message(parameter, line))
                else:
                    time.sleep((line[0] - prev_step))
                    producer.send('input_data_message', value=message(parameter, line))
            except ValueError:
                break


generator()

