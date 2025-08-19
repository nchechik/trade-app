#!/usr/bin/env python3
"""
Forex Trading Bot Launcher
Starts both the trading bot and dashboard in separate processes.
"""

import subprocess
import sys
import time
import os
import signal
import threading
from pathlib import Path

class TradingBotLauncher:
    def __init__(self):
        """Initialize the launcher."""
        self.bot_process = None
        self.dashboard_process = None
        self.running = False
        
    def check_dependencies(self):
        """Check if all required dependencies are installed."""
        try:
            import streamlit
            import oandapyV20
            import pandas
            import plotly
            import dotenv
            print("✅ All dependencies are installed")
            return True
        except ImportError as e:
            print(f"❌ Missing dependency: {e}")
            print("Please install dependencies with: pip install -r requirements.txt")
            return False
    
    def check_environment(self):
        """Check if environment variables are set."""
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('OANDA_API_KEY')
        account_id = os.getenv('OANDA_ACCOUNT_ID')
        
        if not api_key:
            print("❌ OANDA_API_KEY environment variable not set")
            return False
        
        if not account_id:
            print("❌ OANDA_ACCOUNT_ID environment variable not set")
            return False
        
        print("✅ Environment variables are configured")
        return True
    
    def start_bot(self):
        """Start the trading bot in a separate process."""
        try:
            print("🚀 Starting Forex Trading Bot...")
            self.bot_process = subprocess.Popen(
                [sys.executable, 'bot.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print(f"✅ Bot started with PID: {self.bot_process.pid}")
            return True
        except Exception as e:
            print(f"❌ Failed to start bot: {e}")
            return False
    
    def start_dashboard(self):
        """Start the Streamlit dashboard in a separate process."""
        try:
            print("🌐 Starting Trading Dashboard...")
            self.dashboard_process = subprocess.Popen(
                [sys.executable, '-m', 'streamlit', 'run', 'dashboard.py', '--server.port', '8501'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print(f"✅ Dashboard started with PID: {self.dashboard_process.pid}")
            return True
        except Exception as e:
            print(f"❌ Failed to start dashboard: {e}")
            return False
    
    def wait_for_dashboard(self):
        """Wait for dashboard to be ready and show the URL."""
        print("⏳ Waiting for dashboard to start...")
        time.sleep(5)  # Give Streamlit time to start
        
        print("\n" + "="*60)
        print("🎯 FOREX TRADING DASHBOARD IS READY!")
        print("="*60)
        print("📱 Open your browser and go to:")
        print("   http://localhost:8501")
        print("\n📊 The dashboard will show:")
        print("   • Live account balance")
        print("   • Trading history")
        print("   • Balance charts")
        print("   • Real-time updates every minute")
        print("\n🤖 The trading bot is running in the background")
        print("   • Trades EUR/USD and GBP/USD")
        print("   • Logs all activity to database")
        print("   • Implements simple momentum strategy")
        print("="*60)
        print("\n💡 Press Ctrl+C to stop both bot and dashboard")
    
    def monitor_processes(self):
        """Monitor the running processes."""
        try:
            while self.running:
                # Check if bot is still running
                if self.bot_process and self.bot_process.poll() is not None:
                    print("❌ Bot process stopped unexpectedly")
                    self.running = False
                    break
                
                # Check if dashboard is still running
                if self.dashboard_process and self.dashboard_process.poll() is not None:
                    print("❌ Dashboard process stopped unexpectedly")
                    self.running = False
                    break
                
                time.sleep(5)
                
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")
            self.stop_all()
    
    def stop_all(self):
        """Stop all running processes."""
        self.running = False
        
        if self.bot_process:
            print("🛑 Stopping trading bot...")
            self.bot_process.terminate()
            try:
                self.bot_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.bot_process.kill()
            print("✅ Bot stopped")
        
        if self.dashboard_process:
            print("🛑 Stopping dashboard...")
            self.dashboard_process.terminate()
            try:
                self.dashboard_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.dashboard_process.kill()
            print("✅ Dashboard stopped")
        
        print("👋 All processes stopped. Goodbye!")
    
    def run(self):
        """Main launcher execution."""
        print("🚀 Forex Trading Bot Launcher")
        print("="*40)
        
        # Check dependencies
        if not self.check_dependencies():
            return
        
        # Check environment
        if not self.check_environment():
            print("\n📝 Please create a .env file with:")
            print("OANDA_API_KEY=your_api_key_here")
            print("OANDA_ACCOUNT_ID=your_account_id_here")
            return
        
        # Start bot
        if not self.start_bot():
            return
        
        # Start dashboard
        if not self.start_dashboard():
            self.stop_all()
            return
        
        # Show dashboard URL
        self.wait_for_dashboard()
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, lambda sig, frame: self.stop_all())
        signal.signal(signal.SIGTERM, lambda sig, frame: self.stop_all())
        
        # Start monitoring
        self.running = True
        self.monitor_processes()

def main():
    """Main entry point."""
    launcher = TradingBotLauncher()
    launcher.run()

if __name__ == "__main__":
    main()