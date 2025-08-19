# 🤖 Forex Trading Bot with Live Dashboard

A fully automated Forex trading bot that connects to OANDA Demo Account with a real-time Streamlit dashboard for monitoring trades and account performance.

## 🚀 Features

- **Automated Trading**: Monitors EUR/USD and GBP/USD every minute
- **Smart Strategy**: Buys on >0.1% price increase, sells on >0.1% decrease
- **Live Dashboard**: Real-time updates with charts and trade history
- **Database Storage**: SQLite database for all trades and balance history
- **OANDA Integration**: Uses official OANDA API for demo trading
- **Auto-refresh**: Dashboard updates automatically every minute

## 📋 Requirements

- Python 3.8+
- OANDA Demo Account (free)
- Internet connection

## 🛠️ Installation

1. **Clone/Download** this project to your workspace
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up OANDA credentials**:
   - Get free demo account at: https://www.oanda.com/demo-account/
   - Copy `.env.example` to `.env`
   - Edit `.env` with your API key and account ID

## 🚀 Quick Start

### Option 1: Run Everything with One Command
```bash
# Start the trading bot (runs continuously)
python run_bot.py

# In another terminal, start the dashboard
python run_dashboard.py
```

### Option 2: Manual Execution
```bash
# Terminal 1: Start trading bot
python bot.py

# Terminal 2: Start dashboard
streamlit run dashboard.py
```

## 📊 Dashboard Access

Once running, the dashboard will be available at:
- **Local**: http://localhost:8501
- **Network**: http://your-ip:8501 (accessible from mobile/other devices)

## 🔧 Configuration

### Environment Variables
Create a `.env` file with:
```env
OANDA_API_KEY=your_api_key_here
OANDA_ACCOUNT_ID=your_account_id_here
```

### Trading Strategy
The bot implements a simple strategy:
- **BUY**: When price increases >0.1% in 1 minute
- **SELL**: When price decreases >0.1% in 1 minute  
- **HOLD**: Otherwise

Modify `bot.py` to implement your own strategies.

## 📁 Project Structure

```
├── bot.py              # Main trading bot logic
├── dashboard.py        # Streamlit dashboard
├── run_bot.py         # Bot launcher script
├── run_dashboard.py   # Dashboard launcher script
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variables template
├── README.md          # This file
└── forex_trading.db   # SQLite database (created automatically)
```

## 🗄️ Database Schema

### Trades Table
- `id`: Unique trade identifier
- `timestamp`: When the trade occurred
- `pair`: Trading pair (EUR_USD, GBP_USD)
- `action`: BUY, SELL, or HOLD
- `price`: Execution price
- `balance`: Account balance after trade

### Balances Table
- `timestamp`: When balance was recorded
- `balance`: Account balance amount

## 🔍 Monitoring

The dashboard shows:
- **Real-time balance** with profit/loss
- **Trade history** table
- **Balance chart** over time
- **Summary statistics** (total trades, buy/sell counts)
- **Auto-refresh** every minute

## 🛑 Stopping the Bot

- **Trading Bot**: Press `Ctrl+C` in the bot terminal
- **Dashboard**: Press `Ctrl+C` in the dashboard terminal

## 🔒 Security Notes

- Uses OANDA Demo Account (no real money)
- API credentials stored in `.env` file (keep secure)
- Database stored locally in `forex_trading.db`

## 🚨 Troubleshooting

### Common Issues:

1. **"OANDA_API_KEY not set"**
   - Check your `.env` file exists and has correct values
   - Or export variables: `export OANDA_API_KEY='your_key'`

2. **"Database connection failed"**
   - Ensure you have write permissions in the project directory
   - Check if SQLite is available

3. **Dashboard shows no data**
   - Start the trading bot first: `python run_bot.py`
   - Check bot logs for errors

4. **Port 8501 already in use**
   - Kill existing Streamlit processes: `pkill -f streamlit`
   - Or change port in `run_dashboard.py`

## 📈 Extending the Bot

### Add New Trading Pairs
Edit `bot.py` in the `__init__` method:
```python
self.pairs = ['EUR_USD', 'GBP_USD', 'USD_JPY', 'AUD_USD']
```

### Implement New Strategies
Modify the `analyze_and_trade` method in `bot.py` to add your own logic.

### Custom Dashboard Views
Add new visualizations in `dashboard.py` using Streamlit and Plotly.

## 📞 Support

- Check the logs in `trading_bot.log`
- Verify OANDA API credentials
- Ensure all dependencies are installed

## ⚠️ Disclaimer

This is a demo trading bot for educational purposes. It uses OANDA's demo account with virtual money. Never use this bot with real money without proper testing and risk management.

---

**Happy Trading! 🎯**
