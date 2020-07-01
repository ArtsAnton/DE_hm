from flask import Flask, render_template, Response
from pykafka import KafkaClient

app = Flask(__name__)


def get_kafka_client():
    return KafkaClient(hosts='127.0.0.1:9092')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/topic/dashboard1')
def get_messages():
    def events():
        client = get_kafka_client()
        for i in client.topics['dashboard1'].get_simple_consumer():
            yield 'data:{0}\n\n'.format(i.value.decode())
    return Response(events(), mimetype="text/event-stream")


if __name__ == '__main__':
    app.run()
