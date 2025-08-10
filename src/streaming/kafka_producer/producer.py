import json
import logging
from kafka import KafkaProducer
from kafka.errors import KafkaError
from typing import Dict, Any, Optional

class Producer:
    def __init__(self, bootstrap_servers: str = 'localhost:9092'):
        """
        Initialize Kafka Producer
        
        Args:
            bootstrap_servers (str): Kafka broker addresses
        """
        self.bootstrap_servers = bootstrap_servers
        self.producer = None
        self.logger = logging.getLogger(__name__)
        self._initialize_producer()
    
    def _initialize_producer(self):
        """Initialize the Kafka producer with proper configuration"""
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=[self.bootstrap_servers],
                value_serializer=lambda x: json.dumps(x).encode('utf-8') if x else None,
                key_serializer=lambda x: x.encode('utf-8') if x else None,
                acks='all',  # Wait for all replicas to acknowledge
                retries=3,   # Retry failed sends
                max_in_flight_requests_per_connection=1
                # Note: enable_idempotence removed for compatibility
            )
            self.logger.info(f"Producer initialized successfully with bootstrap servers: {self.bootstrap_servers}")
        except Exception as e:
            self.logger.error(f"Failed to initialize producer: {e}")
            raise
    
    def data_producer(self, topic: str, message: Dict[str, Any], key: Optional[str] = None):
        """
        Send a message to a Kafka topic
        
        Args:
            topic (str): Target topic name
            message (Dict[str, Any]): Message data to send
            key (Optional[str]): Message key for partitioning
        """
        if not self.producer:
            raise RuntimeError("Producer not initialized")
        
        try:
            # Send message with callback for success/failure tracking
            future = self.producer.send(
                topic=topic,
                value=message,
                key=key
            )
            
            # Wait for the send to complete and check for errors
            record_metadata = future.get(timeout=10)
            
            self.logger.info(
                f"Message sent successfully to {topic}:{record_metadata.partition}:{record_metadata.offset}"
            )
            
            return record_metadata
            
        except KafkaError as e:
            self.logger.error(f"Failed to send message to topic {topic}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error sending message to topic {topic}: {e}")
            raise
    
    def send_batch(self, topic: str, messages: list, key: Optional[str] = None):
        """
        Send multiple messages to a Kafka topic
        
        Args:
            topic (str): Target topic name
            messages (list): List of messages to send
            key (Optional[str]): Message key for partitioning
        """
        if not self.producer:
            raise RuntimeError("Producer not initialized")
        
        try:
            futures = []
            for message in messages:
                future = self.producer.send(topic=topic, value=message, key=key)
                futures.append(future)
            
            # Wait for all messages to be sent
            for future in futures:
                record_metadata = future.get(timeout=10)
                self.logger.info(
                    f"Batch message sent to {topic}:{record_metadata.partition}:{record_metadata.offset}"
                )
            
            self.logger.info(f"Successfully sent {len(messages)} messages to topic {topic}")
            
        except Exception as e:
            self.logger.error(f"Failed to send batch messages to topic {topic}: {e}")
            raise
    
    def flush(self):
        """Ensure all pending messages are sent"""
        try:
            self.producer.flush()
            self.logger.info("Producer flushed successfully")
        except Exception as e:
            self.logger.error(f"Failed to flush producer: {e}")
            raise
    
    def close(self):
        """Close the producer connection"""
        try:
            if self.producer:
                self.producer.close()
                self.logger.info("Producer closed successfully")
        except Exception as e:
            self.logger.error(f"Error closing producer: {e}")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
        
        

