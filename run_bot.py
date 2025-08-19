#!/usr/bin/env python3
"""
Forex Trading Bot Runner
Simple script to start the trading bot with proper error handling.
"""

import sys
from bot import ForexTradingBot

def main():
    """Main function to run the trading bot."""
    print("🤖 Starting Forex Trading Bot...")
    print("=" * 50)
    
    try:
        # Create and run the bot
        bot = ForexTradingBot()
        print("✅ Bot initialized successfully!")
        print("📊 Monitoring EUR/USD and GBP/USD via public API")
        print("🔄 Running trading cycles every minute...")
        print("💡 Press Ctrl+C to stop the bot")
        print("=" * 50)
        
        bot.run()
        
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Bot error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()