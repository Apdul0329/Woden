import os
import json
from confluent_kafka import Producer


class KafkaProducer:
    def __init__(self):
        conf = {
            'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP', 'localhost:9092'),
        }
        self.producer = Producer(conf)

    def send_event(self, event_type, event_data):
        topic = event_type
        data = json.dumps(event_data).encode('utf-8')
        self.producer.produce(
            topic=topic,
            value=data
        )
        self.producer.flush()
