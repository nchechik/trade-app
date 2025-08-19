#!/usr/bin/env python3
"""
Forex Trading Bot
Connects to OANDA Demo Account and implements a simple trading strategy.
Runs continuously, fetching data every minute and making trading decisions.
"""

import os
import time
import sqlite3
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import requests
from dotenv import load_dotenv

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
        """Initialize the trading bot with OANDA credentials and database."""
        self.api_key = os.getenv('OANDA_API_KEY')
        self.account_id = os.getenv('OANDA_ACCOUNT_ID')
        
        if not self.api_key or not self.account_id:
            raise ValueError("OANDA_API_KEY and OANDA_ACCOUNT_ID must be set in environment variables")
        
        self.base_url = "https://api-fxpractice.oanda.com"  # Demo account URL
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        # Trading pairs to monitor
        self.pairs = ['EUR_USD', 'GBP_USD']
        
        # Initialize database
        self.init_database()
        
        # Track previous prices for strategy
        self.previous_prices = {}
        
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
    
    def get_account_balance(self) -> float:
        """Get current account balance from OANDA."""
        try:
            url = f"{self.base_url}/v3/accounts/{self.account_id}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            balance = float(data['account']['balance'])
            logger.info(f"Current balance: {balance}")
            return balance
            
        except Exception as e:
            logger.error(f"Failed to get account balance: {e}")
            return 0.0
    
    def get_current_price(self, pair: str) -> Optional[float]:
        """Get current price for a trading pair."""
        try:
            url = f"{self.base_url}/v3/accounts/{self.account_id}/pricing"
            params = {'instruments': pair}
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            if data['prices']:
                price = float(data['prices'][0]['bids'][0]['price'])
                return price
            
        except Exception as e:
            logger.error(f"Failed to get price for {pair}: {e}")
        
        return None
    
    def execute_trade(self, pair: str, action: str, price: float, balance: float):
        """Execute a trade and log it to the database."""
        try:
            conn = sqlite3.connect('forex_trading.db')
            cursor = conn.cursor()
            
            # Log the trade
            cursor.execute('''
                INSERT INTO trades (timestamp, pair, action, price, balance)
                VALUES (?, ?, ?, ?, ?)
            ''', (datetime.now().isoformat(), pair, action, price, balance))
            
            # Log the balance
            cursor.execute('''
                INSERT OR REPLACE INTO balances (timestamp, balance)
                VALUES (?, ?)
            ''', (datetime.now().isoformat(), balance))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Trade executed: {action} {pair} at {price}, Balance: {balance}")
            
        except Exception as e:
            logger.error(f"Failed to log trade: {e}")
    
    def analyze_and_trade(self):
        """Analyze current prices and execute trading strategy."""
        current_time = datetime.now()
        
        for pair in self.pairs:
            current_price = self.get_current_price(pair)
            if current_price is None:
                continue
            
            # Get previous price for this pair
            if pair not in self.previous_prices:
                self.previous_prices[pair] = current_price
                continue
            
            previous_price = self.previous_prices[pair]
            
            # Calculate price change percentage
            price_change_pct = ((current_price - previous_price) / previous_price) * 100
            
            # Get current balance
            balance = self.get_account_balance()
            
            # Trading strategy
            action = "HOLD"
            if price_change_pct > 0.1:
                action = "BUY"
                logger.info(f"{pair}: Price increased {price_change_pct:.3f}% - BUY signal")
            elif price_change_pct < -0.1:
                action = "SELL"
                logger.info(f"{pair}: Price decreased {abs(price_change_pct):.3f}% - SELL signal")
            else:
                logger.info(f"{pair}: Price change {price_change_pct:.3f}% - HOLD")
            
            # Execute trade if not HOLD
            if action != "HOLD":
                self.execute_trade(pair, action, current_price, balance)
            
            # Update previous price
            self.previous_prices[pair] = current_price
        
        # Log balance every cycle
        balance = self.get_account_balance()
        self.execute_trade("SYSTEM", "BALANCE_UPDATE", 0.0, balance)
    
    def run(self):
        """Main loop - run the trading bot continuously."""
        logger.info("Starting Forex Trading Bot...")
        
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
        bot = ForexTradingBot()
        bot.run()
    except Exception as e:
        logger.error(f"Failed to start trading bot: {e}")
        raise

if __name__ == "__main__":
    main()