from json import loads
from clickhouse_driver import connect
from pykafka import KafkaClient


def get_kafka_client():
    return KafkaClient(hosts='127.0.0.1:9092')


parameter = ['time', 'total_eccs_imf', 'flow_rate_loop_1', 'flow_rate_loop_2',
             'flow_rate_loop_3', 'water_level_1', 'water_level_2', 'water_level_3', 'coolant_mass_loop_1',
             'coolant_mass_loop_2', 'coolant_mass_loop_3', 'reactivity', 'prz_water_level', 'total_heat_power_2',
             'saturation_temperature', 'total_power', 'pump_velocity_loop_1', 'pump_velocity_loop_2',
             'pump_velocity_loop_3', 'pressure', 'cladding_temperature_1', 'cladding_temperature_2',
             'cladding_temperature_3', 'fuel_temperature_1', 'fuel_temperature_2', 'fuel_temperature_3',
             'secondary_side_pressure', 'rate_flow_break', 'bru_a_flow_rate_loop_1', 'bru_a_flow_rate_loop_3',
             'core_coolant_flow_rate']


connect = connect('clickhouse://localhost')
cursor = connect.cursor()
cursor.execute('CREATE DATABASE IF NOT EXISTS parameter')
cursor.execute('USE parameter')
cursor.execute('DROP TABLE IF EXISTS param')

cursor.execute(
    'CREATE TABLE IF NOT EXISTS param ('
    'time Float32,'
    'total_eccs_imf Float32,'
    'flow_rate_loop_1 Float32,'
    'flow_rate_loop_2 Float32,'
    'flow_rate_loop_3 Float32,'
    'water_level_1 Float32,'
    'water_level_2 Float32,'
    'water_level_3 Float32,'
    'coolant_mass_loop_1 Float32,'
    'coolant_mass_loop_2 Float32,'
    'coolant_mass_loop_3 Float32,'
    'reactivity Float32,'
    'prz_water_level Float32,'
    'total_heat_power_2 Float32,'
    'saturation_temperature Float32,'
    'total_power Float32,'
    'pump_velocity_loop_1 Float32,'
    'pump_velocity_loop_2 Float32,'
    'pump_velocity_loop_3 Float32,'
    'pressure Float32,'
    'cladding_temperature_1 Float32,'
    'cladding_temperature_2 Float32,'
    'cladding_temperature_3 Float32,'
    'fuel_temperature_1 Float32,'
    'fuel_temperature_2 Float32,'
    'fuel_temperature_3 Float32,'
    'secondary_side_pressure Float32,'
    'rate_flow_break Float32,'
    'bru_a_flow_rate_loop_1 Float32,'
    'bru_a_flow_rate_loop_3 Float32,'
    'core_coolant_flow_rate Float32'
    ') ENGINE = Memory'
)


client = get_kafka_client()
topic = client.topics['clickhouse1']

test = []
for m in topic.get_simple_consumer():
    test.append(loads(m.value.decode()))
    if len(test) == 20:
        cursor.executemany('INSERT INTO param ({}) VALUES'.format(', '.join(parameter)), test)
        connect.commit()
        test = []

