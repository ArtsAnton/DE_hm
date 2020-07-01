import os
import time
from subprocess import Popen, call
import subprocess

os.system('echo Starting Docker')
os.system('sudo docker-compose up -d')

os.system('echo')
os.system('echo $(sudo docker ps --format "{{.Names}}")')
os.system('echo')

time.sleep(3)
os.chdir('python')

Popen(['/usr/bin/python3', 'producer.py'])
Popen(['/usr/bin/python3', 'consumer.py'])
Popen(['/usr/bin/python3', 'app.py'])

os.system('google-chrome -private-window "http://127.0.0.1:3000/"')
os.system('google-chrome -private-window "http://127.0.0.1:5000/"')

os.system('sudo docker exec -it clickhouse-server1 /bin/bash')