#!/bin/bash
# Health Check Script for Citibikes Data Pipeline
# This script performs comprehensive health checks on all components
# of the data pipeline to ensure everything is running correctly.

set -e

echo "🔍 Performing comprehensive health check..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
    fi
}

# Check 1: Docker services
echo "🐳 Checking Docker services..."
docker-compose -f config/docker-compose.yaml ps | grep -q "Up"
print_status $? "Docker services are running"

# Check 2: Kafka connectivity
echo "📡 Checking Kafka connectivity..."
nc -z localhost 9092 2>/dev/null
print_status $? "Kafka is accessible on port 9092"

# Check 3: Zookeeper connectivity
echo "🦒 Checking Zookeeper connectivity..."
nc -z localhost 2181 2>/dev/null
print_status $? "Zookeeper is accessible on port 2181"

# Check 4: Log files exist
echo "📝 Checking log files..."
if [ -f "logs/citibikes_pipeline.log" ] && [ -f "logs/citibikes_consumer.log" ]; then
    print_status 0 "Log files exist and are accessible"
else
    print_status 1 "Log files missing or inaccessible"
fi

# Check 5: Python environment
echo "🐍 Checking Python environment..."
python3 --version >/dev/null 2>&1
print_status $? "Python 3 is available"

# Check 6: Required packages
echo "📦 Checking required packages..."
python3 -c "import kafka, structlog, requests" >/dev/null 2>&1
print_status $? "Required Python packages are installed"

# Check 7: AWS CLI (if configured)
echo "☁️ Checking AWS CLI..."
if command -v aws &> /dev/null; then
    if aws sts get-caller-identity &> /dev/null; then
        print_status 0 "AWS CLI is configured and working"
    else
        print_status 1 "AWS CLI is installed but not configured"
    fi
else
    echo -e "${YELLOW}⚠️  AWS CLI not installed (optional for local development)${NC}"
fi

# Check 8: Disk space
echo "💾 Checking disk space..."
df -h . | awk 'NR==2 {if ($4 ~ /[0-9]+G/ && int($4) > 1) exit 0; else exit 1}'
print_status $? "Sufficient disk space available (>1GB)"

# Check 9: Memory usage
echo "🧠 Checking memory usage..."
free -m | awk 'NR==2 {if ($7 > 512) exit 0; else exit 1}'
print_status $? "Sufficient memory available (>512MB)"

# Check 10: Network connectivity
echo "🌐 Checking network connectivity..."
ping -c 1 8.8.8.8 >/dev/null 2>&1
print_status $? "Internet connectivity is available"

echo ""
echo "🏥 Health check complete!"
echo ""

# Summary
echo "📊 Health Check Summary:"
echo "========================"
echo "Docker Services: $(docker-compose -f config/docker-compose.yaml ps --format 'table {{.Name}}\t{{.Status}}' | grep -v 'Name')"
echo "Kafka Status: $(nc -z localhost 9092 2>/dev/null && echo 'Running' || echo 'Not accessible')"
echo "Log Files: $(ls -la logs/*.log 2>/dev/null | wc -l) files found"
echo "Python Version: $(python3 --version 2>/dev/null || echo 'Not available')"
echo ""

# Recommendations
echo "💡 Recommendations:"
if ! nc -z localhost 9092 2>/dev/null; then
    echo "  - Start Docker services: cd config && docker-compose up -d"
fi
if [ ! -f "logs/citibikes_pipeline.log" ]; then
    echo "  - Run the producer to generate logs: python src/core/main.py"
fi
if ! python3 -c "import kafka" >/dev/null 2>&1; then
    echo "  - Install dependencies: pip install -r config/requirements.txt"
fi 