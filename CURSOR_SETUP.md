# 🎯 Cursor Setup Guide

## 🚀 One-Command Startup

In Cursor, simply run this command to start everything:

```bash
./start_cursor.sh
```

This script will:
1. ✅ Create a virtual environment
2. ✅ Install all dependencies
3. ✅ Set up your environment file
4. ✅ Test the setup
5. ✅ Launch the trading bot and dashboard

## 🌐 Access Your Dashboard

Once running, open your browser and go to:
**http://localhost:8501**

## 📱 What You'll See

- **Live Account Balance** - Updates every minute
- **Trading History** - All BUY/SELL actions
- **Interactive Charts** - Balance over time
- **Real-time Updates** - Auto-refreshing data

## 🤖 Bot Features

- **Automated Trading** on EUR/USD and GBP/USD
- **Smart Strategy** based on price momentum
- **Safety Features** with trade cooldowns
- **Complete Logging** to SQLite database

## 🔧 Manual Setup (if needed)

If you prefer to set up manually:

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate it
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up credentials
cp .env.example .env
# Edit .env with your OANDA credentials

# 5. Launch
python launch.py
```

## 📋 Prerequisites

- Python 3.8+
- OANDA demo account
- Internet connection

## 🛑 Stop Everything

Press `Ctrl+C` in the terminal

## ❓ Troubleshooting

**"Permission denied" on start_cursor.sh:**
```bash
chmod +x start_cursor.sh
```

**Virtual environment issues:**
```bash
rm -rf venv
./start_cursor.sh
```

**Test your setup:**
```bash
source venv/bin/activate
python test_setup.py
```

## 🎉 You're Ready!

Your Forex trading bot is now running with a live dashboard accessible at **http://localhost:8501**

The bot will automatically:
- Connect to OANDA
- Start trading based on your strategy
- Log all activity
- Update the dashboard in real-time

Enjoy your automated trading experience! 📈