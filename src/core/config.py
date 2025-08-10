#!/usr/bin/env python3
"""
Configuration file for Citi Bikes Real-Time Streaming Project
"""

import os
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class KafkaConfig:
    """Kafka configuration settings"""
    bootstrap_servers: str = "localhost:9092"
    topic_prefix: str = "bikes"
    producer_acks: str = "all"
    producer_retries: int = 3
    consumer_group_id: str = "bikes-consumer-group"
    consumer_auto_offset_reset: str = "earliest"
    consumer_enable_auto_commit: bool = True
    consumer_auto_commit_interval_ms: int = 1000

@dataclass
class APIConfig:
    """API configuration settings"""
    base_url: str = "https://gbfs.citibikenyc.com/gbfs/en"
    timeout: int = 30
    max_retries: int = 3
    retry_delay: int = 5
    user_agent: str = "CitiBikes-DataPipeline/1.0"

@dataclass
class LoggingConfig:
    """Logging configuration settings"""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: str = "citibikes_pipeline.log"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5

@dataclass
class PipelineConfig:
    """Pipeline configuration settings"""
    execution_interval: int = 60  # seconds
    max_execution_time: int = 300  # seconds
    enable_data_validation: bool = True
    enable_retry_logic: bool = True
    batch_size: int = 100

class Config:
    """Main configuration class"""
    
    def __init__(self):
        self.kafka = KafkaConfig()
        self.api = APIConfig()
        self.logging = LoggingConfig()
        self.pipeline = PipelineConfig()
        self._load_environment_variables()
    
    def _load_environment_variables(self):
        """Load configuration from environment variables"""
        # Kafka settings
        if os.getenv("KAFKA_BOOTSTRAP_SERVERS"):
            self.kafka.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
        
        if os.getenv("KAFKA_CONSUMER_GROUP_ID"):
            self.kafka.consumer_group_id = os.getenv("KAFKA_CONSUMER_GROUP_ID")
        
        # API settings
        if os.getenv("API_TIMEOUT"):
            self.api.timeout = int(os.getenv("API_TIMEOUT"))
        
        if os.getenv("API_MAX_RETRIES"):
            self.api.max_retries = int(os.getenv("API_MAX_RETRIES"))
        
        # Logging settings
        if os.getenv("LOG_LEVEL"):
            self.logging.level = os.getenv("LOG_LEVEL")
        
        # Pipeline settings
        if os.getenv("PIPELINE_INTERVAL"):
            self.pipeline.execution_interval = int(os.getenv("PIPELINE_INTERVAL"))
    
    def get_kafka_config(self) -> Dict[str, Any]:
        """Get Kafka configuration as dictionary"""
        return {
            "bootstrap_servers": [self.kafka.bootstrap_servers],
            "acks": self.kafka.producer_acks,
            "retries": self.kafka.producer_retries,
            "group_id": self.kafka.consumer_group_id,
            "auto_offset_reset": self.kafka.consumer_auto_offset_reset,
            "enable_auto_commit": self.kafka.consumer_enable_auto_commit,
            "auto_commit_interval_ms": self.kafka.consumer_auto_commit_interval_ms
        }
    
    def get_api_config(self) -> Dict[str, Any]:
        """Get API configuration as dictionary"""
        return {
            "timeout": self.api.timeout,
            "max_retries": self.api.max_retries,
            "retry_delay": self.api.retry_delay,
            "user_agent": self.api.user_agent
        }
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration as dictionary"""
        return {
            "level": self.logging.level,
            "format": self.logging.format,
            "file_path": self.logging.file_path,
            "max_file_size": self.logging.max_file_size,
            "backup_count": self.logging.backup_count
        }
    
    def get_pipeline_config(self) -> Dict[str, Any]:
        """Get pipeline configuration as dictionary"""
        return {
            "execution_interval": self.pipeline.execution_interval,
            "max_execution_time": self.pipeline.max_execution_time,
            "enable_data_validation": self.pipeline.enable_data_validation,
            "enable_retry_logic": self.pipeline.enable_retry_logic,
            "batch_size": self.pipeline.batch_size
        }
    
    def validate(self) -> bool:
        """Validate configuration settings"""
        try:
            # Validate Kafka settings
            if not self.kafka.bootstrap_servers:
                raise ValueError("Kafka bootstrap servers cannot be empty")
            
            # Validate API settings
            if self.api.timeout <= 0:
                raise ValueError("API timeout must be positive")
            if self.api.max_retries < 0:
                raise ValueError("API max retries cannot be negative")
            
            # Validate pipeline settings
            if self.pipeline.execution_interval <= 0:
                raise ValueError("Pipeline execution interval must be positive")
            
            return True
            
        except Exception as e:
            print(f"Configuration validation failed: {e}")
            return False

# Global configuration instance
config = Config()

# Validate configuration on import
if not config.validate():
    raise RuntimeError("Invalid configuration detected") 