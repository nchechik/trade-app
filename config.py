#!/usr/bin/env python3
"""
Configuration file for the Forex Trading Bot
Modify these settings to customize the bot's behavior
"""

# Trading Strategy Configuration
TRADING_CONFIG = {
    # Minimum price change threshold for trading (0.001 = 0.1%)
    'min_price_change': 0.001,
    
    # Cooldown period between trades in seconds
    'trade_cooldown': 60,
    
    # Currency pairs to trade
    'pairs': ["EUR_USD", "GBP_USD"],
    
    # Risk management - maximum trades per hour
    'max_trades_per_hour': 10,
    
    # Position size as percentage of account balance (0.01 = 1%)
    'position_size_percent': 0.01
}

# OANDA API Configuration
OANDA_CONFIG = {
    # Use practice environment (True) or live environment (False)
    'use_practice': True,
    
    # API request timeout in seconds
    'timeout': 30,
    
    # Maximum retries for failed API calls
    'max_retries': 3
}

# Database Configuration
DATABASE_CONFIG = {
    # Database file path
    'db_path': 'forex_trading.db',
    
    # How long to keep historical data (in days)
    'data_retention_days': 30,
    
    # Backup database before cleanup
    'backup_before_cleanup': True
}

# Dashboard Configuration
DASHBOARD_CONFIG = {
    # Auto-refresh interval in seconds
    'refresh_interval': 60,
    
    # Chart time range options (in hours)
    'chart_ranges': [1, 6, 24, 168],  # 1h, 6h, 1d, 1w
    
    # Number of recent trades to display
    'max_trades_display': 100,
    
    # Enable real-time price updates
    'live_price_updates': True
}

# Logging Configuration
LOGGING_CONFIG = {
    # Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
    'level': 'INFO',
    
    # Log file path
    'file_path': 'trading_bot.log',
    
    # Maximum log file size in MB
    'max_file_size': 10,
    
    # Number of backup log files to keep
    'backup_count': 5
}

# Performance Monitoring
PERFORMANCE_CONFIG = {
    # Enable performance metrics collection
    'enabled': True,
    
    # Metrics collection interval in seconds
    'collection_interval': 300,  # 5 minutes
    
    # Track execution time of trading cycles
    'track_execution_time': True,
    
    # Track memory usage
    'track_memory_usage': True
}

# Alert Configuration
ALERT_CONFIG = {
    # Enable email alerts (requires SMTP configuration)
    'email_alerts': False,
    
    # Enable console alerts
    'console_alerts': True,
    
    # Alert on significant balance changes (percentage)
    'balance_change_threshold': 0.05,  # 5%
    
    # Alert on consecutive losses
    'consecutive_loss_threshold': 3
}

# Development/Testing Configuration
DEV_CONFIG = {
    # Enable debug mode
    'debug_mode': False,
    
    # Simulate trades without executing them
    'paper_trading': False,
    
    # Use mock data for testing
    'use_mock_data': False,
    
    # Enable verbose logging
    'verbose_logging': False
}