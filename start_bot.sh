#!/bin/bash

# Forex Trading Bot Startup Script
# This script installs dependencies and starts the trading bot system

echo "🚀 Starting Forex Trading Bot System..."
echo "======================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

echo "✅ Python and pip are available"

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "📝 Please edit .env file with your OANDA credentials:"
        echo "   OANDA_API_KEY=your_api_key_here"
        echo "   OANDA_ACCOUNT_ID=your_account_id_here"
        echo ""
        echo "Press Enter after editing .env file to continue..."
        read
    else
        echo "❌ .env.example not found. Please create .env file manually."
        exit 1
    fi
fi

# Start the system
echo "🚀 Launching trading bot and dashboard..."
python3 launch.py