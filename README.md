# 📈 Forex Trading Bot with Live Dashboard

A fully automated Forex trading bot that connects to OANDA and provides a real-time dashboard for monitoring trades and account performance.

## 🚀 Features

- **Automated Trading**: Implements a simple momentum-based strategy for EUR/USD and GBP/USD
- **Live Dashboard**: Beautiful Streamlit interface showing real-time data
- **Database Logging**: All trades and balances stored in SQLite
- **OANDA Integration**: Connects to OANDA demo account via API
- **Background Operation**: Bot runs continuously while dashboard provides live updates

## 🎯 Trading Strategy

The bot implements a simple momentum strategy:
- **BUY**: When price increases >0.1% in the last minute
- **SELL**: When price decreases >0.1% in the last minute  
- **HOLD**: Otherwise (with 60-second cooldown between trades)

## 📋 Requirements

- Python 3.8+
- OANDA demo account
- Internet connection

## ⚙️ Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure OANDA Credentials
1. Get your OANDA API key from [OANDA API page](https://www.oanda.com/account/api)
2. Get your Account ID from your OANDA dashboard
3. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
4. Edit `.env` with your actual credentials:
   ```
   OANDA_API_KEY=your_actual_api_key_here
   OANDA_ACCOUNT_ID=your_actual_account_id_here
   ```

## 🚀 Quick Start

### Option 1: Use the Launcher (Recommended)
```bash
python launch.py
```

This will:
- Start the trading bot in the background
- Launch the dashboard on http://localhost:8501
- Show you the dashboard URL
- Monitor both processes

### Option 2: Run Components Separately

**Start the trading bot:**
```bash
python bot.py
```

**Start the dashboard (in another terminal):**
```bash
streamlit run dashboard.py
```

## 📊 Dashboard Features

- **Account Summary**: Current balance, total trades, buy/sell counts
- **Balance Chart**: Interactive chart showing account balance over time
- **Trades Table**: Complete history of all executed trades
- **Auto-refresh**: Updates every minute automatically
- **Mobile Friendly**: Responsive design for all devices

## 🔧 Configuration

### Trading Parameters
Edit `bot.py` to modify:
- `min_price_change`: Minimum price change threshold (default: 0.001 = 0.1%)
- `trade_cooldown`: Seconds between trades (default: 60)
- `pairs`: Currency pairs to trade (default: ["EUR_USD", "GBP_USD"])

### Dashboard Settings
Edit `dashboard.py` to customize:
- Auto-refresh interval
- Chart appearance
- Table styling

## 📁 Project Structure

```
├── bot.py              # Main trading bot
├── dashboard.py        # Streamlit dashboard
├── launch.py           # Launcher script
├── requirements.txt    # Python dependencies
├── .env.example       # Environment template
├── README.md          # This file
└── forex_trading.db   # SQLite database (created automatically)
```

## 🗄️ Database Schema

### Trades Table
- `id`: Unique trade identifier
- `timestamp`: When the trade occurred
- `pair`: Currency pair (e.g., EUR_USD)
- `action`: BUY, SELL, or HOLD
- `price`: Execution price
- `balance`: Account balance after trade

### Balances Table
- `timestamp`: When balance was recorded
- `balance`: Account balance amount

## 🔒 Security Notes

- **Demo Account Only**: This bot uses OANDA's practice environment
- **API Key Protection**: Never commit your `.env` file to version control
- **Risk Warning**: Forex trading involves substantial risk of loss

## 🛠️ Troubleshooting

### Common Issues

**"Missing OANDA credentials"**
- Ensure `.env` file exists and contains valid credentials
- Check that environment variables are loaded correctly

**"Database connection failed"**
- Bot needs to run first to create the database
- Check file permissions in the project directory

**"Dashboard not loading"**
- Ensure Streamlit is installed: `pip install streamlit`
- Check if port 8501 is available
- Try refreshing the browser

### Logs
- Bot logs: `trading_bot.log`
- Dashboard logs: Check terminal output

## 📈 Extending the Bot

### Adding New Strategies
1. Modify the `trading_strategy()` method in `bot.py`
2. Add new indicators or analysis
3. Implement more sophisticated decision logic

### Adding New Currency Pairs
1. Add to the `pairs` list in `bot.py`
2. Ensure OANDA supports the pair
3. Test with small amounts first

### Custom Dashboard Widgets
1. Add new methods to the `TradingDashboard` class
2. Create new Streamlit components
3. Integrate with additional data sources

## 📞 Support

For issues or questions:
1. Check the logs for error messages
2. Verify your OANDA credentials
3. Ensure all dependencies are installed
4. Check that the database file is writable

## ⚠️ Disclaimer

This software is for educational and demonstration purposes only. Forex trading involves substantial risk of loss and is not suitable for all investors. Past performance does not guarantee future results. Always test thoroughly with demo accounts before using real money.

## 📄 License

This project is open source and available under the MIT License.
