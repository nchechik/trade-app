#!/usr/bin/env python3
"""
Mobile-Friendly Forex Trading Dashboard
Web-based dashboard accessible from any device on your network.
Uses Python's built-in HTTP server - no external dependencies required.
"""

import sqlite3
import json
import time
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import threading
import os

class TradingDataHandler:
    def __init__(self):
        self.db_path = 'forex_trading.db'
    
    def get_trades_data(self):
        """Fetch all trades from the database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = """
                SELECT timestamp, pair, action, price, balance
                FROM trades
                WHERE pair != 'SYSTEM'
                ORDER BY timestamp DESC
                LIMIT 50
            """
            cursor.execute(query)
            trades = cursor.fetchall()
            
            result = []
            for trade in trades:
                result.append({
                    'timestamp': trade[0],
                    'pair': trade[1],
                    'action': trade[2],
                    'price': round(trade[3], 5),
                    'balance': round(trade[4], 2)
                })
            
            conn.close()
            return result
        except Exception as e:
            print(f"Error fetching trades: {e}")
            return []
    
    def get_balances_data(self):
        """Fetch balance history from the database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = """
                SELECT timestamp, balance
                FROM balances
                ORDER BY timestamp ASC
                LIMIT 100
            """
            cursor.execute(query)
            balances = cursor.fetchall()
            
            result = []
            for balance in balances:
                result.append({
                    'timestamp': balance[0],
                    'balance': round(balance[1], 2)
                })
            
            conn.close()
            return result
        except Exception as e:
            print(f"Error fetching balances: {e}")
            return []
    
    def get_summary_stats(self):
        """Calculate summary statistics."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get trade counts
            cursor.execute("SELECT COUNT(*) FROM trades WHERE pair != 'SYSTEM'")
            total_trades = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM trades WHERE action = 'BUY' AND pair != 'SYSTEM'")
            buy_trades = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM trades WHERE action = 'SELL' AND pair != 'SYSTEM'")
            sell_trades = cursor.fetchone()[0]
            
            # Get current balance
            cursor.execute("SELECT balance FROM balances ORDER BY timestamp DESC LIMIT 1")
            result = cursor.fetchone()
            current_balance = result[0] if result else 10000.0
            
            conn.close()
            
            return {
                'total_trades': total_trades,
                'buy_trades': buy_trades,
                'sell_trades': sell_trades,
                'current_balance': round(current_balance, 2),
                'total_profit_loss': round(current_balance - 10000.0, 2)
            }
        except Exception as e:
            print(f"Error calculating stats: {e}")
            return {}

class MobileDashboardHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.data_handler = TradingDataHandler()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        if path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.get_dashboard_html().encode())
        
        elif path == '/api/trades':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            trades = self.data_handler.get_trades_data()
            self.wfile.write(json.dumps(trades).encode())
        
        elif path == '/api/balances':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            balances = self.data_handler.get_balances_data()
            self.wfile.write(json.dumps(balances).encode())
        
        elif path == '/api/stats':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            stats = self.data_handler.get_summary_stats()
            self.wfile.write(json.dumps(stats).encode())
        
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')
    
    def get_dashboard_html(self):
        """Generate the mobile-friendly dashboard HTML."""
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📈 Forex Trading Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .header p {{
            font-size: 1.1rem;
            opacity: 0.9;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        
        .stat-value {{
            font-size: 2rem;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            color: #666;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .profit {{
            color: #10b981;
        }}
        
        .loss {{
            color: #ef4444;
        }}
        
        .content-grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 30px;
        }}
        
        @media (min-width: 768px) {{
            .content-grid {{
                grid-template-columns: 2fr 1fr;
            }}
        }}
        
        .section {{
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }}
        
        .section h2 {{
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.5rem;
            border-bottom: 2px solid #f0f0f0;
            padding-bottom: 10px;
        }}
        
        .trades-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        
        .trades-table th,
        .trades-table td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #f0f0f0;
        }}
        
        .trades-table th {{
            background: #f8f9fa;
            font-weight: 600;
            color: #495057;
        }}
        
        .action-buy {{
            color: #10b981;
            font-weight: bold;
        }}
        
        .action-sell {{
            color: #ef4444;
            font-weight: bold;
        }}
        
        .action-hold {{
            color: #6b7280;
        }}
        
        .refresh-info {{
            text-align: center;
            color: white;
            margin-top: 20px;
            opacity: 0.8;
        }}
        
        .loading {{
            text-align: center;
            padding: 20px;
            color: #666;
        }}
        
        .error {{
            background: #fef2f2;
            color: #dc2626;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📈 Forex Trading Dashboard</h1>
            <p>Live trading data from public Forex API</p>
        </div>
        
        <div class="stats-grid" id="stats-grid">
            <div class="loading">Loading statistics...</div>
        </div>
        
        <div class="content-grid">
            <div class="section">
                <h2>💰 Balance History</h2>
                <div id="balance-chart">
                    <div class="loading">Loading balance data...</div>
                </div>
            </div>
            
            <div class="section">
                <h2>📋 Recent Trades</h2>
                <div id="trades-table">
                    <div class="loading">Loading trades...</div>
                </div>
            </div>
        </div>
        
        <div class="refresh-info">
            <p>🔄 Auto-refreshes every 30 seconds | 📱 Mobile-friendly design</p>
            <p>Last updated: <span id="last-update">-</span></p>
        </div>
    </div>
    
    <script>
        // Chart.js for balance visualization
        let balanceChart = null;
        
        async function loadStats() {{
            try {{
                const response = await fetch('/api/stats');
                const stats = await response.json();
                
                const statsGrid = document.getElementById('stats-grid');
                statsGrid.innerHTML = `
                    <div class="stat-card">
                        <div class="stat-value">$${{stats.current_balance.toLocaleString()}}</div>
                        <div class="stat-label">Current Balance</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value ${{stats.total_profit_loss >= 0 ? 'profit' : 'loss'}}">
                            ${{stats.total_profit_loss >= 0 ? '+' : ''}}${{stats.total_profit_loss.toLocaleString()}}
                        </div>
                        <div class="stat-label">Total P&L</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${{stats.total_trades}}</div>
                        <div class="stat-label">Total Trades</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${{stats.buy_trades}} / ${{stats.sell_trades}}</div>
                        <div class="stat-label">Buy / Sell</div>
                    </div>
                `;
            }} catch (error) {{
                console.error('Error loading stats:', error);
            }}
        }}
        
        async function loadTrades() {{
            try {{
                const response = await fetch('/api/trades');
                const trades = await response.json();
                
                const tradesTable = document.getElementById('trades-table');
                if (trades.length === 0) {{
                    tradesTable.innerHTML = '<p>No trades recorded yet.</p>';
                    return;
                }}
                
                let tableHTML = `
                    <table class="trades-table">
                        <thead>
                            <tr>
                                <th>Time</th>
                                <th>Pair</th>
                                <th>Action</th>
                                <th>Price</th>
                                <th>Balance</th>
                            </tr>
                        </thead>
                        <tbody>
                `;
                
                trades.forEach(trade => {{
                    const time = new Date(trade.timestamp).toLocaleString();
                    const actionClass = trade.action === 'BUY' ? 'action-buy' : 
                                      trade.action === 'SELL' ? 'action-sell' : 'action-hold';
                    
                    tableHTML += `
                        <tr>
                            <td>${{time}}</td>
                            <td>${{trade.pair}}</td>
                            <td class="${{actionClass}}">${{trade.action}}</td>
                            <td>${{trade.price}}</td>
                            <td>$${{trade.balance.toLocaleString()}}</td>
                        </tr>
                    `;
                }});
                
                tableHTML += '</tbody></table>';
                tradesTable.innerHTML = tableHTML;
                
            }} catch (error) {{
                console.error('Error loading trades:', error);
                document.getElementById('trades-table').innerHTML = 
                    '<div class="error">Error loading trades. Please refresh the page.</div>';
            }}
        }}
        
        async function loadBalances() {{
            try {{
                const response = await fetch('/api/balances');
                const balances = await response.json();
                
                const balanceChart = document.getElementById('balance-chart');
                if (balances.length === 0) {{
                    balanceChart.innerHTML = '<p>No balance data available.</p>';
                    return;
                }}
                
                // Simple text-based balance display for now
                let chartHTML = '<div style="font-family: monospace; font-size: 14px;">';
                chartHTML += '<div style="margin-bottom: 15px;"><strong>Recent Balance Changes:</strong></div>';
                
                balances.slice(-10).reverse().forEach(balance => {{
                    const time = new Date(balance.timestamp).toLocaleString();
                    chartHTML += `<div>${{time}}: $${balance.balance.toLocaleString()}</div>`;
                }});
                
                chartHTML += '</div>';
                balanceChart.innerHTML = chartHTML;
                
            }} catch (error) {{
                console.error('Error loading balances:', error);
                document.getElementById('balance-chart').innerHTML = 
                    '<div class="error">Error loading balance data. Please refresh the page.</div>';
            }}
        }}
        
        function updateLastUpdate() {{
            document.getElementById('last-update').textContent = new Date().toLocaleString();
        }}
        
        async function refreshData() {{
            await Promise.all([
                loadStats(),
                loadTrades(),
                loadBalances()
            ]);
            updateLastUpdate();
        }}
        
        // Initial load
        refreshData();
        
        // Auto-refresh every 30 seconds
        setInterval(refreshData, 30000);
        
        // Refresh on page focus (useful for mobile)
        document.addEventListener('visibilitychange', () => {{
            if (!document.hidden) {{
                refreshData();
            }}
        }});
    </script>
</body>
</html>
        """

def run_mobile_dashboard(host='0.0.0.0', port=8080):
    """Run the mobile dashboard server."""
    server_address = (host, port)
    httpd = HTTPServer(server_address, MobileDashboardHandler)
    
    print("🚀 Mobile Forex Trading Dashboard Starting...")
    print("=" * 60)
    print(f"📱 Dashboard URL: http://{host}:{port}")
    print(f"🌐 Network Access: http://YOUR_IP:{port}")
    print("💡 Access from any device on your network!")
    print("🔄 Auto-refreshes every 30 seconds")
    print("=" * 60)
    
    try:
        print("✅ Dashboard running successfully!")
        print("📱 Open the URL above in your phone's browser")
        print("💡 Press Ctrl+C to stop")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
    finally:
        httpd.server_close()

if __name__ == "__main__":
    run_mobile_dashboard()