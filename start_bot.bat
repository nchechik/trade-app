@echo off
REM Forex Trading Bot Startup Script for Windows
REM This script installs dependencies and starts the trading bot system

echo 🚀 Starting Forex Trading Bot System...
echo ======================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not installed. Please install pip first.
    pause
    exit /b 1
)

echo ✅ Python and pip are available

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully

REM Check if .env file exists
if not exist .env (
    echo ⚠️  .env file not found. Creating from template...
    if exist .env.example (
        copy .env.example .env
        echo 📝 Please edit .env file with your OANDA credentials:
        echo    OANDA_API_KEY=your_api_key_here
        echo    OANDA_ACCOUNT_ID=your_account_id_here
        echo.
        echo Press any key after editing .env file to continue...
        pause >nul
    ) else (
        echo ❌ .env.example not found. Please create .env file manually.
        pause
        exit /b 1
    )
)

REM Start the system
echo 🚀 Launching trading bot and dashboard...
python launch.py

pause