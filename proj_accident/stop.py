from kafka import KafkaAdminClient
import os

admin = KafkaAdminClient(bootstrap_servers='localhost:9092')

os.system('pkill -9 -f app.py')
os.system('pkill -9 -f consumer.py')
os.system('pkill -9 -f producer.py')

admin.delete_topics(['dashboard1', 'clickhouse1'])
admin.close()

#os.system('sudo docker stop $(sudo docker ps -a -q)')
