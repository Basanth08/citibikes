import sys
import os
import logging
import time
from typing import Dict, Any, List, Optional
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.http_service import HttpService
from kafka_producer.producer import Producer
from constants.topics import BIKES_STATION_INFORMATION_TOPIC, BIKES_STATION_STATUS_TOPIC

class Bikes:
    def __init__(self, retry_attempts: int = 3, retry_delay: int = 5):
        """
        Initialize Bikes data orchestrator
        
        Args:
            retry_attempts (int): Number of retry attempts for failed operations
            retry_delay (int): Delay between retry attempts in seconds
        """
        self.retry_attempts = retry_attempts
        self.retry_delay = retry_delay
        self.http_service = HttpService()
        self.producer = Producer()
        self.logger = logging.getLogger(__name__)
        
        self.logger.info("Bikes orchestrator initialized successfully")
    
    def _validate_station_data(self, station_data: Dict[str, Any]) -> bool:
        """
        Validate station data structure
        
        Args:
            station_data (Dict[str, Any]): Station data to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        required_fields = ['station_id', 'name', 'lat', 'lon']
        
        for field in required_fields:
            if field not in station_data:
                self.logger.warning(f"Missing required field '{field}' in station data")
                return False
        
        # Validate coordinates
        try:
            lat = float(station_data.get('lat', 0))
            lon = float(station_data.get('lon', 0))
            
            if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                self.logger.warning(f"Invalid coordinates: lat={lat}, lon={lon}")
                return False
                
        except (ValueError, TypeError):
            self.logger.warning("Invalid coordinate values in station data")
            return False
        
        return True
    
    def _validate_status_data(self, status_data: Dict[str, Any]) -> bool:
        """
        Validate station status data structure
        
        Args:
            status_data (Dict[str, Any]): Status data to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        required_fields = ['station_id', 'num_bikes_available', 'num_docks_available']
        
        for field in required_fields:
            if field not in status_data:
                self.logger.warning(f"Missing required field '{field}' in status data")
                return False
        
        # Validate numeric values
        try:
            bikes_available = int(status_data.get('num_bikes_available', 0))
            docks_available = int(status_data.get('num_docks_available', 0))
            
            if bikes_available < 0 or docks_available < 0:
                self.logger.warning(f"Invalid availability values: bikes={bikes_available}, docks={docks_available}")
                return False
                
        except (ValueError, TypeError):
            self.logger.warning("Invalid availability values in status data")
            return False
        
        return True
    
    def get_bikes_station_information(self, url: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Fetch and stream station information data
        
        Args:
            url (str): API endpoint URL
            params (Dict[str, Any], optional): Query parameters
            
        Returns:
            List[Dict[str, Any]]: List of valid station information records
        """
        if params is None:
            params = {}
        
        for attempt in range(self.retry_attempts + 1):
            try:
                self.logger.info(f"Fetching station information from {url} (attempt {attempt + 1})")
                
                response = self.http_service.get(url, params)
                data = response.json()
                
                if 'data' not in data or 'stations' not in data['data']:
                    raise ValueError("Invalid response structure from API")
                
                stations = data['data']['stations']
                self.logger.info(f"Retrieved {len(stations)} station records")
                
                valid_stations = []
                for station in stations:
                    if self._validate_station_data(station):
                        # Add timestamp for tracking
                        station['timestamp'] = int(time.time())
                        station['data_type'] = 'station_information'
                        
                        self.logger.debug(f"Processing station: {station.get('name', 'Unknown')} (ID: {station.get('station_id', 'Unknown')})")
                        
                        # Send to Kafka topic
                        try:
                            self.producer.data_producer(BIKES_STATION_INFORMATION_TOPIC, station)
                            valid_stations.append(station)
                        except Exception as e:
                            self.logger.error(f"Failed to send station {station.get('station_id', 'Unknown')} to Kafka: {e}")
                    else:
                        self.logger.warning(f"Skipping invalid station data: {station.get('station_id', 'Unknown')}")
                
                self.logger.info(f"Successfully processed {len(valid_stations)} valid station records")
                return valid_stations
                
            except Exception as e:
                if attempt < self.retry_attempts:
                    self.logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                    continue
                else:
                    self.logger.error(f"Failed to fetch station information after {self.retry_attempts + 1} attempts: {e}")
                    raise
        
        return []
    
    def get_bikes_station_status(self, url: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Fetch and stream station status data
        
        Args:
            url (str): API endpoint URL
            params (Dict[str, Any], optional): Query parameters
            
        Returns:
            List[Dict[str, Any]]: List of valid station status records
        """
        if params is None:
            params = {}
        
        for attempt in range(self.retry_attempts + 1):
            try:
                self.logger.info(f"Fetching station status from {url} (attempt {attempt + 1})")
                
                response = self.http_service.get(url, params)
                data = response.json()
                
                if 'data' not in data or 'stations' not in data['data']:
                    raise ValueError("Invalid response structure from API")
                
                stations = data['data']['stations']
                self.logger.info(f"Retrieved {len(stations)} status records")
                
                valid_statuses = []
                for status in stations:
                    if self._validate_status_data(status):
                        # Add timestamp for tracking
                        status['timestamp'] = int(time.time())
                        status['data_type'] = 'station_status'
                        
                        self.logger.debug(f"Processing status for station ID: {status.get('station_id', 'Unknown')}")
                        
                        # Send to Kafka topic
                        try:
                            self.producer.data_producer(BIKES_STATION_STATUS_TOPIC, status)
                            valid_statuses.append(status)
                        except Exception as e:
                            self.logger.error(f"Failed to send status for station {status.get('station_id', 'Unknown')} to Kafka: {e}")
                    else:
                        self.logger.warning(f"Skipping invalid status data for station: {status.get('station_id', 'Unknown')}")
                
                self.logger.info(f"Successfully processed {len(valid_statuses)} valid status records")
                return valid_statuses
                
            except Exception as e:
                if attempt < self.retry_attempts:
                    self.logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                    continue
                else:
                    self.logger.error(f"Failed to fetch station status after {self.retry_attempts + 1} attempts: {e}")
                    raise
        
        return []
    
    def get_all_bikes_data(self, info_url: str, status_url: str, params: Dict[str, Any] = None) -> Dict[str, List[Dict[str, Any]]]:
        """
        Fetch both station information and status data
        
        Args:
            info_url (str): Station information API endpoint
            status_url (str): Station status API endpoint
            params (Dict[str, Any], optional): Query parameters
            
        Returns:
            Dict[str, List[Dict[str, Any]]]: Dictionary containing both data types
        """
        self.logger.info("Starting comprehensive data collection")
        
        try:
            # Fetch station information
            station_info = self.get_bikes_station_information(info_url, params)
            
            # Fetch station status
            station_status = self.get_bikes_station_status(status_url, params)
            
            result = {
                'station_information': station_info,
                'station_status': station_status,
                'total_records': len(station_info) + len(station_status),
                'timestamp': int(time.time())
            }
            
            self.logger.info(f"Comprehensive data collection completed. Total records: {result['total_records']}")
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to collect comprehensive data: {e}")
            raise
    
    def close(self):
        """Clean up resources"""
        try:
            if hasattr(self, 'producer'):
                self.producer.close()
            if hasattr(self, 'http_service'):
                self.http_service.close()
            self.logger.info("Bikes orchestrator resources cleaned up")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()