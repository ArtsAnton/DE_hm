import time
from kafka import KafkaProducer, KafkaClient
from json import dumps


parameter = ['time', 'total_eccs_imf', 'flow_rate_loop_1', 'flow_rate_loop_2',
             'flow_rate_loop_3', 'water_level_1', 'water_level_2', 'water_level_3', 'coolant_mass_loop_1',
             'coolant_mass_loop_2', 'coolant_mass_loop_3', 'reactivity', 'prz_water_level', 'total_heat_power_2',
             'saturation_temperature', 'total_power', 'pump_velocity_loop_1', 'pump_velocity_loop_2',
             'pump_velocity_loop_3', 'pressure', 'cladding_temperature_1', 'cladding_temperature_2',
             'cladding_temperature_3', 'fuel_temperature_1', 'fuel_temperature_2', 'fuel_temperature_3',
             'secondary_side_pressure', 'rate_flow_break', 'bru_a_flow_rate_loop_1', 'bru_a_flow_rate_loop_3',
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
                    producer.send('dashboard1', value=message(parameter, line))
                    producer.send('clickhouse1', value=message(parameter, line))
                else:
                    time.sleep((line[0] - prev_step)/10)
                    producer.send('dashboard1', value=message(parameter, line))
                    producer.send('clickhouse1', value=message(parameter, line))
            except ValueError:
                break


if __name__ == '__main__':
    client = KafkaClient(bootstrap_servers='localhost:9092')
    client.add_topic('dashboard1')
    client.add_topic('clickhouse1')
    client.close()
    generator()
