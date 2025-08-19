#!/usr/bin/env python3
"""
Forex Trading Bot Setup Test
Test script to verify the project is properly configured.
"""

import sys
import os
import importlib
import sqlite3
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported."""
    print("🧪 Testing module imports...")
    
    required_modules = [
        'streamlit',
        'pandas', 
        'plotly',
        'requests',
        'dotenv'
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"  ✅ {module}")
        except ImportError:
            print(f"  ❌ {module}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✅ All modules imported successfully")
    return True

def test_environment():
    """Test if environment variables are set."""
    print("\n🔐 Testing environment variables...")
    
    api_key = os.getenv('OANDA_API_KEY')
    account_id = os.getenv('OANDA_ACCOUNT_ID')
    
    if api_key and account_id:
        print("  ✅ OANDA_API_KEY: Set")
        print("  ✅ OANDA_ACCOUNT_ID: Set")
        return True
    else:
        print("  ❌ OANDA_API_KEY: Not set")
        print("  ❌ OANDA_ACCOUNT_ID: Not set")
        print("\n💡 Set up your .env file with OANDA credentials")
        return False

def test_database():
    """Test database creation."""
    print("\n🗄️  Testing database...")
    
    try:
        # Test database connection
        conn = sqlite3.connect('forex_trading.db')
        cursor = conn.cursor()
        
        # Test table creation
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_table (
                id INTEGER PRIMARY KEY,
                test_value TEXT
            )
        ''')
        
        # Test insert
        cursor.execute('INSERT INTO test_table (test_value) VALUES (?)', ('test',))
        
        # Test select
        cursor.execute('SELECT test_value FROM test_table')
        result = cursor.fetchone()
        
        # Cleanup
        cursor.execute('DROP TABLE test_table')
        conn.commit()
        conn.close()
        
        print("  ✅ Database connection: Working")
        print("  ✅ Table operations: Working")
        return True
        
    except Exception as e:
        print(f"  ❌ Database test failed: {e}")
        return False

def test_files():
    """Test if all required files exist."""
    print("\n📁 Testing project files...")
    
    required_files = [
        'bot.py',
        'dashboard.py', 
        'requirements.txt',
        '.env.example',
        'README.md'
    ]
    
    missing_files = []
    
    for file in required_files:
        if Path(file).exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file}")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ All project files present")
    return True

def main():
    """Run all tests."""
    print("🚀 Forex Trading Bot Setup Test")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_files),
        ("Module Imports", test_imports),
        ("Environment Variables", test_environment),
        ("Database", test_database)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}")
        print("-" * 30)
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your project is ready to run.")
        print("\n🚀 To start the project:")
        print("   python start_project.py")
        print("\n📊 Or run components separately:")
        print("   python run_bot.py      # Trading bot")
        print("   python run_dashboard.py # Dashboard")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please fix the issues above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())