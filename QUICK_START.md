# 🚀 Quick Start Guide

## ⚡ Get Running in 3 Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up OANDA Credentials
```bash
cp .env.example .env
# Edit .env with your OANDA API key and account ID
```

### 3. Launch Everything
```bash
python launch.py
```

## 🌐 Access Your Dashboard

Once running, open your browser and go to:
**http://localhost:8501**

## 📱 What You'll See

- **Live Account Balance** - Real-time updates every minute
- **Trading History** - All BUY/SELL actions with timestamps
- **Balance Charts** - Interactive charts showing performance over time
- **Trade Summary** - Total trades, profit/loss, buy/sell counts

## 🤖 What the Bot Does

- **Automatically trades** EUR/USD and GBP/USD
- **Strategy**: Buy on 0.1% price increase, Sell on 0.1% decrease
- **Safety**: 60-second cooldown between trades
- **Logging**: Records everything to SQLite database

## 🛑 Stop Everything

Press `Ctrl+C` in the terminal where you ran `launch.py`

## 🔧 Customize

Edit `config.py` to change:
- Trading thresholds
- Currency pairs
- Update frequencies
- Risk parameters

## ❓ Need Help?

Run the test script to check your setup:
```bash
python test_setup.py
```

## 📋 Prerequisites

- Python 3.8+
- OANDA demo account
- Internet connection

That's it! Your Forex trading bot is now running with a live dashboard. 🎉