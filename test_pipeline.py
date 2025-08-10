#!/usr/bin/env python3
"""
Test script for Citi Bikes Real-Time Streaming Project
"""

import unittest
import logging
import time
from unittest.mock import Mock, patch
from bikes_module.bikes import Bikes
from kafka_producer.producer import Producer
from kafka_consumer.consumer import Consumer
from services.http_service import HttpService
from constants.routes import BIKES_STATION_INFORMATION, BIKES_STATION_STATUS
from constants.topics import BIKES_STATION_INFORMATION_TOPIC, BIKES_STATION_STATUS_TOPIC

# Set up logging for tests
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestHttpService(unittest.TestCase):
    """Test HTTP service functionality"""
    
    def setUp(self):
        self.http_service = HttpService()
    
    def test_http_service_initialization(self):
        """Test HTTP service initialization"""
        self.assertIsNotNone(self.http_service.session)
        self.assertEqual(self.http_service.timeout, 30)
        self.assertEqual(self.http_service.max_retries, 3)
    
    def test_default_headers(self):
        """Test default headers are set correctly"""
        headers = self.http_service.session.headers
        self.assertIn('User-Agent', headers)
        self.assertIn('Accept', headers)
        self.assertIn('Content-Type', headers)
    
    def test_config_service(self):
        """Test service configuration"""
        custom_headers = {'X-Custom-Header': 'test-value'}
        result = self.http_service.config_service(custom_headers)
        
        self.assertEqual(result, self.http_service)
        self.assertEqual(self.http_service.session.headers['X-Custom-Header'], 'test-value')

class TestProducer(unittest.TestCase):
    """Test Kafka producer functionality"""
    
    @patch('kafka.KafkaProducer')
    def test_producer_initialization(self, mock_kafka_producer):
        """Test producer initialization"""
        mock_producer_instance = Mock()
        mock_kafka_producer.return_value = mock_producer_instance
        
        producer = Producer()
        
        self.assertIsNotNone(producer.producer)
        mock_kafka_producer.assert_called_once()
    
    @patch('kafka.KafkaProducer')
    def test_data_producer(self, mock_kafka_producer):
        """Test data production"""
        mock_producer_instance = Mock()
        mock_future = Mock()
        mock_future.get.return_value = Mock(partition=0, offset=123)
        mock_producer_instance.send.return_value = mock_future
        mock_kafka_producer.return_value = mock_producer_instance
        
        producer = Producer()
        result = producer.data_producer("test-topic", {"test": "data"})
        
        self.assertIsNotNone(result)
        mock_producer_instance.send.assert_called_once()

class TestConsumer(unittest.TestCase):
    """Test Kafka consumer functionality"""
    
    @patch('kafka.KafkaConsumer')
    def test_consumer_initialization(self, mock_kafka_consumer):
        """Test consumer initialization"""
        mock_consumer_instance = Mock()
        mock_kafka_consumer.return_value = mock_consumer_instance
        
        consumer = Consumer("test-group")
        
        self.assertIsNotNone(consumer.consumer)
        self.assertEqual(consumer.group_id, "test-group")
        mock_kafka_consumer.assert_called_once()
    
    @patch('kafka.KafkaConsumer')
    def test_subscribe_to_topics(self, mock_kafka_consumer):
        """Test topic subscription"""
        mock_consumer_instance = Mock()
        mock_kafka_consumer.return_value = mock_consumer_instance
        
        consumer = Consumer("test-group")
        topics = ["topic1", "topic2"]
        consumer.subscribe_to_topics(topics)
        
        mock_consumer_instance.subscribe.assert_called_once_with(topics)

