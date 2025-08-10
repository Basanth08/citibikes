#!/usr/bin/env python3
"""
Consumer test script for Citi Bikes Real-Time Streaming Project
"""

import logging
import time
from kafka_consumer.consumer import Consumer
from constants.topics import BIKES_STATION_INFORMATION_TOPIC, BIKES_STATION_STATUS_TOPIC

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_consumer():
    """Test the Kafka consumer functionality"""
    try:
        logger.info("🚴 Starting Citi Bikes Consumer Test")
        
        # Initialize consumer
        consumer = Consumer("bikes-consumer-test-group")
        logger.info("✅ Consumer initialized successfully")
        
        # Subscribe to both topics
        topics = [BIKES_STATION_INFORMATION_TOPIC, BIKES_STATION_STATUS_TOPIC]
        consumer.subscribe_to_topics(topics)
        logger.info(f"📡 Subscribed to topics: {topics}")
        
        # Consume messages for a limited time
        logger.info("🔄 Starting message consumption (will consume for 30 seconds)...")
        start_time = time.time()
        timeout = 30  # seconds
        
        message_count = 0
        for message in consumer.consume_messages():
            message_count += 1
            logger.info(f"📨 Message {message_count} received:")
            logger.info(f"   Topic: {message['topic']}")
            logger.info(f"   Partition: {message['partition']}")
            logger.info(f"   Offset: {message['offset']}")
            logger.info(f"   Data: {message['value']}")
            logger.info("-" * 50)
            
            # Check if timeout reached
            if time.time() - start_time > timeout:
                logger.info(f"⏰ Timeout reached ({timeout} seconds). Stopping consumption.")
                break
        
        logger.info(f"✅ Consumer test completed. Received {message_count} messages.")
        
    except KeyboardInterrupt:
        logger.info("⏹️ Consumer test interrupted by user")
    except Exception as e:
        logger.error(f"❌ Error in consumer test: {e}")
        raise
    finally:
        if 'consumer' in locals():
            consumer.close()
            logger.info("🔒 Consumer closed")

def consume_single_message():
    """Test consuming a single message from each topic"""
    try:
        logger.info("🔍 Testing single message consumption")
        
        with Consumer("bikes-single-test-group") as consumer:
            # Test station information topic
            logger.info(f"📡 Testing {BIKES_STATION_INFORMATION_TOPIC}")
            message = consumer.consume_single_message(BIKES_STATION_INFORMATION_TOPIC)
            if message:
                logger.info(f"✅ Received message from {BIKES_STATION_INFORMATION_TOPIC}")
                logger.info(f"   Data: {message['value']}")
            else:
                logger.warning(f"⚠️ No message available in {BIKES_STATION_INFORMATION_TOPIC}")
            
            # Test station status topic
            logger.info(f"📡 Testing {BIKES_STATION_STATUS_TOPIC}")
            message = consumer.consume_single_message(BIKES_STATION_STATUS_TOPIC)
            if message:
                logger.info(f"✅ Received message from {BIKES_STATION_STATUS_TOPIC}")
                logger.info(f"   Data: {message['value']}")
            else:
                logger.warning(f"⚠️ No message available in {BIKES_STATION_STATUS_TOPIC}")
                
    except Exception as e:
        logger.error(f"❌ Error in single message test: {e}")
        raise

if __name__ == "__main__":
    logger.info("🚀 Starting Citi Bikes Consumer Tests")
    
    # Test 1: Continuous consumption
    test_consumer()
    
    # Test 2: Single message consumption
    consume_single_message()
    
    logger.info("🎉 All consumer tests completed!")