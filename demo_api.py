#!/usr/bin/env python3
"""
Forex Public API Demo
Simple script to demonstrate the public Forex API functionality.
"""

import urllib.request
import json
from datetime import datetime

def demo_public_api():
    """Demonstrate the public Forex API functionality."""
    print("🌐 Forex Public API Demo")
    print("=" * 50)
    
    # API endpoint
    api_url = "https://api.frankfurter.app/latest"
    
    try:
        print("📡 Fetching live exchange rates...")
        print(f"API: {api_url}")
        print()
        
        # Fetch USD rates for EUR and GBP
        url = f"{api_url}?from=USD&to=EUR,GBP"
        
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
        
        print("✅ API Response:")
        print(f"  Base Currency: {data.get('base', 'N/A')}")
        print(f"  Date: {data.get('date', 'N/A')}")
        print(f"  Amount: {data.get('amount', 'N/A')}")
        print()
        
        print("💱 Exchange Rates:")
        rates = data.get('rates', {})
        
        if 'EUR' in rates:
            print(f"  USD → EUR: {rates['EUR']:.5f}")
            print(f"  EUR → USD: {1/rates['EUR']:.5f}")
        
        if 'GBP' in rates:
            print(f"  USD → GBP: {rates['GBP']:.5f}")
            print(f"  GBP → USD: {1/rates['GBP']:.5f}")
        
        print()
        print("🎯 Trading Strategy Demo:")
        
        # Simulate price changes
        if 'EUR' in rates:
            eur_rate = rates['EUR']
            print(f"  Current EUR rate: {eur_rate:.5f}")
            
            # Simulate a small increase
            new_rate = eur_rate * 1.0006  # 0.06% increase
            change_pct = ((new_rate - eur_rate) / eur_rate) * 100
            
            print(f"  New EUR rate: {new_rate:.5f}")
            print(f"  Change: {change_pct:.3f}%")
            
            if change_pct > 0.05:
                print("  🟢 BUY signal (price increased >0.05%)")
            elif change_pct < -0.05:
                print("  🔴 SELL signal (price decreased >0.05%)")
            else:
                print("  🟡 HOLD (price change within threshold)")
        
        print()
        print("🚀 Ready to run the full trading bot!")
        print("  python3 run_simple.py")
        
    except urllib.error.URLError as e:
        print(f"❌ API request failed: {e}")
        print("Check your internet connection and try again.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    demo_public_api()