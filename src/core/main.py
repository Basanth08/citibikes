#!/usr/bin/env python3
"""
Main execution script for Citi Bikes Real-Time Streaming Project
"""

import argparse
import logging
import time
import signal
import sys
from src.core.bikes_module.bikes import Bikes
from src.utils.constants.routes import BIKES_STATION_INFORMATION, BIKES_STATION_STATUS

# Global variable for graceful shutdown
running = True

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    global running
    logging.info(f"Received signal {signum}. Shutting down gracefully...")
    running = False

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
            logging.FileHandler('citibikes_pipeline.log')
        ]
    )
    
    return logging.getLogger(__name__)

def run_single_execution(bikes: Bikes, logger: logging.Logger) -> bool:
    """Run a single execution of the data pipeline"""
    try:
        logger.info("Starting Citi Bikes Real-Time Streaming Pipeline")
        
        # Fetch and stream station information
        logger.info("Fetching station information...")
        station_info = bikes.get_bikes_station_information(BIKES_STATION_INFORMATION)
        logger.info(f"Station information processed: {len(station_info)} records")
        
        # Fetch and stream station status
        logger.info("Fetching station status...")
        station_status = bikes.get_bikes_station_status(BIKES_STATION_STATUS)
        logger.info(f"Station status processed: {len(station_status)} records")
        
        total_records = len(station_info) + len(station_status)
        logger.info(f"Data pipeline execution completed successfully! Total records: {total_records}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error in main pipeline: {e}")
        return False

def run_continuous_streaming(bikes: Bikes, logger: logging.Logger, interval: int = 60) -> None:
    """Run continuous streaming with specified interval"""
    logger.info(f"Starting continuous streaming with {interval} second intervals")
    logger.info("Press Ctrl+C to stop streaming")
    
    execution_count = 0
    start_time = time.time()
    
    try:
        while running:
            execution_count += 1
            logger.info(f"Execution #{execution_count} starting at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            success = run_single_execution(bikes, logger)
            
            if success:
                logger.info(f"Execution #{execution_count} completed successfully")
            else:
                logger.error(f"Execution #{execution_count} failed")
            
            # Calculate next execution time
            elapsed = time.time() - start_time
            next_execution = interval - (elapsed % interval)
            
            if running:  # Check again in case signal was received
                logger.info(f"Next execution in {next_execution:.1f} seconds...")
                time.sleep(next_execution)
            
    except KeyboardInterrupt:
        logger.info("Continuous streaming interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error in continuous streaming: {e}")
        raise

def main():
    """Main function to run the Citi Bikes data pipeline"""
    parser = argparse.ArgumentParser(description="Citi Bikes Real-Time Streaming Pipeline")
    parser.add_argument(
        "--mode", 
        choices=["single", "continuous"], 
        default="single",
        help="Execution mode: single run or continuous streaming"
    )
    parser.add_argument(
        "--interval", 
        type=int, 
        default=60,
        help="Interval between executions in seconds (for continuous mode)"
    )
    parser.add_argument(
        "--log-level", 
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Logging level"
    )
    
    args = parser.parse_args()
    
    # Set up logging
    logger = setup_logging(args.log_level)
    
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    bikes = None
    try:
        # Initialize the bikes orchestrator
        bikes = Bikes()
        logger.info("Bikes orchestrator initialized successfully")
        
        if args.mode == "single":
            # Single execution mode
            success = run_single_execution(bikes, logger)
            return 0 if success else 1
        else:
            # Continuous streaming mode
            run_continuous_streaming(bikes, logger, args.interval)
            return 0
            
    except Exception as e:
        logger.error(f"Fatal error in main pipeline: {e}")
        return 1
    finally:
        # Cleanup
        if bikes:
            bikes.close()
            logger.info("Bikes orchestrator resources cleaned up")
        
        logger.info("Pipeline shutdown complete")

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 