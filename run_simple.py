#!/usr/bin/env python3
"""
Simple Forex Trading Bot Launcher
Launches both the simplified bot and dashboard without external dependencies.
"""

import subprocess
import sys
import time
import threading
import os

def start_simple_bot():
    """Start the simplified trading bot in a separate thread."""
    print("🤖 Starting simplified trading bot...")
    try:
        # Import and run the bot
        from bot_simple import SimpleForexTradingBot
        bot = SimpleForexTradingBot()
        bot.run()
    except Exception as e:
        print(f"❌ Bot error: {e}")

def start_simple_dashboard():
    """Start the simplified dashboard."""
    print("📊 Starting simplified dashboard...")
    try:
        # Import and run the dashboard
        from dashboard_simple import SimpleTradingDashboard
        dashboard = SimpleTradingDashboard()
        dashboard.run_dashboard()
    except Exception as e:
        print(f"❌ Dashboard error: {e}")

def main():
    """Main function to start the simplified project."""
    print("🚀 Simple Forex Trading Bot Project Starter (Public API)")
    print("=" * 60)
    print("✅ No external dependencies required")
    print("✅ No registration required - using free public Forex API")
    print("=" * 60)
    
    print("\n🎯 Starting Simple Forex Trading Bot Project...")
    print("=" * 60)
    
    # Check if database exists
    if not os.path.exists('forex_trading.db'):
        print("⚠️  No trading database found. Will be created automatically.")
        print()
    
    # Start bot in background thread
    print("🤖 Starting trading bot in background...")
    bot_thread = threading.Thread(target=start_simple_bot, daemon=True)
    bot_thread.start()
    
    # Wait a moment for bot to initialize
    print("⏳ Waiting for bot to initialize...")
    time.sleep(3)
    
    # Start dashboard
    print("📊 Starting dashboard...")
    print("💡 Press Ctrl+C to stop everything")
    print("=" * 60)
    
    try:
        start_simple_dashboard()
    except KeyboardInterrupt:
        print("\n🛑 Stopping project...")
        print("✅ Trading bot and dashboard stopped")

if __name__ == "__main__":
    main()