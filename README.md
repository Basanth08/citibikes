# Citi Bikes Real-Time Streaming Project

## Project Overview
I'm building a real-time streaming project focused on Citi Bike data. This project will involve processing and analyzing live data from the Citi Bike system to provide real-time insights and analytics.

## What I'm Building
I'm creating a streaming data pipeline that will:
- Collect real-time data from Citi Bike stations
- Process and transform the streaming data
- Provide live analytics and insights
- Monitor bike availability and station status in real-time

## Data Sources
I'm using the official Citi Bike GBFS (General Bikeshare Feed Specification) API endpoints to collect real-time data:

- **Station Information**: `https://gbfs.citibikenyc.com/gbfs/en/station_information.json`
  - Provides static data about bike stations (location, capacity, etc.)
- **Station Status**: `https://gbfs.citibikenyc.com/gbfs/en/station_status.json`
  - Provides real-time status updates (available bikes, docks, etc.)

These endpoints will feed data into my streaming pipeline to monitor bike availability and station status across New York City in real-time.

## Kafka Topics
I've defined two main Kafka topics to organize the streaming data:

- **`bikes-station-information`**: For storing static station data (locations, names, capacities)
- **`bikes-station-status`**: For real-time status updates (available bikes, dock counts, station status)

This topic structure allows me to separate static reference data from dynamic status updates, making the pipeline more efficient and easier to manage.

## HTTP Methods for API Integration
![HTTP Request Methods](images/HTTPMethods.png)

Understanding HTTP methods is **crucial** for building my producer and consumer scripts:

- **GET**: I'll use this extensively to fetch data from the Citi Bike API endpoints
- **POST**: May be needed for sending data to Kafka Connect or other services
- **PUT/PATCH**: For updating configuration or status information
- **DELETE**: For cleanup operations or removing old data

Since my producer will be making HTTP requests to the Citi Bike API to fetch real-time data, and my consumer will need to interact with various services, mastering these HTTP methods is essential for building robust, reliable streaming scripts.

## Architecture
I've designed a real-time streaming pipeline with the following components:

![Real-Time Streaming Pipeline Architecture](images/architecture.png)

```
API → Producer → Broker → Consumer → AWS S3 Data Load
```

**Data Flow:**
1. **API**: The starting point where Citi Bike data originates
2. **Producer**: Handles the incoming data and prepares it for streaming
3. **Broker**: Acts as the message queue/buffer for the streaming data
4. **Consumer**: Processes the streaming data in real-time
5. **AWS S3**: Final destination where the processed data is stored for analysis

This architecture follows a standard streaming pattern that will allow me to handle real-time Citi Bike data efficiently while maintaining data persistence in the cloud.

## Infrastructure Setup
I've set up a complete Kafka infrastructure using Docker Compose:

- **Apache Kafka**: Message broker for streaming data
- **Apache Zookeeper**: Cluster coordination and metadata management
- **Kafka Connect**: Data pipeline connectors
- **Kafka UI**: Web interface for monitoring topics and clusters

The infrastructure is currently running and ready for data streaming operations.

## Project Structure
I've organized the project into a clean, modular structure:

```
citibikes/
├── constants/           # Configuration constants
│   ├── routes.py       # API endpoints
│   └── topics.py       # Kafka topic names
├── services/           # Service layer
│   └── http_service.py # HTTP client service
├── bikes_module/       # Core business logic (renamed from 'bikes')
│   └── bikes.py        # Main bikes data orchestrator
├── kafka_producer/     # Kafka integration
│   └── producer.py     # Kafka producer implementation
├── images/             # Project documentation images
├── docker-compose.yaml # Infrastructure setup
├── main.py             # Main execution script
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## Implementation Status
✅ **Completed Components:**
- HTTP service with all HTTP methods (GET, POST, PUT, DELETE)
- Kafka producer setup with JSON serialization
- Main bikes orchestrator class (`Bikes`)
- Docker infrastructure (Kafka, Zookeeper, Schema Registry, Connect)
- Project structure and constants
- Main execution script (`main.py`)
- Requirements.txt with dependencies
- **Producer Testing**: Successfully tested and verified working

✅ **Producer Status: WORKING CORRECTLY**
- Successfully fetches data from Citi Bike GBFS API
- Processes both station information and station status endpoints
- Sends messages to appropriate Kafka topics
- Handles JSON serialization and data transformation
- Includes proper error handling and logging

🔄 **In Progress:**
- Producer-consumer integration
- Data pipeline execution

📋 **Next Steps:**
- Implement consumer for data processing
- Set up continuous data streaming
- Add error handling and retry logic
- Integrate with AWS S3 for data storage
- Set up monitoring and alerting

## Recent Achievements
I've successfully resolved several technical challenges:

1. **Import Resolution**: Fixed Python import conflicts by restructuring the project and using absolute imports
2. **Method Integration**: Connected the producer to the main bikes orchestrator
3. **Data Pipeline Testing**: Successfully executed the complete pipeline from API to Kafka
4. **Infrastructure Setup**: Established a stable Kafka environment for streaming operations

## Data Flow Verification
The current pipeline successfully:
- Fetches real-time data from Citi Bike API endpoints
- Processes JSON responses and extracts station data
- Streams messages to Kafka topics via the producer
- Provides comprehensive logging throughout the process
- Maintains clean separation of concerns between components

---
*This README will be updated as I continue working on different aspects of the project.*