class TestBikes(unittest.TestCase):
    """Test Bikes orchestrator functionality"""
    
    def setUp(self):
        self.bikes = Bikes()
    
    def test_bikes_initialization(self):
        """Test bikes orchestrator initialization"""
        self.assertIsNotNone(self.bikes.http_service)
        self.assertIsNotNone(self.bikes.producer)
        self.assertEqual(self.bikes.retry_attempts, 3)
        self.assertEqual(self.bikes.retry_delay, 5)
    
    def test_validate_station_data_valid(self):
        """Test station data validation with valid data"""
        valid_station = {
            'station_id': 'test123',
            'name': 'Test Station',
            'lat': 40.7589,
            'lon': -73.9851
        }
        
        result = self.bikes._validate_station_data(valid_station)
        self.assertTrue(result)
    
    def test_validate_station_data_invalid(self):
        """Test station data validation with invalid data"""
        invalid_station = {
            'station_id': 'test123',
            'name': 'Test Station'
            # Missing lat and lon
        }
        
        result = self.bikes._validate_station_data(invalid_station)
        self.assertFalse(result)
    
    def test_validate_status_data_valid(self):
        """Test status data validation with valid data"""
        valid_status = {
            'station_id': 'test123',
            'num_bikes_available': 5,
            'num_docks_available': 10
        }
        
        result = self.bikes._validate_status_data(valid_status)
        self.assertTrue(result)
    
    def test_validate_status_data_invalid(self):
        """Test status data validation with invalid data"""
        invalid_status = {
            'station_id': 'test123',
            'num_bikes_available': -1,  # Invalid negative value
            'num_docks_available': 10
        }
        
        result = self.bikes._validate_status_data(invalid_status)
        self.assertFalse(result)

class TestIntegration(unittest.TestCase):
    """Integration tests for the complete pipeline"""
    
    @patch('services.http_service.HttpService.get')
    @patch('kafka_producer.producer.Producer.data_producer')
    def test_end_to_end_pipeline(self, mock_producer, mock_http_get):
        """Test complete pipeline execution"""
        # Mock HTTP response
        mock_response = Mock()
        mock_response.json.return_value = {
            'data': {
                'stations': [
                    {
                        'station_id': 'test123',
                        'name': 'Test Station',
                        'lat': 40.7589,
                        'lon': -73.9851
                    }
                ]
            }
        }
        mock_http_get.return_value = mock_response
        
        # Mock producer
        mock_producer.return_value = Mock()
        
        # Create bikes instance and test
        bikes = Bikes()
        result = bikes.get_bikes_station_information("http://test.com")
        
        # Verify results
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['station_id'], 'test123')
        mock_producer.assert_called_once()

def run_performance_test():
    """Run performance test for the pipeline"""
    logger.info("🚀 Starting Performance Test")
    
    start_time = time.time()
    
    try:
        # Test producer performance
        producer = Producer()
        test_messages = [{"test": f"message_{i}"} for i in range(100)]
        
        producer_start = time.time()
        for message in test_messages:
            producer.data_producer("test-topic", message)
        producer_time = time.time() - producer_start
        
        logger.info(f"✅ Producer performance: {len(test_messages)} messages in {producer_time:.2f}s")
        logger.info(f"   Rate: {len(test_messages)/producer_time:.1f} messages/second")
        
        # Test HTTP service performance
        http_service = HttpService()
        
        http_start = time.time()
        for i in range(10):
            try:
                response = http_service.get("https://httpbin.org/get")
                logger.debug(f"HTTP request {i+1}: {response.status_code}")
            except Exception as e:
                logger.warning(f"HTTP request {i+1} failed: {e}")
        http_time = time.time() - http_start
        
        logger.info(f"✅ HTTP service performance: 10 requests in {http_time:.2f}s")
        logger.info(f"   Rate: {10/http_time:.1f} requests/second")
        
        total_time = time.time() - start_time
        logger.info(f"🎉 Performance test completed in {total_time:.2f}s")
        
    except Exception as e:
        logger.error(f"❌ Performance test failed: {e}")
        raise
    finally:
        if 'producer' in locals():
            producer.close()
        if 'http_service' in locals():
            http_service.close()

def main():
    """Run all tests"""
    logger.info("🧪 Starting Citi Bikes Pipeline Tests")
    
    # Run unit tests
    logger.info("📋 Running Unit Tests...")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Run performance tests
    logger.info("📊 Running Performance Tests...")
    run_performance_test()
    
    logger.info("🎉 All tests completed!")

if __name__ == "__main__":
    main() 