import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.http_service import HttpService
from kafka_producer.producer import Producer
from constants.topics import BIKES_STATION_INFORMATION_TOPIC, BIKES_STATION_STATUS_TOPIC


class Bikes:
    def __init__(self):
        self.http_service = HttpService()
        self.producer = Producer()
        
    def get_bikes_station_information(self, url, params={}):
        response = self.http_service.get(url, params).json()
        for message in response['data']['stations']:
            print("bikes_station_information", message)
            self.producer.data_producer(BIKES_STATION_INFORMATION_TOPIC, message)
            
    def get_bikes_station_status(self, url, params={}):
        response = self.http_service.get(url, params).json()
        for message in response['data']['stations']:
            print("bikes_station_status", message)
            self.producer.data_producer(BIKES_STATION_STATUS_TOPIC, message)