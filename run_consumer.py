#!/usr/bin/env python3
"""
Consumer runner script for Citi Bikes Real-Time Streaming Project
This script runs the consumer from the project root directory.
"""

import sys
import logging
import time
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from streaming.kafka_consumer.consumer import Consumer
from utils.constants.topics import BIKES_STATION_INFORMATION_TOPIC, BIKES_STATION_STATUS_TOPIC

def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """Set up logging configuration"""
    log_levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    
    logging.basicConfig(
        level=log_levels.get(log_level.upper(), logging.INFO),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('logs/citibikes_consumer.log')
        ]
    )
    
    return logging.getLogger(__name__)

def test_consumer():
    """Test the Kafka consumer functionality"""
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starting Citi Bikes Consumer Test")
        
        # Initialize consumer
        consumer = Consumer("bikes-consumer-test-group")
        logger.info("Consumer initialized successfully")
        
        # Subscribe to both topics
        topics = [BIKES_STATION_INFORMATION_TOPIC, BIKES_STATION_STATUS_TOPIC]
        consumer.subscribe_to_topics(topics)
        logger.info(f"Subscribed to topics: {topics}")
        
        # Consume messages for a limited time
        logger.info("Starting message consumption (will consume for 30 seconds)...")
        start_time = time.time()
        timeout = 30  # seconds
        
        message_count = 0
        for message in consumer.consume_messages():
            message_count += 1
            logger.info(f"Message {message_count} received:")
            logger.info(f"   Topic: {message['topic']}")
            logger.info(f"   Partition: {message['partition']}")
            logger.info(f"   Offset: {message['offset']}")
            logger.info(f"   Data: {message['value']}")
            logger.info("-" * 50)
            
            # Check if timeout reached
            if time.time() - start_time > timeout:
                logger.info(f"Timeout reached ({timeout} seconds). Stopping consumption.")
                break
        
        logger.info(f"Consumer test completed. Received {message_count} messages.")
        
    except KeyboardInterrupt:
        logger.info("Consumer test interrupted by user")
    except Exception as e:
        logger.error(f"Error in consumer test: {e}")
        raise
    finally:
        if 'consumer' in locals():
            consumer.close()
            logger.info("Consumer closed")

def consume_single_message():
    """Test consuming a single message from each topic"""
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Testing single message consumption")
        
        with Consumer("bikes-single-test-group") as consumer:
            # Test station information topic
            logger.info(f"Testing {BIKES_STATION_INFORMATION_TOPIC}")
            message = consumer.consume_single_message(BIKES_STATION_INFORMATION_TOPIC)
            if message:
                logger.info(f"Received message from {BIKES_STATION_INFORMATION_TOPIC}")
                logger.info(f"   Data: {message['value']}")
            else:
                logger.warning(f"No message available in {BIKES_STATION_INFORMATION_TOPIC}")
            
            # Test station status topic
            logger.info(f"Testing {BIKES_STATION_STATUS_TOPIC}")
            message = consumer.consume_single_message(BIKES_STATION_STATUS_TOPIC)
            if message:
                logger.info(f"Received message from {BIKES_STATION_STATUS_TOPIC}")
                logger.info(f"   Data: {message['value']}")
            else:
                logger.warning(f"No message available in {BIKES_STATION_STATUS_TOPIC}")
                
    except Exception as e:
        logger.error(f"Error in single message test: {e}")
        raise

def main():
    """Main entry point"""
    import argparse
    parser = argparse.ArgumentParser(description="Citi Bikes Consumer")
    parser.add_argument("--mode", choices=["test", "single"], default="test",
                       help="Consumer mode: test (continuous) or single message")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], default="INFO",
                       help="Logging level")
    
    args = parser.parse_args()
    
    # Ensure logs directory exists
    import os
    os.makedirs("logs", exist_ok=True)
    
    # Set up logging
    logger = setup_logging(args.log_level)
    
    try:
        logger.info("Starting Citi Bikes Consumer")
        
        if args.mode == "test":
            test_consumer()
        else:
            consume_single_message()
            
        logger.info("Consumer completed successfully!")
        return 0
        
    except Exception as e:
        logger.error(f"Fatal error in consumer: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 