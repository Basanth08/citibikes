#!/bin/bash
# Metrics Collection Script for Citibikes Data Pipeline
# This script collects and displays key performance metrics
# for monitoring the health and performance of the data pipeline.

set -e

echo "📊 Collecting pipeline metrics..."

# Colors for output
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo -e "${BLUE}🕐 Metrics collected at: $TIMESTAMP${NC}"
echo ""

# 1. System Resources
echo -e "${BLUE}💻 System Resources${NC}"
echo "=================="
echo "CPU Usage: $(top -l 1 | grep "CPU usage" | awk '{print $3}' | sed 's/%//')"
echo "Memory Usage: $(top -l 1 | grep PhysMem | awk '{print $2}')"
echo "Disk Usage: $(df -h . | awk 'NR==2 {print $5}')"
echo ""

# 2. Docker Services Status
echo -e "${BLUE}🐳 Docker Services Status${NC}"
echo "========================"
if command -v docker-compose &> /dev/null; then
    cd config
    docker-compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"
    cd ..
else
    echo "Docker Compose not available"
fi
echo ""

# 3. Kafka Metrics
echo -e "${BLUE}📡 Kafka Metrics${NC}"
echo "================"
if nc -z localhost 9092 2>/dev/null; then
    echo "Kafka Status: Running"
    echo "Port: 9092"
    
    # Check if we can get topic information
    if command -v docker &> /dev/null; then
        echo "Topics:"
        docker exec -it citibikes-kafka-1 kafka-topics --bootstrap-server localhost:9092 --list 2>/dev/null || echo "  Unable to list topics"
    fi
else
    echo "Kafka Status: Not accessible"
fi
echo ""

# 4. Log File Metrics
echo -e "${BLUE}📝 Log File Metrics${NC}"
echo "=================="
if [ -d "logs" ]; then
    echo "Log Directory: logs/"
    echo "Pipeline Log:"
    if [ -f "logs/citibikes_pipeline.log" ]; then
        echo "  - Size: $(ls -lh logs/citibikes_pipeline.log | awk '{print $5}')"
        echo "  - Lines: $(wc -l < logs/citibikes_pipeline.log)"
        echo "  - Last Modified: $(stat -f "%Sm" logs/citibikes_pipeline.log)"
    else
        echo "  - Not found"
    fi
    
    echo "Consumer Log:"
    if [ -f "logs/citibikes_consumer.log" ]; then
        echo "  - Size: $(ls -lh logs/citibikes_consumer.log | awk '{print $5}')"
        echo "  - Lines: $(wc -l < logs/citibikes_consumer.log)"
        echo "  - Last Modified: $(stat -f "%Sm" logs/citibikes_consumer.log)"
    else
        echo "  - Not found"
    fi
else
    echo "Logs directory not found"
fi
echo ""

# 5. Python Environment
echo -e "${BLUE}🐍 Python Environment${NC}"
echo "====================="
if command -v python3 &> /dev/null; then
    echo "Python Version: $(python3 --version)"
    echo "Pip Version: $(pip3 --version 2>/dev/null || echo 'Not available')"
    
    # Check key packages
    echo "Key Packages:"
    python3 -c "import kafka; print('  - kafka-python: OK')" 2>/dev/null || echo "  - kafka-python: Missing"
    python3 -c "import structlog; print('  - structlog: OK')" 2>/dev/null || echo "  - structlog: Missing"
    python3 -c "import requests; print('  - requests: OK')" 2>/dev/null || echo "  - requests: Missing"
    python3 -c "import boto3; print('  - boto3: OK')" 2>/dev/null || echo "  - boto3: Missing"
else
    echo "Python 3 not available"
fi
echo ""

# 6. AWS Integration Status
echo -e "${BLUE}☁️ AWS Integration Status${NC}"
echo "========================"
if command -v aws &> /dev/null; then
    if aws sts get-caller-identity &> /dev/null; then
        echo "AWS CLI: Configured"
        echo "Account ID: $(aws sts get-caller-identity --query Account --output text)"
        echo "Region: $(aws configure get region)"
        
        # Check if config file exists
        if [ -f "config/aws_config.env" ]; then
            echo "Config File: Present"
            echo "S3 Bucket: $(grep S3_BUCKET_NAME config/aws_config.env | cut -d'=' -f2 || echo 'Not set')"
            echo "Glue Database: $(grep GLUE_DATABASE_NAME config/aws_config.env | cut -d'=' -f2 || echo 'Not set')"
        else
            echo "Config File: Missing"
        fi
    else
        echo "AWS CLI: Installed but not configured"
    fi
else
    echo "AWS CLI: Not installed"
fi
echo ""

# 7. Network Connectivity
echo -e "${BLUE}🌐 Network Connectivity${NC}"
echo "======================="
echo "Internet: $(ping -c 1 8.8.8.8 >/dev/null 2>&1 && echo 'Connected' || echo 'Disconnected')"
echo "Localhost: $(ping -c 1 localhost >/dev/null 2>&1 && echo 'Available' || echo 'Unavailable')"
echo ""

# 8. Performance Indicators
echo -e "${BLUE}⚡ Performance Indicators${NC}"
echo "========================="

# Check if logs are being actively written
if [ -f "logs/citibikes_pipeline.log" ]; then
    LOG_SIZE_1=$(stat -f%z logs/citibikes_pipeline.log)
    sleep 2
    LOG_SIZE_2=$(stat -f%z logs/citibikes_pipeline.log)
    
    if [ $LOG_SIZE_2 -gt $LOG_SIZE_1 ]; then
        echo "Pipeline Activity: Active (logs growing)"
    else
        echo "Pipeline Activity: Inactive (logs static)"
    fi
else
    echo "Pipeline Activity: Unknown (no logs)"
fi

# Check Docker resource usage
if command -v docker &> /dev/null; then
    echo "Docker Resources:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}" 2>/dev/null || echo "  Unable to get stats"
fi
echo ""

# 9. Recommendations
echo -e "${BLUE}💡 Recommendations${NC}"
echo "================"

# Check for common issues and provide recommendations
if ! nc -z localhost 9092 2>/dev/null; then
    echo -e "${RED}  - Start Docker services: cd config && docker-compose up -d${NC}"
fi

if [ ! -f "logs/citibikes_pipeline.log" ]; then
    echo -e "${YELLOW}  - Run producer to generate logs: python src/core/main.py${NC}"
fi

if ! python3 -c "import kafka" >/dev/null 2>&1; then
    echo -e "${RED}  - Install dependencies: pip install -r config/requirements.txt${NC}"
fi

if [ ! -f "config/aws_config.env" ] && command -v aws &> /dev/null; then
    echo -e "${YELLOW}  - Configure AWS environment: cp config/aws_config.env.example config/aws_config.env${NC}"
fi

echo ""

# 10. Summary
echo -e "${BLUE}📋 Summary${NC}"
echo "========"
echo "Overall Status: $(nc -z localhost 9092 2>/dev/null && echo 'Healthy' || echo 'Needs Attention')"
echo "Ready for Production: $(nc -z localhost 9092 2>/dev/null && [ -f "logs/citibikes_pipeline.log" ] && echo 'Yes' || echo 'No')"
echo ""

echo -e "${GREEN}✅ Metrics collection complete!${NC}"
echo "Run this script regularly to monitor pipeline health." 