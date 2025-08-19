#!/bin/bash

# Cursor-specific startup script for Forex Trading Bot
# This script handles virtual environment creation and dependency installation

echo "🚀 Starting Forex Trading Bot in Cursor Environment..."
echo "===================================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    
    # Try to create virtual environment
    if command -v python3 &> /dev/null; then
        # Check if venv module is available
        if python3 -c "import venv" 2>/dev/null; then
            python3 -m venv venv
            echo "✅ Virtual environment created"
        else
            echo "⚠️  venv module not available, trying alternative approach..."
            # Try using virtualenv if available
            if command -v virtualenv &> /dev/null; then
                virtualenv venv
                echo "✅ Virtual environment created with virtualenv"
            else
                echo "❌ Neither venv nor virtualenv available"
                echo "💡 Please install python3-venv: sudo apt install python3-venv"
                exit 1
            fi
        fi
    else
        echo "❌ Python3 not found"
        exit 1
    fi
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

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

# Test the setup
echo "🧪 Testing setup..."
python test_setup.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Setup complete! Starting the trading bot..."
    echo ""
    python launch.py
else
    echo ""
    echo "⚠️  Setup test failed. Please fix the issues above."
    echo "💡 You can still try to run the bot manually:"
    echo "   source venv/bin/activate"
    echo "   python launch.py"
fi