from kafka import KafkaConsumer
from json import loads
from clickhouse_driver import Client


client = Client(host='localhost', port=9000)
client.execute('CREATE DATABASE IF NOT EXISTS parameter')
client.execute('USE parameter')
client.execute("DROP TABLE IF EXISTS parameter.param")
client.execute(
    'CREATE TABLE IF NOT EXISTS parameter.param ('
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


consumer = KafkaConsumer(
    'input_data_message',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group-1',
    value_deserializer=lambda m: loads(m.decode('utf-8')),
    bootstrap_servers='localhost:9092')


for m in consumer:
    client.execute('INSERT INTO parameter.param VALUES  (%s)' % ', '.join(list(map(str, m.value.values()))))

