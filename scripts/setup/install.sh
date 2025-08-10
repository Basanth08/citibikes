#!/bin/bash
"""
Citibikes Data Pipeline - Installation Script

This script sets up the complete development environment for the
Citibikes real-time data streaming pipeline.
"""

set -e

echo "🚀 Setting up Citibikes Data Pipeline..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.8+ and try again."
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is required but not running."
    echo "Please start Docker Desktop and try again."
    exit 1
fi

# Create virtual environment
echo "📦 Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📚 Installing Python dependencies..."
pip install --upgrade pip
pip install -r config/requirements.txt

# Start infrastructure
echo "🐳 Starting Docker infrastructure..."
cd config
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Verify services
echo "🔍 Verifying services..."
docker-compose ps

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run producer: python src/core/main.py"
echo "3. Run consumer: python src/core/consume.py"
echo "4. Check logs: tail -f logs/citibikes_pipeline.log" 