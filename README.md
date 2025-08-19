# 🤖 Forex Trading Bot with Live Dashboard (Public API)

A fully automated Forex trading bot that uses **free public Forex APIs** with a real-time Streamlit dashboard for monitoring simulated trades and account performance. **No registration or API keys required!**

## 🚀 Features

- **Automated Trading**: Monitors EUR/USD and GBP/USD every minute using public API
- **Smart Strategy**: Buys on >0.05% price increase, sells on >0.05% decrease
- **Live Dashboard**: Real-time updates with charts and trade history
- **Database Storage**: SQLite database for all trades and balance history
- **Public API Integration**: Uses free exchangerate.host API - no registration needed
- **Simulated Trading**: Realistic trading simulation with balance tracking
- **Auto-refresh**: Dashboard updates automatically every minute

## 📋 Requirements

- Python 3.8+
- Internet connection
- **No registration or API keys required!**

## 🛠️ Installation

1. **Clone/Download** this project to your workspace
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **That's it!** No API keys or account setup needed.

## 🚀 Quick Start

### Option 1: Run Everything with One Command
```bash
python start_project.py
```

**That's it!** This will:
- ✅ Install all dependencies automatically
- ✅ Start the trading bot in the background
- ✅ Launch the live dashboard
- ✅ Open your browser to the dashboard

### Option 2: Manual Execution
```bash
# Terminal 1: Start trading bot
python run_bot.py

# Terminal 2: Start dashboard
python run_dashboard.py
```

## 📊 Dashboard Access

Once running, the dashboard will be available at:
- **Local**: http://localhost:8501
- **Network**: http://your-ip:8501 (accessible from mobile/other devices)

## 🔧 Configuration

### Trading Strategy
The bot implements a simple strategy:
- **BUY**: When price increases >0.05% in 1 minute
- **SELL**: When price decreases >0.05% in 1 minute  
- **HOLD**: Otherwise

Modify `bot.py` to implement your own strategies.

### Public API
The bot uses `https://api.exchangerate.host/latest` which provides:
- **USD→EUR** exchange rates
- **USD→GBP** exchange rates
- **No rate limits** or registration required
- **Real-time data** updated frequently

## 📁 Project Structure

```
├── bot.py              # Main trading bot logic (public API)
├── dashboard.py        # Streamlit dashboard
├── start_project.py    # Master launcher script
├── run_bot.py         # Bot launcher script
├── run_dashboard.py   # Dashboard launcher script
├── test_setup.py      # Setup verification script
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── forex_trading.db   # SQLite database (created automatically)
```

## 🗄️ Database Schema

### Trades Table
- `id`: Unique trade identifier
- `timestamp`: When the trade occurred
- `pair`: Trading pair (EUR, GBP)
- `action`: BUY, SELL, or HOLD
- `price`: Execution price (exchange rate)
- `balance`: Simulated account balance after trade

### Balances Table
- `timestamp`: When balance was recorded
- `balance`: Simulated account balance amount

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

- **No real money involved** - completely simulated trading
- **No API keys or credentials** stored
- **Public API access** - no account required
- **Database stored locally** in `forex_trading.db`

## 🚨 Troubleshooting

### Common Issues:

1. **"Failed to fetch exchange rates"**
   - Check your internet connection
   - The public API might be temporarily unavailable
   - Wait a few minutes and try again

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
self.pairs = ['EUR', 'GBP', 'JPY', 'AUD']  # Add more currencies
```

### Implement New Strategies
Modify the `analyze_and_trade` method in `bot.py` to add your own logic.

### Custom Dashboard Views
Add new visualizations in `dashboard.py` using Streamlit and Plotly.

### Use Different Public APIs
The bot can easily be modified to use other free Forex APIs:
- `https://api.frankfurter.app/latest`
- `https://open.er-api.com/v6/latest/USD`

## 📞 Support

- Check the logs in `trading_bot.log`
- Run `python test_setup.py` to verify everything works
- Ensure all dependencies are installed

## ⚠️ Disclaimer

This is a **simulated trading bot** for educational purposes. It uses public Forex APIs and simulated trading with no real money involved. The trading strategy is simplified and should not be used for actual trading without proper testing and risk management.

## 🌟 Why Public API?

- **No registration required** - start trading immediately
- **No API keys** to manage or secure
- **No rate limits** or usage restrictions
- **Always available** - no account suspensions
- **Perfect for learning** and testing strategies

---

**Happy Trading! 🎯 No registration needed! 🚀**
