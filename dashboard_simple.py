#!/usr/bin/env python3
"""
Simplified Forex Trading Dashboard
Basic dashboard that displays trading data without external dependencies.
"""

import sqlite3
import time
from datetime import datetime
import os

class SimpleTradingDashboard:
    def __init__(self):
        """Initialize the simplified dashboard."""
        self.db_path = 'forex_trading.db'
        self.update_interval = 30  # seconds
        
    def get_database_connection(self):
        """Create a connection to the SQLite database."""
        try:
            conn = sqlite3.connect(self.db_path)
            return conn
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return None
    
    def get_trades_data(self):
        """Fetch all trades from the database."""
        conn = self.get_database_connection()
        if conn is None:
            return []
        
        try:
            query = """
                SELECT timestamp, pair, action, price, balance
                FROM trades
                WHERE pair != 'SYSTEM'
                ORDER BY timestamp DESC
                LIMIT 20
            """
            cursor = conn.cursor()
            cursor.execute(query)
            trades = cursor.fetchall()
            
            return trades
        except Exception as e:
            print(f"❌ Failed to fetch trades: {e}")
            return []
        finally:
            conn.close()
    
    def get_balances_data(self):
        """Fetch balance history from the database."""
        conn = self.get_database_connection()
        if conn is None:
            return []
        
        try:
            query = """
                SELECT timestamp, balance
                FROM balances
                ORDER BY timestamp ASC
                LIMIT 50
            """
            cursor = conn.cursor()
            cursor.execute(query)
            balances = cursor.fetchall()
            
            return balances
        except Exception as e:
            print(f"❌ Failed to fetch balances: {e}")
            return []
        finally:
            conn.close()
    
    def get_current_balance(self):
        """Get the most recent account balance."""
        conn = self.get_database_connection()
        if conn is None:
            return 0.0
        
        try:
            query = "SELECT balance FROM balances ORDER BY timestamp DESC LIMIT 1"
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchone()
            
            return float(result[0]) if result else 0.0
        except Exception as e:
            print(f"❌ Failed to get current balance: {e}")
            return 0.0
        finally:
            conn.close()
    
    def calculate_summary_stats(self, trades, balances):
        """Calculate summary statistics for the dashboard."""
        stats = {
            'total_trades': len(trades),
            'buy_trades': len([t for t in trades if t[2] == 'BUY']),
            'sell_trades': len([t for t in trades if t[2] == 'SELL']),
            'total_profit_loss': 0.0,
            'initial_balance': 10000.0,
            'current_balance': 0.0
        }
        
        if balances:
            stats['current_balance'] = balances[-1][1]
            stats['total_profit_loss'] = stats['current_balance'] - stats['initial_balance']
        
        return stats
    
    def display_dashboard(self):
        """Display the trading dashboard in the terminal."""
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print("📈 Forex Trading Bot Dashboard (Public API)")
        print("=" * 60)
        print(f"🕐 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Get data
        trades = self.get_trades_data()
        balances = self.get_balances_data()
        current_balance = self.get_current_balance()
        stats = self.calculate_summary_stats(trades, balances)
        
        # Display key metrics
        print("\n📊 Account Overview")
        print("-" * 30)
        print(f"💰 Current Balance: ${stats['current_balance']:,.2f}")
        print(f"📈 Total Profit/Loss: ${stats['total_profit_loss']:+,.2f}")
        print(f"🔄 Total Trades: {stats['total_trades']}")
        print(f"🟢 Buy Trades: {stats['buy_trades']}")
        print(f"🔴 Sell Trades: {stats['sell_trades']}")
        
        # Display recent trades
        print(f"\n📋 Recent Trades (Last {len(trades)})")
        print("-" * 60)
        if trades:
            print(f"{'Timestamp':<20} {'Pair':<6} {'Action':<6} {'Price':<10} {'Balance':<12}")
            print("-" * 60)
            for trade in trades:
                timestamp = datetime.fromisoformat(trade[0]).strftime('%m-%d %H:%M:%S')
                pair = trade[1]
                action = trade[2]
                price = f"{trade[3]:.5f}"
                balance = f"${trade[4]:,.2f}"
                print(f"{timestamp:<20} {pair:<6} {action:<6} {price:<10} {balance:<12}")
        else:
            print("No trades recorded yet.")
        
        # Display balance history
        print(f"\n💰 Balance History (Last {len(balances)} records)")
        print("-" * 40)
        if balances:
            print(f"{'Timestamp':<20} {'Balance':<15}")
            print("-" * 40)
            for balance in balances[-10:]:  # Show last 10
                timestamp = datetime.fromisoformat(balance[0]).strftime('%m-%d %H:%M:%S')
                balance_amount = f"${balance[1]:,.2f}"
                print(f"{timestamp:<20} {balance_amount:<15}")
        else:
            print("No balance history available.")
        
        # Footer
        print("\n" + "=" * 60)
        print("🤖 Forex Trading Bot Dashboard | Auto-refreshes every 30 seconds")
        print("🌐 Using public API - no registration required")
        print("💡 Press Ctrl+C to stop")
        print("=" * 60)
    
    def run_dashboard(self):
        """Main dashboard loop."""
        print("🚀 Starting Simplified Forex Trading Dashboard...")
        print("✅ No external dependencies required")
        print("📊 Dashboard will refresh every 30 seconds")
        print("💡 Press Ctrl+C to stop")
        
        try:
            while True:
                self.display_dashboard()
                time.sleep(self.update_interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Dashboard stopped by user")
        except Exception as e:
            print(f"❌ Dashboard error: {e}")

def main():
    """Main function to run the dashboard."""
    try:
        dashboard = SimpleTradingDashboard()
        dashboard.run_dashboard()
    except Exception as e:
        print(f"❌ Dashboard error: {e}")

if __name__ == "__main__":
    main()