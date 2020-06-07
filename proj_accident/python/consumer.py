from kafka import KafkaConsumer
from json import loads


consumer = KafkaConsumer(
    'input_data_message',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group-1',
    value_deserializer=lambda m: loads(m.decode('utf-8')),
    bootstrap_servers='localhost:9092')

for m in consumer:
    print(m.value)

