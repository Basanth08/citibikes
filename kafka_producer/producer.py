import json
from kafka import KafkaProducer
from constants.routes import BIKES_STATION_INFORMATION, BIKES_STATION_STATUS
from constants.topics import BIKES_STATION_INFORMATION_TOPIC, BIKES_STATION_STATUS_TOPIC

class Producer:
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                                      value_serializer=lambda x: json.dumps(x).encode('utf-8'))
        
    def data_producer(self, topic, message):
        self.producer.send(topic, message)
        self.producer.flush()  # Ensure message is sent immediately
        
    def close(self):
        self.producer.close()
        
        

