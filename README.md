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

## Project Status
🚧 **In Progress** - I'm currently setting up the foundation for this streaming project.

## Infrastructure Setup
I'm setting up the streaming infrastructure using Docker Compose to run:
- **Apache Kafka**: As the message broker for handling real-time data streams
- **Apache Zookeeper**: For managing Kafka cluster coordination
- **Kafka Connect**: For data pipeline connectors

### Current Setup Status
✅ **Infrastructure Ready!** I discovered that Kafka infrastructure is already running from a previous setup:

- **Zookeeper**: Running on port 2181
- **Kafka**: Running on port 9092  
- **Kafka Connect**: Running on port 8083
- **Kafka UI**: Available on port 8080 for monitoring

Since the infrastructure is already operational, I can proceed directly to building the data pipeline components.

---
*This README will be updated as I continue working on different aspects of the project.*