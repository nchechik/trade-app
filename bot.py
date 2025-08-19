#!/usr/bin/env python3
"""
Forex Trading Bot
Connects to OANDA Demo Account and implements a simple trading strategy.
Runs continuously in the background, logging trades and balances to SQLite.
"""

import os
import time
import logging
import sqlite3
import threading
from datetime import datetime, timedelta
from dotenv import load_dotenv
from oandapyV20 import API
from oandapyV20.endpoints.accounts import AccountDetails
from oandapyV20.endpoints.pricing import PricingInfo
from oandapyV20.endpoints.orders import OrderCreate
from oandapyV20.endpoints.trades import TradeCRUD
from oandapyV20.contrib.requests import MarketOrderRequest

# Load environment variables
load_dotenv()

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

class ForexTradingBot:
    def __init__(self):
        """Initialize the trading bot with OANDA connection and database setup."""
        self.api_key = os.getenv('OANDA_API_KEY')
        self.account_id = os.getenv('OANDA_ACCOUNT_ID')
        
        if not self.api_key or not self.account_id:
            logger.error("OANDA_API_KEY and OANDA_ACCOUNT_ID must be set in environment variables")
            raise ValueError("Missing OANDA credentials")
        
        self.api = API(access_token=self.api_key, environment="practice")
        self.pairs = ["EUR_USD", "GBP_USD"]
        self.price_history = {pair: [] for pair in self.pairs}
        self.last_trade_time = {pair: datetime.now() for pair in self.pairs}
        
        # Initialize database
        self.init_database()
        
        # Trading parameters
        self.min_price_change = 0.001  # 0.1%
        self.trade_cooldown = 60  # seconds
        
        logger.info("Forex Trading Bot initialized successfully")
    
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
            
            conn.commit()
            conn.close()
            logger.info("Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise
    
    def get_account_balance(self):
        """Get current account balance from OANDA."""
        try:
            account_details = AccountDetails(accountID=self.account_id)
            response = self.api.request(account_details)
            balance = float(response['account']['balance'])
            return balance
        except Exception as e:
            logger.error(f"Failed to get account balance: {e}")
            return None
    
    def get_current_prices(self):
        """Get current prices for all trading pairs."""
        try:
            pricing_info = PricingInfo(accountID=self.account_id, instruments=",".join(self.pairs))
            response = self.api.request(pricing_info)
            
            prices = {}
            for price in response['prices']:
                pair = price['instrument']
                bid = float(price['bids'][0]['price'])
                ask = float(price['asks'][0]['price'])
                prices[pair] = (bid, ask)
            
            return prices
        except Exception as e:
            logger.error(f"Failed to get current prices: {e}")
            return {}
    
    def calculate_price_change(self, pair):
        """Calculate price change percentage over the last minute."""
        if len(self.price_history[pair]) < 2:
            return 0
        
        current_price = self.price_history[pair][-1]
        previous_price = self.price_history[pair][-2]
        
        if previous_price == 0:
            return 0
        
        return (current_price - previous_price) / previous_price
    
    def execute_trade(self, pair, action, price):
        """Execute a trade and log it to the database."""
        try:
            # Get current balance
            balance = self.get_account_balance()
            if balance is None:
                return False
            
            # Log trade to database
            conn = sqlite3.connect('forex_trading.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO trades (timestamp, pair, action, price, balance)
                VALUES (?, ?, ?, ?, ?)
            ''', (datetime.now().isoformat(), pair, action, price, balance))
            
            # Log balance
            cursor.execute('''
                INSERT OR REPLACE INTO balances (timestamp, balance)
                VALUES (?, ?)
            ''', (datetime.now().isoformat(), balance))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Trade executed: {action} {pair} at {price}, Balance: {balance}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to execute trade: {e}")
            return False
    
    def trading_strategy(self, pair, current_price):
        """Implement the trading strategy."""
        now = datetime.now()
        
        # Check cooldown period
        if (now - self.last_trade_time[pair]).seconds < self.trade_cooldown:
            return "HOLD"
        
        # Calculate price change
        price_change = self.calculate_price_change(pair)
        
        # Trading logic
        if price_change > self.min_price_change:
            action = "BUY"
        elif price_change < -self.min_price_change:
            action = "SELL"
        else:
            action = "HOLD"
        
        # Execute trade if not HOLD
        if action != "HOLD":
            if self.execute_trade(pair, action, current_price):
                self.last_trade_time[pair] = now
        
        return action
    
    def update_price_history(self, pair, price):
        """Update price history for a trading pair."""
        now = datetime.now()
        
        # Keep only last 10 minutes of data (600 seconds)
        cutoff_time = now - timedelta(seconds=600)
        
        # Add new price with timestamp
        self.price_history[pair].append((now, price))
        
        # Remove old prices
        self.price_history[pair] = [
            (timestamp, price) for timestamp, price in self.price_history[pair]
            if timestamp > cutoff_time
        ]
    
    def run_trading_cycle(self):
        """Run one complete trading cycle."""
        try:
            # Get current prices
            prices = self.get_current_prices()
            if not prices:
                return
            
            # Update price history and execute strategy for each pair
            for pair in self.pairs:
                if pair in prices:
                    bid, ask = prices[pair]
                    current_price = (bid + ask) / 2  # Use mid price
                    
                    # Update price history
                    self.update_price_history(pair, current_price)
                    
                    # Execute trading strategy
                    action = self.trading_strategy(pair, current_price)
                    
                    logger.info(f"{pair}: Price={current_price:.5f}, Action={action}")
            
            # Log current balance
            balance = self.get_account_balance()
            if balance is not None:
                conn = sqlite3.connect('forex_trading.db')
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO balances (timestamp, balance)
                    VALUES (?, ?)
                ''', (datetime.now().isoformat(), balance))
                conn.commit()
                conn.close()
                
        except Exception as e:
            logger.error(f"Trading cycle failed: {e}")
    
    def run(self):
        """Main bot loop - runs continuously."""
        logger.info("Starting Forex Trading Bot...")
        
        while True:
            try:
                self.run_trading_cycle()
                time.sleep(60)  # Wait 1 minute between cycles
                
            except KeyboardInterrupt:
                logger.info("Bot stopped by user")
                break
            except Exception as e:
                logger.error(f"Unexpected error in main loop: {e}")
                time.sleep(60)  # Wait before retrying

def main():
    """Main entry point."""
    try:
        bot = ForexTradingBot()
        bot.run()
    except Exception as e:
        logger.error(f"Bot initialization failed: {e}")

if __name__ == "__main__":
    main()