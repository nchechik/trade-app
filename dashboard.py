#!/usr/bin/env python3
"""
Forex Trading Dashboard
Streamlit application that displays live trading data and account information.
Reads from the SQLite database created by the trading bot.
"""

import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import threading

# Page configuration
st.set_page_config(
    page_title="Forex Trading Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .trade-table {
        background-color: white;
        border-radius: 0.5rem;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

class TradingDashboard:
    def __init__(self):
        """Initialize the dashboard."""
        self.db_path = 'forex_trading.db'
        self.auto_refresh = True
        
    def get_database_connection(self):
        """Get a connection to the SQLite database."""
        try:
            conn = sqlite3.connect(self.db_path)
            return conn
        except Exception as e:
            st.error(f"Database connection failed: {e}")
            return None
    
    def get_trades_data(self):
        """Fetch all trades from the database."""
        conn = self.get_database_connection()
        if conn is None:
            return pd.DataFrame()
        
        try:
            query = """
                SELECT 
                    id,
                    timestamp,
                    pair,
                    action,
                    price,
                    balance
                FROM trades 
                ORDER BY timestamp DESC
            """
            df = pd.read_sql_query(query, conn)
            
            # Convert timestamp to datetime
            if not df.empty:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df['timestamp_formatted'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
            
            conn.close()
            return df
        except Exception as e:
            st.error(f"Failed to fetch trades: {e}")
            conn.close()
            return pd.DataFrame()
    
    def get_balances_data(self):
        """Fetch balance history from the database."""
        conn = self.get_database_connection()
        if conn is None:
            return pd.DataFrame()
        
        try:
            query = """
                SELECT 
                    timestamp,
                    balance
                FROM balances 
                ORDER BY timestamp ASC
            """
            df = pd.read_sql_query(query, conn)
            
            # Convert timestamp to datetime
            if not df.empty:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            conn.close()
            return df
        except Exception as e:
            st.error(f"Failed to fetch balances: {e}")
            conn.close()
            return pd.DataFrame()
    
    def get_current_balance(self):
        """Get the most recent account balance."""
        conn = self.get_database_connection()
        if conn is None:
            return None
        
        try:
            query = "SELECT balance FROM balances ORDER BY timestamp DESC LIMIT 1"
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchone()
            
            conn.close()
            return result[0] if result else None
        except Exception as e:
            st.error(f"Failed to get current balance: {e}")
            conn.close()
            return None
    
    def calculate_summary_stats(self, trades_df):
        """Calculate summary statistics from trades data."""
        if trades_df.empty:
            return {
                'total_trades': 0,
                'buy_trades': 0,
                'sell_trades': 0,
                'total_profit_loss': 0,
                'avg_price': 0
            }
        
        total_trades = len(trades_df)
        buy_trades = len(trades_df[trades_df['action'] == 'BUY'])
        sell_trades = len(trades_df[trades_df['action'] == 'SELL'])
        
        # Calculate profit/loss (simplified - assumes equal position sizes)
        if len(trades_df) >= 2:
            # Get initial and final balance
            initial_balance = trades_df.iloc[-1]['balance']
            final_balance = trades_df.iloc[0]['balance']
            total_profit_loss = final_balance - initial_balance
        else:
            total_profit_loss = 0
        
        avg_price = trades_df['price'].mean()
        
        return {
            'total_trades': total_trades,
            'buy_trades': buy_trades,
            'sell_trades': sell_trades,
            'total_profit_loss': total_profit_loss,
            'avg_price': avg_price
        }
    
    def create_balance_chart(self, balances_df):
        """Create a line chart showing account balance over time."""
        if balances_df.empty:
            st.warning("No balance data available yet.")
            return
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=balances_df['timestamp'],
            y=balances_df['balance'],
            mode='lines+markers',
            name='Account Balance',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title="Account Balance Over Time",
            xaxis_title="Time",
            yaxis_title="Balance ($)",
            hovermode='x unified',
            template='plotly_white',
            height=400
        )
        
        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1h", step="hour", stepmode="backward"),
                    dict(count=6, label="6h", step="hour", stepmode="backward"),
                    dict(count=1, label="1d", step="day", stepmode="backward"),
                    dict(count=7, label="1w", step="day", stepmode="backward"),
                    dict(step="all", label="All")
                ])
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def display_summary_metrics(self, current_balance, summary_stats):
        """Display summary metrics in a grid layout."""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Current Balance",
                value=f"${current_balance:.2f}" if current_balance else "$0.00",
                delta=f"{summary_stats['total_profit_loss']:.2f}" if summary_stats['total_profit_loss'] != 0 else "0.00"
            )
        
        with col2:
            st.metric(
                label="Total Trades",
                value=summary_stats['total_trades']
            )
        
        with col3:
            st.metric(
                label="Buy Trades",
                value=summary_stats['buy_trades']
            )
        
        with col4:
            st.metric(
                label="Sell Trades",
                value=summary_stats['sell_trades']
            )
    
    def display_trades_table(self, trades_df):
        """Display trades in a formatted table."""
        if trades_df.empty:
            st.info("No trades recorded yet. The bot will start logging trades once it begins trading.")
            return
        
        st.subheader("Recent Trades")
        
        # Format the trades data for display
        display_df = trades_df[['timestamp_formatted', 'pair', 'action', 'price', 'balance']].copy()
        display_df.columns = ['Timestamp', 'Pair', 'Action', 'Price', 'Balance']
        
        # Color code the action column
        def color_action(val):
            if val == 'BUY':
                return 'background-color: #d4edda; color: #155724;'
            elif val == 'SELL':
                return 'background-color: #f8d7da; color: #721c24;'
            else:
                return 'background-color: #fff3cd; color: #856404;'
        
        styled_df = display_df.style.applymap(
            color_action, subset=['Action']
        )
        
        st.dataframe(
            styled_df,
            use_container_width=True,
            height=400
        )
    
    def run(self):
        """Main dashboard execution."""
        # Header
        st.markdown('<h1 class="main-header">📈 Forex Trading Dashboard</h1>', unsafe_allow_html=True)
        
        # Sidebar controls
        st.sidebar.title("Dashboard Controls")
        self.auto_refresh = st.sidebar.checkbox("Auto-refresh every 60 seconds", value=True)
        
        if st.sidebar.button("Refresh Now"):
            st.rerun()
        
        # Status indicator
        st.sidebar.markdown("---")
        st.sidebar.subheader("Bot Status")
        
        # Check if database exists and has data
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='trades'")
            table_exists = cursor.fetchone() is not None
            conn.close()
            
            if table_exists:
                st.sidebar.success("✅ Database Connected")
                st.sidebar.success("✅ Bot Active")
            else:
                st.sidebar.warning("⚠️ Database Not Ready")
                st.sidebar.info("Bot needs to run first to create database")
        except:
            st.sidebar.error("❌ Database Error")
        
        # Main content
        try:
            # Get data
            trades_df = self.get_trades_data()
            balances_df = self.get_balances_data()
            current_balance = self.get_current_balance()
            summary_stats = self.calculate_summary_stats(trades_df)
            
            # Display summary metrics
            st.subheader("Account Summary")
            self.display_summary_metrics(current_balance, summary_stats)
            
            # Display balance chart
            st.subheader("Balance History")
            self.create_balance_chart(balances_df)
            
            # Display trades table
            self.display_trades_table(trades_df)
            
            # Auto-refresh functionality
            if self.auto_refresh:
                time.sleep(60)
                st.rerun()
                
        except Exception as e:
            st.error(f"Dashboard error: {e}")
            st.info("Make sure the trading bot is running and the database exists.")

def main():
    """Main entry point for the dashboard."""
    dashboard = TradingDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()