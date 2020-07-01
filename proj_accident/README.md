# Финальный проект [Otus DE](https://otus.ru/lessons/data-engineer/?int_source=courses_catalog&int_term=data-science)
## Назанчение проекта
Анализ состояния энергетического объекта (сбор и хранение информации теплогидравлических параметров системы в элементах оборудования)
## Данные
Используемые в проетке данные представляют собой набор теплогидравлических параметров описывающих аварийный процес на энергетическом объекте.
Данные получены с помощью теплогидравлического кода [relap5 mod 3.2](https://en.wikipedia.org/wiki/RELAP5-3D).
## Технологии
- [Docker;](https://www.docker.com/)
- [Apache Kafka;](https://kafka.apache.org/)
- [Apache Zookeeper;](https://zookeeper.apache.org/)
- [Clickhiuse;](https://clickhouse.tech/)
- [Grafana;](https://grafana.com/)
- [ClickHouse datasource for Grafana;](https://github.com/Vertamedia/clickhouse-grafana)
- [Python;](https://www.python.org/)
- [Smoothie.js.](http://smoothiecharts.org/)
## Модули Pytnon
- [Clickhouse-driver;](https://clickhouse-driver.readthedocs.io/en/latest/index.html)
- [Pykafka;](https://pykafka.readthedocs.io/en/latest/index.html)
- [Kafka-python.](https://kafka-python.readthedocs.io/en/master/index.html)
## Структура проекта
- [app.py](https://github.com/ArtsAnton/DE_hm/blob/master/proj_accident/python/app.py) - Flask приложение для визуализации графиков аварийного процесса в real-time. Читает данные из соответствующего топика Kafka;
- [consumer.py](https://github.com/ArtsAnton/DE_hm/blob/master/proj_accident/python/consumer.py) - пишет данные в Ckickhouse. Данные читает из соответствующего топика Kafka;
- [producer.py](https://github.com/ArtsAnton/DE_hm/blob/master/proj_accident/python/producer.py) - создает два топика в Kafka и отправляет сообщения для  app.py и consumer.py; 
- [start.py](https://github.com/ArtsAnton/DE_hm/blob/master/proj_accident/start.py) - запускает проект (1. Запускает Docker 2. Добавляет в Kafka топики для Clickhouse и flask приложения 3. Запускает producer.py, app.py, consumer.py. 4. Открывает в окнах браузера Flask приложение (app.py) и Grafana;   
- [stop.py](https://github.com/ArtsAnton/DE_hm/blob/master/proj_accident/stop.py) - останавливает app.py, roducer.py, consumer.py.
