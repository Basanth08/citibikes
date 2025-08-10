#!/usr/bin/env python3
"""
Main execution script for Citi Bikes Real-Time Streaming Project
"""

from bikes_module.bikes import Bikes
from constants.routes import BIKES_STATION_INFORMATION, BIKES_STATION_STATUS
import time
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main function to run the Citi Bikes data pipeline"""
    try:
        logger.info("Starting Citi Bikes Real-Time Streaming Pipeline")
        
        # Initialize the bikes orchestrator
        bikes = Bikes()
        logger.info("Bikes orchestrator initialized successfully")
        
        # Fetch and stream station information
        logger.info("Fetching station information...")
        bikes.get_bikes_station_information(BIKES_STATION_INFORMATION)
        
        # Fetch and stream station status
        logger.info("Fetching station status...")
        bikes.get_bikes_station_status(BIKES_STATION_STATUS)
        
        logger.info("Data pipeline execution completed successfully!")
        
    except Exception as e:
        logger.error(f"Error in main pipeline: {e}")
        raise

if __name__ == "__main__":
    main() 