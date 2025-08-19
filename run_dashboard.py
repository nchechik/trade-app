#!/usr/bin/env python3
"""
Forex Trading Dashboard Runner
Simple script to start the Streamlit dashboard.
"""

import subprocess
import sys
import os

def main():
    """Main function to run the dashboard."""
    print("📊 Starting Forex Trading Dashboard...")
    print("=" * 50)
    
    # Check if database exists
    if not os.path.exists('forex_trading.db'):
        print("⚠️  Warning: No trading database found.")
        print("   The dashboard will show empty data until the bot runs.")
        print("   Start the bot first with: python run_bot.py")
        print()
    
    try:
        # Start Streamlit dashboard
        print("🚀 Launching Streamlit dashboard...")
        print("📱 Dashboard will open in your browser automatically")
        print("🌐 Or visit: http://localhost:8501")
        print("💡 Press Ctrl+C to stop the dashboard")
        print("=" * 50)
        
        # Run Streamlit with the dashboard
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "dashboard.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ])
        
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Dashboard error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()