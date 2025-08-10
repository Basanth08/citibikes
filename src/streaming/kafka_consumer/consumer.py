import json
import logging
from kafka import KafkaConsumer
from typing import List, Dict, Any

class Consumer:
    def __init__(self, group_id: str = "bikes-consumer-group"):
        """
        Initialize Kafka Consumer
        
        Args:
            group_id (str): Consumer group ID for offset management
        """
        self.group_id = group_id
        self.consumer = None
        self.logger = logging.getLogger(__name__)
        self._initialize_consumer()
    
    def _initialize_consumer(self):
        """Initialize the Kafka consumer with proper configuration"""
        try:
            self.consumer = KafkaConsumer(
                group_id=self.group_id,
                bootstrap_servers=['localhost:9092'],
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                auto_commit_interval_ms=1000,
                value_deserializer=lambda x: json.loads(x.decode('utf-8')) if x else None,
                key_deserializer=lambda x: x.decode('utf-8') if x else None
            )
            self.logger.info(f"Consumer initialized successfully with group ID: {self.group_id}")
        except Exception as e:
            self.logger.error(f"Failed to initialize consumer: {e}")
            raise
    
    def subscribe_to_topics(self, topics: List[str]):
        """
        Subscribe to multiple Kafka topics
        
        Args:
            topics (List[str]): List of topic names to subscribe to
        """
        try:
            self.consumer.subscribe(topics)
            self.logger.info(f"Subscribed to topics: {topics}")
        except Exception as e:
            self.logger.error(f"Failed to subscribe to topics {topics}: {e}")
            raise
    
    def consume_messages(self, max_messages: int = None, timeout_ms: int = 5000):
        """
        Consume messages from subscribed topics
        
        Args:
            max_messages (int, optional): Maximum number of messages to consume
            timeout_ms (int): Timeout for message consumption in milliseconds
            
        Yields:
            Dict: Message data with topic, partition, offset, and value
        """
        if not self.consumer:
            raise RuntimeError("Consumer not initialized")
        
        message_count = 0
        try:
            for message in self.consumer:
                message_data = {
                    'topic': message.topic,
                    'partition': message.partition,
                    'offset': message.offset,
                    'key': message.key,
                    'value': message.value,
                    'timestamp': message.timestamp
                }
                
                self.logger.info(f"Received message from {message.topic}:{message.partition}:{message.offset}")
                yield message_data
                
                message_count += 1
                if max_messages and message_count >= max_messages:
                    break
                    
        except Exception as e:
            self.logger.error(f"Error consuming messages: {e}")
            raise
    
    def consume_single_message(self, topic: str, timeout_ms: int = 5000):
        """
        Consume a single message from a specific topic
        
        Args:
            topic (str): Topic name to consume from
            timeout_ms (int): Timeout for message consumption
            
        Returns:
            Dict: Single message data or None if timeout
        """
        try:
            self.consumer.subscribe([topic])
            message = next(self.consumer, None)
            if message:
                return {
                    'topic': message.topic,
                    'partition': message.partition,
                    'offset': message.offset,
                    'key': message.key,
                    'value': message.value,
                    'timestamp': message.timestamp
                }
            return None
        except Exception as e:
            self.logger.error(f"Error consuming single message from {topic}: {e}")
            raise
    
    def unsubscribe(self):
        """Unsubscribe from all topics"""
        try:
            self.consumer.unsubscribe()
            self.logger.info("Unsubscribed from all topics")
        except Exception as e:
            self.logger.error(f"Failed to unsubscribe: {e}")
    
    def close(self):
        """Close the consumer connection"""
        try:
            if self.consumer:
                self.consumer.close()
                self.logger.info("Consumer closed successfully")
        except Exception as e:
            self.logger.error(f"Error closing consumer: {e}")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
    
