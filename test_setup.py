#!/usr/bin/env python3
"""
Test Setup Script
Verifies that all components of the Forex trading bot are working correctly.
"""

import sys
import os
import sqlite3
from datetime import datetime

def test_python_version():
    """Test Python version compatibility."""
    print("🐍 Testing Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.8+")
        return False

def test_dependencies():
    """Test if all required packages are installed."""
    print("\n📦 Testing dependencies...")
    
    required_packages = [
        'streamlit',
        'oandapyV20', 
        'pandas',
        'plotly',
        'dotenv'
    ]
    
    all_installed = True
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} - Installed")
        except ImportError:
            print(f"❌ {package} - Missing")
            all_installed = False
    
    return all_installed

def test_database_creation():
    """Test database creation and table structure."""
    print("\n🗄️ Testing database creation...")
    
    try:
        # Test database creation
        conn = sqlite3.connect('test_forex_trading.db')
        cursor = conn.cursor()
        
        # Create test tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                pair TEXT NOT NULL,
                action TEXT NOT NULL,
                price REAL NOT NULL,
                balance REAL NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_balances (
                timestamp TEXT PRIMARY KEY,
                balance REAL NOT NULL
            )
        ''')
        
        # Insert test data
        test_time = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO test_trades (timestamp, pair, action, price, balance)
            VALUES (?, ?, ?, ?, ?)
        ''', (test_time, 'EUR_USD', 'BUY', 1.1000, 10000.00))
        
        cursor.execute('''
            INSERT OR REPLACE INTO test_balances (timestamp, balance)
            VALUES (?, ?)
        ''', (test_time, 10000.00))
        
        # Test data retrieval
        cursor.execute('SELECT COUNT(*) FROM test_trades')
        trades_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM test_balances')
        balances_count = cursor.fetchone()[0]
        
        conn.commit()
        conn.close()
        
        # Clean up test database
        os.remove('test_forex_trading.db')
        
        if trades_count == 1 and balances_count == 1:
            print("✅ Database creation and operations - Working")
            return True
        else:
            print("❌ Database operations - Failed")
            return False
            
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_environment_variables():
    """Test environment variable loading."""
    print("\n🔐 Testing environment variables...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('OANDA_API_KEY')
        account_id = os.getenv('OANDA_ACCOUNT_ID')
        
        if api_key and account_id:
            if api_key == 'your_api_key_here' or account_id == 'your_account_id_here':
                print("⚠️  Environment variables set but using placeholder values")
                print("   Please update .env file with real OANDA credentials")
                return False
            else:
                print("✅ Environment variables - Configured with real values")
                return True
        else:
            print("❌ Environment variables - Missing or not loaded")
            return False
            
    except Exception as e:
        print(f"❌ Environment test failed: {e}")
        return False

def test_file_structure():
    """Test if all required files exist."""
    print("\n📁 Testing file structure...")
    
    required_files = [
        'bot.py',
        'dashboard.py', 
        'launch.py',
        'requirements.txt',
        '.env.example'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} - Found")
        else:
            print(f"❌ {file} - Missing")
            all_exist = False
    
    return all_exist

def main():
    """Run all tests."""
    print("🧪 Forex Trading Bot Setup Test")
    print("=" * 40)
    
    tests = [
        ("Python Version", test_python_version),
        ("Dependencies", test_dependencies),
        ("Database Operations", test_database_creation),
        ("Environment Variables", test_environment_variables),
        ("File Structure", test_file_structure)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 TEST SUMMARY")
    print("=" * 40)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your setup is ready.")
        print("🚀 Run 'python launch.py' to start the trading bot.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please fix the issues above.")
        
        if not any(name == "Environment Variables" and result for name, result in results):
            print("\n💡 Next steps:")
            print("1. Copy .env.example to .env")
            print("2. Add your OANDA API key and account ID to .env")
            print("3. Run this test again")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)