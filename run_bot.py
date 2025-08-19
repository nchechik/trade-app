#!/usr/bin/env python3
"""
Forex Trading Bot Runner
Simple script to start the trading bot with proper error handling.
"""

import sys
import os
from bot import ForexTradingBot

def main():
    """Main function to run the trading bot."""
    print("🤖 Starting Forex Trading Bot...")
    print("=" * 50)
    
    # Check if environment variables are set
    if not os.getenv('OANDA_API_KEY') or not os.getenv('OANDA_ACCOUNT_ID'):
        print("❌ Error: OANDA_API_KEY and OANDA_ACCOUNT_ID must be set!")
        print("\nTo set them up:")
        print("1. Copy .env.example to .env")
        print("2. Edit .env with your OANDA credentials")
        print("3. Or export them in your terminal:")
        print("   export OANDA_API_KEY='your_api_key'")
        print("   export OANDA_ACCOUNT_ID='your_account_id'")
        print("\nGet credentials from: https://www.oanda.com/demo-account/")
        sys.exit(1)
    
    try:
        # Create and run the bot
        bot = ForexTradingBot()
        print("✅ Bot initialized successfully!")
        print("📊 Monitoring EUR/USD and GBP/USD")
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