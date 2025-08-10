#!/usr/bin/env python3
"""
Main runner script for Citi Bikes Real-Time Streaming Project
This script runs the entire pipeline from the project root directory.
"""

import sys
import os
import logging
import time
import signal
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.bikes_module.bikes import Bikes
from utils.constants.routes import BIKES_STATION_INFORMATION, BIKES_STATION_STATUS

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
            logging.FileHandler('logs/citibikes_pipeline.log')
        ]
    )
    
    return logging.getLogger(__name__)

def run_single_execution(bikes: Bikes, logger: logging.Logger) -> bool:
    """Run a single execution of the data pipeline"""
    try:
        logger.info("Starting Citi Bikes Real-Time Streaming Pipeline")
        
        # Fetch and stream station information
        logger.info("Fetching station information...")
        bikes.get_bikes_station_information(BIKES_STATION_INFORMATION)
        logger.info("Station information processed successfully")
        
        # Fetch and stream station status
        logger.info("Fetching station status...")
        bikes.get_bikes_station_status(BIKES_STATION_STATUS)
        logger.info("Station status processed successfully")
        
        logger.info("Data pipeline execution completed successfully!")
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
    """Main entry point"""
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description="Citi Bikes Real-Time Streaming Pipeline")
    parser.add_argument("--mode", choices=["single", "continuous"], default="single",
                       help="Execution mode: single run or continuous streaming")
    parser.add_argument("--interval", type=int, default=60,
                       help="Interval between executions in seconds (for continuous mode)")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], default="INFO",
                       help="Logging level")
    
    args = parser.parse_args()
    
    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)
    
    # Set up logging
    logger = setup_logging(args.log_level)
    
    try:
        logger.info("Initializing Citi Bikes Pipeline...")
        
        # Initialize bikes module
        bikes = Bikes()
        logger.info("Bikes module initialized successfully")
        
        if args.mode == "single":
            logger.info("Running single execution mode")
            success = run_single_execution(bikes, logger)
            if success:
                logger.info("Pipeline completed successfully!")
                return 0
            else:
                logger.error("Pipeline failed!")
                return 1
        else:
            logger.info("Running continuous streaming mode")
            run_continuous_streaming(bikes, logger, args.interval)
            return 0
            
    except Exception as e:
        logger.error(f"Fatal error in pipeline: {e}")
        return 1
    finally:
        logger.info("Pipeline shutdown complete")

if __name__ == "__main__":
    sys.exit(main()) 