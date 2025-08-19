#!/usr/bin/env python3
"""
Forex Trading Bot Project Starter
Master script to launch both the trading bot and dashboard.
"""

import subprocess
import sys
import time
import threading

def install_dependencies():
    """Install required Python packages."""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def start_bot():
    """Start the trading bot in a separate thread."""
    print("🤖 Starting trading bot...")
    try:
        # Import and run the bot
        from bot import ForexTradingBot
        bot = ForexTradingBot()
        bot.run()
    except Exception as e:
        print(f"❌ Bot error: {e}")

def start_dashboard():
    """Start the Streamlit dashboard."""
    print("📊 Starting dashboard...")
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "dashboard.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ])
    except Exception as e:
        print(f"❌ Dashboard error: {e}")

def main():
    """Main function to start the entire project."""
    print("🚀 Forex Trading Bot Project Starter (Public API)")
    print("=" * 50)
    print("✅ No registration required - using free public Forex API")
    print("=" * 50)
    
    # Install dependencies
    if not install_dependencies():
        print("⚠️  Continuing anyway, but some features may not work...")
    
    print("\n🎯 Starting Forex Trading Bot Project...")
    print("=" * 50)
    
    # Start bot in background thread
    bot_thread = threading.Thread(target=start_bot, daemon=True)
    bot_thread.start()
    
    # Wait a moment for bot to initialize
    print("⏳ Waiting for bot to initialize...")
    time.sleep(3)
    
    # Start dashboard
    print("🌐 Launching dashboard...")
    print("📱 Dashboard will open in your browser")
    print("🌐 URL: http://localhost:8501")
    print("💡 Press Ctrl+C to stop everything")
    print("=" * 50)
    
    try:
        start_dashboard()
    except KeyboardInterrupt:
        print("\n🛑 Stopping project...")
        print("✅ Trading bot and dashboard stopped")

if __name__ == "__main__":
    main()