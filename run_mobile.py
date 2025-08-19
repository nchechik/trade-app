#!/usr/bin/env python3
"""
Mobile Forex Trading Bot Launcher
Starts both the trading bot and mobile dashboard for phone access.
"""

import subprocess
import sys
import time
import threading
import os
import socket

def get_local_ip():
    """Get the local IP address for network access."""
    try:
        # Get local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "localhost"

def start_trading_bot():
    """Start the trading bot in a separate thread."""
    print("🤖 Starting trading bot...")
    try:
        # Import and run the bot
        from bot_simple import SimpleForexTradingBot
        bot = SimpleForexTradingBot()
        bot.run()
    except Exception as e:
        print(f"❌ Bot error: {e}")

def start_mobile_dashboard():
    """Start the mobile dashboard."""
    print("📱 Starting mobile dashboard...")
    try:
        # Import and run the mobile dashboard
        from mobile_dashboard import run_mobile_dashboard
        run_mobile_dashboard()
    except Exception as e:
        print(f"❌ Dashboard error: {e}")

def main():
    """Main function to start the mobile trading project."""
    print("🚀 Mobile Forex Trading Bot Project Starter")
    print("=" * 60)
    print("✅ No external dependencies required")
    print("✅ No registration required - using free public Forex API")
    print("📱 Mobile-friendly dashboard included!")
    print("=" * 60)
    
    # Get local IP for network access
    local_ip = get_local_ip()
    
    print("\n🎯 Starting Mobile Forex Trading Bot Project...")
    print("=" * 60)
    
    # Check if database exists
    if not os.path.exists('forex_trading.db'):
        print("⚠️  No trading database found. Will be created automatically.")
        print()
    
    # Start bot in background thread
    print("🤖 Starting trading bot in background...")
    bot_thread = threading.Thread(target=start_trading_bot, daemon=True)
    bot_thread.start()
    
    # Wait a moment for bot to initialize
    print("⏳ Waiting for bot to initialize...")
    time.sleep(3)
    
    # Start mobile dashboard
    print("📱 Starting mobile dashboard...")
    print("=" * 60)
    print("🌐 Access URLs:")
    print(f"  📱 Local: http://localhost:8080")
    print(f"  📱 Network: http://{local_ip}:8080")
    print("=" * 60)
    print("💡 To access from your phone:")
    print(f"  1. Make sure your phone is on the same WiFi network")
    print(f"  2. Open your phone's browser")
    print(f"  3. Go to: http://{local_ip}:8080")
    print("=" * 60)
    print("💡 Press Ctrl+C to stop everything")
    
    try:
        start_mobile_dashboard()
    except KeyboardInterrupt:
        print("\n🛑 Stopping project...")
        print("✅ Trading bot and mobile dashboard stopped")

if __name__ == "__main__":
    main()