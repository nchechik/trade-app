#!/usr/bin/env python3
"""
Forex Trading Dashboard
Streamlit application that displays live trading data and account information.
Updates automatically every minute to show real-time trading status.
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
    page_title="Forex Trading Bot Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

class TradingDashboard:
    def __init__(self):
        """Initialize the trading dashboard."""
        self.db_path = 'forex_trading.db'
        self.update_interval = 60  # seconds
        
    def get_database_connection(self):
        """Create a connection to the SQLite database."""
        try:
            conn = sqlite3.connect(self.db_path)
            return conn
        except Exception as e:
            st.error(f"Database connection failed: {e}")
            return None
    
    def get_trades_data(self) -> pd.DataFrame:
        """Fetch all trades from the database."""
        conn = self.get_database_connection()
        if conn is None:
            return pd.DataFrame()
        
        try:
            query = """
                SELECT timestamp, pair, action, price, balance
                FROM trades
                WHERE pair != 'SYSTEM'
                ORDER BY timestamp DESC
            """
            df = pd.read_sql_query(query, conn)
            
            if not df.empty:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df['price'] = df['price'].round(5)
                df['balance'] = df['balance'].round(2)
            
            return df
        except Exception as e:
            st.error(f"Failed to fetch trades: {e}")
            return pd.DataFrame()
        finally:
            conn.close()
    
    def get_balances_data(self) -> pd.DataFrame:
        """Fetch balance history from the database."""
        conn = self.get_database_connection()
        if conn is None:
            return pd.DataFrame()
        
        try:
            query = """
                SELECT timestamp, balance
                FROM balances
                ORDER BY timestamp ASC
            """
            df = pd.read_sql_query(query, conn)
            
            if not df.empty:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df['balance'] = df['balance'].round(2)
            
            return df
        except Exception as e:
            st.error(f"Failed to fetch balances: {e}")
            return pd.DataFrame()
        finally:
            conn.close()
    
    def get_current_balance(self) -> float:
        """Get the most recent account balance."""
        conn = self.get_database_connection()
        if conn is None:
            return 0.0
        
        try:
            query = "SELECT balance FROM balances ORDER BY timestamp DESC LIMIT 1"
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchone()
            
            return float(result[0]) if result else 0.0
        except Exception as e:
            st.error(f"Failed to get current balance: {e}")
            return 0.0
        finally:
            conn.close()
    
    def calculate_summary_stats(self, trades_df: pd.DataFrame, balances_df: pd.DataFrame) -> dict:
        """Calculate summary statistics for the dashboard."""
        stats = {
            'total_trades': 0,
            'buy_trades': 0,
            'sell_trades': 0,
            'total_profit_loss': 0.0,
            'initial_balance': 0.0,
            'current_balance': 0.0
        }
        
        if not trades_df.empty:
            stats['total_trades'] = len(trades_df)
            stats['buy_trades'] = len(trades_df[trades_df['action'] == 'BUY'])
            stats['sell_trades'] = len(trades_df[trades_df['action'] == 'SELL'])
        
        if not balances_df.empty:
            stats['initial_balance'] = balances_df['balance'].iloc[0]
            stats['current_balance'] = balances_df['balance'].iloc[-1]
            stats['total_profit_loss'] = stats['current_balance'] - stats['initial_balance']
        
        return stats
    
    def create_balance_chart(self, balances_df: pd.DataFrame) -> go.Figure:
        """Create a line chart showing account balance over time."""
        if balances_df.empty:
            return go.Figure()
        
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
            title='Account Balance Over Time',
            xaxis_title='Time',
            yaxis_title='Balance (USD)',
            hovermode='x unified',
            template='plotly_white',
            height=400
        )
        
        return fig
    
    def create_trades_table(self, trades_df: pd.DataFrame) -> pd.DataFrame:
        """Format trades data for display in the table."""
        if trades_df.empty:
            return pd.DataFrame()
        
        # Format the dataframe for display
        display_df = trades_df.copy()
        display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
        display_df['price'] = display_df['price'].astype(str)
        display_df['balance'] = display_df['balance'].astype(str)
        
        # Rename columns for better display
        display_df.columns = ['Timestamp', 'Pair', 'Action', 'Price', 'Balance']
        
        return display_df
    
    def run_dashboard(self):
        """Main dashboard function."""
        st.title("📈 Forex Trading Bot Dashboard (Public API)")
        st.markdown("---")
        
        # Auto-refresh every minute
        if 'last_refresh' not in st.session_state:
            st.session_state.last_refresh = time.time()
        
        # Check if it's time to refresh
        if time.time() - st.session_state.last_refresh >= self.update_interval:
            st.session_state.last_refresh = time.time()
            st.rerun()
        
        # Sidebar for controls
        st.sidebar.header("Dashboard Controls")
        st.sidebar.info(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
        
        # Manual refresh button
        if st.sidebar.button("🔄 Refresh Now"):
            st.rerun()
        
        # Main content area
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📊 Account Overview")
            
            # Get data
            trades_df = self.get_trades_data()
            balances_df = self.get_balances_data()
            current_balance = self.get_current_balance()
            stats = self.calculate_summary_stats(trades_df, balances_df)
            
            # Display key metrics
            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
            
            with metric_col1:
                st.metric(
                    label="Current Balance",
                    value=f"${stats['current_balance']:,.2f}",
                    delta=f"${stats['total_profit_loss']:+,.2f}"
                )
            
            with metric_col2:
                st.metric(
                    label="Total Trades",
                    value=stats['total_trades']
                )
            
            with metric_col3:
                st.metric(
                    label="Buy Trades",
                    value=stats['buy_trades']
                )
            
            with metric_col4:
                st.metric(
                    label="Sell Trades",
                    value=stats['sell_trades']
                )
            
            # Balance chart
            st.subheader("💰 Balance History")
            balance_chart = self.create_balance_chart(balances_df)
            st.plotly_chart(balance_chart, use_container_width=True)
        
        with col2:
            st.subheader("📋 Recent Trades")
            
            if not trades_df.empty:
                # Show last 10 trades
                recent_trades = trades_df.head(10)
                display_trades = self.create_trades_table(recent_trades)
                
                st.dataframe(
                    display_trades,
                    use_container_width=True,
                    height=400
                )
                
                # Download button for all trades
                csv = trades_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download All Trades (CSV)",
                    data=csv,
                    file_name=f"forex_trades_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            else:
                st.info("No trades recorded yet. The bot may not be running or no trades have been executed.")
        
        # Full trades table at the bottom
        st.markdown("---")
        st.subheader("📊 Complete Trading History")
        
        if not trades_df.empty:
            full_display_trades = self.create_trades_table(trades_df)
            st.dataframe(
                full_display_trades,
                use_container_width=True,
                height=400
            )
        else:
            st.info("No trading history available.")
        
        # Footer
        st.markdown("---")
        st.markdown(
            """
            <div style='text-align: center; color: #666;'>
                <p>🤖 Forex Trading Bot Dashboard (Public API) | Auto-refreshes every minute</p>
                <p>Built with Streamlit and Python | No registration required</p>
            </div>
            """,
            unsafe_allow_html=True
        )

def main():
    """Main function to run the dashboard."""
    try:
        dashboard = TradingDashboard()
        dashboard.run_dashboard()
    except Exception as e:
        st.error(f"Dashboard error: {e}")
        st.exception(e)

if __name__ == "__main__":
    main()