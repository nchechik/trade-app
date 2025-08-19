#!/usr/bin/env python3
"""
Simplified Forex Trading Bot
Uses public Forex API to fetch live exchange rates and implements simulated trading.
Minimal dependencies - works with basic Python installation.
"""

import time
import sqlite3
import logging
from datetime import datetime
import urllib.request
import json
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SimpleForexTradingBot:
    def __init__(self):
        """Initialize the simplified trading bot."""
        # Public Forex API - no registration required
        self.api_url = "https://api.frankfurter.app/latest"
        
        # Trading pairs to monitor (USD base currency)
        self.pairs = ['EUR', 'GBP']  # Will fetch USD→EUR and USD→GBP rates
        
        # Simulated account balance (starts at $10,000)
        self.simulated_balance = 10000.0
        
        # Initialize database
        self.init_database()
        
        # Track previous prices for strategy
        self.previous_prices = {}
        
        # Track trade count for balance simulation
        self.trade_count = 0
        
        logger.info("Simple Forex Trading Bot initialized successfully")
        logger.info(f"Using public API: {self.api_url}")
        logger.info(f"Simulated starting balance: ${self.simulated_balance:,.2f}")
    
    def init_database(self):
        """Initialize SQLite database with required tables."""
        try:
            conn = sqlite3.connect('forex_trading.db')
            cursor = conn.cursor()
            
            # Create trades table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS trades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    pair TEXT NOT NULL,
                    action TEXT NOT NULL,
                    price REAL NOT NULL,
                    balance REAL NOT NULL
                )
            ''')
            
            # Create balances table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS balances (
                    timestamp TEXT PRIMARY KEY,
                    balance REAL NOT NULL
                )
            ''')
            
            # Insert initial balance
            cursor.execute('''
                INSERT OR REPLACE INTO balances (timestamp, balance)
                VALUES (?, ?)
            ''', (datetime.now().isoformat(), self.simulated_balance))
            
            conn.commit()
            conn.close()
            logger.info("Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise
    
    def get_current_prices(self):
        """Get current exchange rates from public Forex API using urllib."""
        try:
            # Fetch USD rates for EUR and GBP
            url = f"{self.api_url}?from=USD&to=EUR,GBP"
            
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
            
            rates = data.get('rates', {})
            
            # Extract rates (these are USD→EUR and USD→GBP rates)
            prices = {}
            if 'EUR' in rates:
                prices['EUR'] = rates['EUR']
            if 'GBP' in rates:
                prices['GBP'] = rates['GBP']
            
            logger.info(f"Fetched rates: {prices}")
            return prices
            
        except Exception as e:
            logger.error(f"Failed to fetch exchange rates: {e}")
            return {}
    
    def simulate_trade_execution(self, pair, action, price):
        """Simulate trade execution and update balance."""
        # Simple simulation: each trade affects balance by a small amount
        trade_amount = 100.0  # Fixed trade size
        
        if action == "BUY":
            # Simulate buying foreign currency (costs USD)
            cost = trade_amount * price
            self.simulated_balance -= cost
            logger.info(f"Simulated BUY: Spent ${cost:.2f} to buy {trade_amount} {pair}")
            
        elif action == "SELL":
            # Simulate selling foreign currency (earns USD)
            earnings = trade_amount / price
            self.simulated_balance += earnings
            logger.info(f"Simulated SELL: Earned ${earnings:.2f} from selling {trade_amount} {pair}")
        
        # Add some random variation to make it more realistic
        variation = random.uniform(-0.5, 0.5)  # Small random change
        self.simulated_balance += variation
        
        # Ensure balance doesn't go negative
        self.simulated_balance = max(0.0, self.simulated_balance)
        
        return self.simulated_balance
    
    def execute_trade(self, pair, action, price):
        """Execute a simulated trade and log it to the database."""
        try:
            # Simulate the trade and get new balance
            new_balance = self.simulate_trade_execution(pair, action, price)
            
            conn = sqlite3.connect('forex_trading.db')
            cursor = conn.cursor()
            
            # Log the trade
            cursor.execute('''
                INSERT INTO trades (timestamp, pair, action, price, balance)
                VALUES (?, ?, ?, ?, ?)
            ''', (datetime.now().isoformat(), pair, action, price, new_balance))
            
            # Log the balance
            cursor.execute('''
                INSERT OR REPLACE INTO balances (timestamp, balance)
                VALUES (?, ?)
            ''', (datetime.now().isoformat(), new_balance))
            
            conn.commit()
            conn.close()
            
            self.trade_count += 1
            logger.info(f"Trade executed: {action} {pair} at {price:.5f}, New Balance: ${new_balance:,.2f}")
            
        except Exception as e:
            logger.error(f"Failed to log trade: {e}")
    
    def analyze_and_trade(self):
        """Analyze current prices and execute trading strategy."""
        current_time = datetime.now()
        
        # Fetch current prices from public API
        current_prices = self.get_current_prices()
        
        if not current_prices:
            logger.warning("No prices fetched, skipping trading cycle")
            return
        
        for pair in self.pairs:
            if pair not in current_prices:
                continue
                
            current_price = current_prices[pair]
            
            # Get previous price for this pair
            if pair not in self.previous_prices:
                self.previous_prices[pair] = current_price
                logger.info(f"Initial price for {pair}: {current_price:.5f}")
                continue
            
            previous_price = self.previous_prices[pair]
            
            # Calculate price change percentage
            price_change_pct = ((current_price - previous_price) / previous_price) * 100
            
            # Trading strategy (simplified for demo)
            action = "HOLD"
            if price_change_pct > 0.05:  # Reduced threshold for more frequent trades
                action = "BUY"
                logger.info(f"{pair}: Price increased {price_change_pct:.3f}% - BUY signal")
            elif price_change_pct < -0.05:
                action = "SELL"
                logger.info(f"{pair}: Price decreased {abs(price_change_pct):.3f}% - SELL signal")
            else:
                logger.info(f"{pair}: Price change {price_change_pct:.3f}% - HOLD")
            
            # Execute trade if not HOLD
            if action != "HOLD":
                self.execute_trade(pair, action, current_price)
            
            # Update previous price
            self.previous_prices[pair] = current_price
        
        # Log current balance every cycle
        self.execute_trade("SYSTEM", "BALANCE_UPDATE", 0.0)
        
        logger.info(f"Trading cycle complete. Current balance: ${self.simulated_balance:,.2f}")
    
    def run(self):
        """Main loop - run the trading bot continuously."""
        logger.info("Starting Simple Forex Trading Bot with public API...")
        logger.info("No registration required - using free public Forex rates")
        
        try:
            while True:
                logger.info("Starting trading cycle...")
                self.analyze_and_trade()
                
                # Wait for 1 minute before next cycle
                logger.info("Waiting 60 seconds until next cycle...")
                time.sleep(60)
                
        except KeyboardInterrupt:
            logger.info("Trading bot stopped by user")
        except Exception as e:
            logger.error(f"Trading bot error: {e}")
            raise

def main():
    """Main function to run the trading bot."""
    try:
        bot = SimpleForexTradingBot()
        bot.run()
    except Exception as e:
        logger.error(f"Failed to start trading bot: {e}")
        raise

if __name__ == "__main__":
    main()