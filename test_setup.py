#!/usr/bin/env python3
"""
Forex Trading Bot Setup Test
Test script to verify the project is properly configured.
"""

import sys
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
        'requests'
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

def test_public_api():
    """Test if the public Forex API is accessible."""
    print("\n🌐 Testing public Forex API...")
    
    try:
        import requests
        response = requests.get("https://api.exchangerate.host/latest?base=USD&symbols=EUR,GBP")
        response.raise_for_status()
        
        data = response.json()
        if 'rates' in data and 'EUR' in data['rates'] and 'GBP' in data['rates']:
            print("  ✅ Public API accessible")
            print(f"  ✅ EUR rate: {data['rates']['EUR']}")
            print(f"  ✅ GBP rate: {data['rates']['GBP']}")
            return True
        else:
            print("  ❌ API response format unexpected")
            return False
            
    except Exception as e:
        print(f"  ❌ API test failed: {e}")
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
    print("🚀 Forex Trading Bot Setup Test (Public API)")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_files),
        ("Module Imports", test_imports),
        ("Public Forex API", test_public_api),
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
        print("\n✅ No registration required - using free public Forex API!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please fix the issues above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())