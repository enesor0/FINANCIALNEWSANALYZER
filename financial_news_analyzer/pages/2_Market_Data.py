"""
Market Data Analysis Page
Latest available market-data visualization and price history
"""

import streamlit as st          # type: ignore
import pandas as pd # type: ignore
import plotly.express as px # type: ignore
import plotly.graph_objects as go  # type: ignore
from datetime import datetime, timedelta
import numpy as np
import sys
from pathlib import Path

repository_root = Path(__file__).resolve().parents[2]
if str(repository_root) not in sys.path:
    sys.path.insert(0, str(repository_root))

from financial_news_analyzer.src.infrastructure.services.yahoo_finance_service import (
    LiveDataUnavailable,
    YahooFinanceService,
)

# Page configuration
st.set_page_config(
    page_title="📈 Market Data",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def load_custom_css():
    """Load custom CSS for consistent styling"""
    st.markdown("""
    <style>
    /* Main theme colors - matching Start.py */
    :root {
        --primary-bg: #1a1a1a;
        --secondary-bg: #2c3e50;
        --tertiary-bg: #34495e;
        --accent-color: #00D4AA;
        --text-primary: #ffffff;
        --text-secondary: #bdc3c7;
        --border-color: #3a3a3a;
        --gradient-1: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        --gradient-2: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --gradient-3: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    /* Hide some Streamlit default elements but keep hamburger menu */
    footer {visibility: hidden;}
    
    /* Force hamburger button to be visible with smooth animation */
    button[title="View fullscreen"] {
        visibility: hidden;
    }
    
    /* Enhanced hamburger menu animation */
    button[data-testid="collapsedControl"] {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border-radius: 8px !important;
    }
    
    button[data-testid="collapsedControl"]:hover {
        transform: scale(1.1) rotate(5deg) !important;
        background-color: rgba(0, 212, 170, 0.1) !important;
        box-shadow: 0 4px 12px rgba(0, 212, 170, 0.3) !important;
    }
    
    button[data-testid="collapsedControl"]:active {
        transform: scale(0.95) !important;
        transition: all 0.1s ease-in-out !important;
    }
    
    /* Modern animations */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(0, 212, 170, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(0, 212, 170, 0); }
        100% { box-shadow: 0 0 0 0 rgba(0, 212, 170, 0); }
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 5px rgba(0, 212, 170, 0.3); }
        50% { box-shadow: 0 0 20px rgba(0, 212, 170, 0.8), 0 0 30px rgba(0, 212, 170, 0.4); }
    }
    
    @keyframes gradient-shift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    /* App background with animation */
    .stApp {
        background-color: var(--primary-bg) !important;
        color: var(--text-primary);
        animation: fadeInUp 0.8s ease-out;
    }
    
    .main .block-container {
        background: var(--primary-bg) !important;
        color: var(--text-primary);
        padding: 2rem;
        border-radius: 15px;
        margin-top: 1rem;
        animation: fadeInUp 1s ease-out;
    }
    
    /* Custom cards with animations */
    .metric-card {
        background: var(--gradient-1);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        margin: 10px 0;
        color: var(--text-primary);
        animation: slideInLeft 0.6s ease-out;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0, 212, 170, 0.2);
        animation: glow 2s infinite;
    }
    
    .price-up {
        border-left: 4px solid #00D4AA;
        background: linear-gradient(135deg, #2c3e50 0%, rgba(0, 212, 170, 0.1) 100%);
    }
    
    .price-down {
        border-left: 4px solid #FF6B6B;
        background: linear-gradient(135deg, #2c3e50 0%, rgba(255, 107, 107, 0.1) 100%);
    }
    
    .price-stable {
        border-left: 4px solid #4ECDC4;
        background: linear-gradient(135deg, #2c3e50 0%, rgba(78, 205, 196, 0.1) 100%);
    }
    
    /* Animated gradient text */
    .gradient-text {
        background: var(--gradient-2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 30px;
        background-size: 200% 200%;
        animation: gradient-shift 3s ease-in-out infinite, slideInRight 1s ease-out;
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }
    
    .status-active { background-color: #00D4AA; }
    .status-warning { background-color: #FFA726; }
    .status-error { background-color: #FF6B6B; }
    
    /* Custom buttons with enhanced smooth transitions */
    .stButton > button {
        background: var(--gradient-1);
        color: white;
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 12px 30px;
        font-weight: 600;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 8px 25px rgba(0, 212, 170, 0.3);
        background: var(--tertiary-bg);
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(1.01);
        transition: all 0.1s ease-in-out;
    }
    
    /* Sidebar - only background styling, allow native Streamlit behavior with smooth transitions */
    section[data-testid="stSidebar"] > div {
        background: linear-gradient(180deg, var(--primary-bg) 0%, var(--secondary-bg) 100%) !important;
        color: var(--text-primary) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    /* Enhanced sidebar animations */
    section[data-testid="stSidebar"] {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    /* Smooth animations for sidebar elements */
    section[data-testid="stSidebar"] * {
        transition: opacity 0.2s ease-in-out, transform 0.2s ease-in-out !important;
    }
    
    /* Enhanced hover effects for sidebar elements */
    section[data-testid="stSidebar"] .stSelectbox:hover,
    section[data-testid="stSidebar"] .stMultiSelect:hover,
    section[data-testid="stSidebar"] .stButton:hover {
        transform: translateX(2px);
        transition: transform 0.2s ease-in-out;
    }
    
    /* Smooth scroll for sidebar */
    section[data-testid="stSidebar"] {
        scroll-behavior: smooth !important;
    }
    
    /* Fade in animation for sidebar content */
    section[data-testid="stSidebar"] .element-container {
        animation: fadeInLeft 0.5s ease-out !important;
    }
    
    @keyframes fadeInLeft {
        from { 
            opacity: 0; 
            transform: translateX(-20px); 
        }
        to { 
            opacity: 1; 
            transform: translateX(0); 
        }
    }
    
    /* Sidebar text handling with smooth animations */
    .sidebar-content {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        font-size: 0.85rem;
        line-height: 1.2;
        transition: all 0.2s ease-in-out;
    }
    
    .sidebar-content:hover {
        opacity: 0.8;
        transform: scale(1.02);
    }
    
    /* Multiselect and selectbox styling with smooth transitions */
    .stSelectbox label, .stMultiSelect label {
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        color: var(--text-primary) !important;
        white-space: nowrap !important;
        transition: color 0.2s ease-in-out !important;
    }
    
    .stSelectbox > div > div, .stMultiSelect > div > div {
        min-width: 300px !important;
        font-size: 0.85rem !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border-radius: 8px !important;
    }
    
    .stSelectbox > div > div:hover, .stMultiSelect > div > div:hover {
        box-shadow: 0 4px 12px rgba(0, 212, 170, 0.2) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Chart containers */
    .chart-container {
        background: var(--gradient-1);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    /* Price change indicators */
    .price-change-positive {
        color: #00D4AA;
        font-weight: bold;
    }
    
    .price-change-negative {
        color: #FF6B6B;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

def get_company_database():
    """Get comprehensive company database with categories and symbols"""
    return {
        'Technology': {
            'Apple': 'AAPL', 'Microsoft': 'MSFT', 'Google': 'GOOGL', 'Amazon': 'AMZN', 'Meta': 'META', 
            'Netflix': 'NFLX', 'NVIDIA': 'NVDA', 'Adobe': 'ADBE', 'Salesforce': 'CRM', 'Oracle': 'ORCL',
            'IBM': 'IBM', 'Intel': 'INTC', 'AMD': 'AMD', 'Qualcomm': 'QCOM', 'Broadcom': 'AVGO', 
            'Texas Instruments': 'TXN', 'Applied Materials': 'AMAT', 'Micron': 'MU', 'Cisco Systems': 'CSCO',
            'VMware': 'VMW', 'ServiceNow': 'NOW', 'Snowflake': 'SNOW', 'CrowdStrike': 'CRWD', 'Zoom': 'ZM',
            'Slack': 'WORK', 'Dropbox': 'DBX', 'Box': 'BOX', 'Atlassian': 'TEAM', 'Splunk': 'SPLK',
            'Palantir': 'PLTR', 'Unity': 'U', 'Roblox': 'RBLX', 'Shopify': 'SHOP', 'Square': 'SQ',
            'PayPal': 'PYPL', 'Twilio': 'TWLO', 'MongoDB': 'MDB', 'Datadog': 'DDOG', 'Okta': 'OKTA'
        },
        'Finance': {
            'JPMorgan Chase': 'JPM', 'Bank of America': 'BAC', 'Wells Fargo': 'WFC', 'Citigroup': 'C',
            'Goldman Sachs': 'GS', 'Morgan Stanley': 'MS', 'American Express': 'AXP', 'Visa': 'V',
            'Mastercard': 'MA', 'BlackRock': 'BLK', 'Charles Schwab': 'SCHW', 'Berkshire Hathaway': 'BRK.A',
            'Progressive': 'PGR', 'Allstate': 'ALL', 'Travelers': 'TRV', 'AIG': 'AIG', 'MetLife': 'MET',
            'Prudential': 'PRU', 'Aflac': 'AFL', 'Capital One': 'COF', 'Discover': 'DIS', 'Coinbase': 'COIN'
        },
        'Healthcare': {
            'Johnson & Johnson': 'JNJ', 'Pfizer': 'PFE', 'UnitedHealth': 'UNH', 'Merck': 'MRK',
            'AbbVie': 'ABBV', 'Bristol Myers Squibb': 'BMY', 'Eli Lilly': 'LLY', 'Amgen': 'AMGN',
            'Gilead Sciences': 'GILD', 'Regeneron': 'REGN', 'Vertex Pharmaceuticals': 'VRTX', 'Biogen': 'BIIB',
            'Moderna': 'MRNA', 'Abbott Laboratories': 'ABT', 'Danaher': 'DHR', 'Thermo Fisher Scientific': 'TMO',
            'Intuitive Surgical': 'ISRG', 'Medtronic': 'MDT', 'Boston Scientific': 'BSX', 'Stryker': 'SYK'
        },
        'Energy': {
            'ExxonMobil': 'XOM', 'Chevron': 'CVX', 'ConocoPhillips': 'COP', 'EOG Resources': 'EOG',
            'Pioneer Natural Resources': 'PXD', 'Schlumberger': 'SLB', 'Halliburton': 'HAL', 'Baker Hughes': 'BKR',
            'Kinder Morgan': 'KMI', 'NextEra Energy': 'NEE', 'Duke Energy': 'DUK', 'Southern Company': 'SO',
            'Tesla Energy': 'TSLA', 'First Solar': 'FSLR', 'SunPower': 'SPWR', 'Enphase Energy': 'ENPH'
        },
        'Consumer': {
            'Walmart': 'WMT', 'Target': 'TGT', 'Home Depot': 'HD', 'Lowes': 'LOW', 'Costco': 'COST',
            'Best Buy': 'BBY', 'Macys': 'M', 'TJX Companies': 'TJX', 'Dollar General': 'DG', 'CVS Health': 'CVS',
            'Walgreens': 'WBA', 'Coca-Cola': 'KO', 'PepsiCo': 'PEP', 'Procter & Gamble': 'PG',
            'Nike': 'NKE', 'Starbucks': 'SBUX', 'McDonald\'s': 'MCD', 'Disney': 'DIS'
        },
        'Automotive': {
            'Tesla': 'TSLA', 'Ford': 'F', 'General Motors': 'GM', 'Toyota': 'TM', 'Honda': 'HMC',
            'Ferrari': 'RACE', 'Lucid Motors': 'LCID', 'Rivian': 'RIVN', 'NIO': 'NIO', 'XPeng': 'XPEV',
            'Li Auto': 'LI', 'BYD': 'BYDDY'
        },
        'Real Estate': {
            'American Tower': 'AMT', 'Prologis': 'PLD', 'Crown Castle': 'CCI', 'Equinix': 'EQIX',
            'Public Storage': 'PSA', 'Realty Income': 'O', 'Simon Property Group': 'SPG', 'CBRE Group': 'CBRE',
            'Zillow': 'ZG', 'Redfin': 'RDFN'
        },
        'Industrial': {
            'Boeing': 'BA', 'Lockheed Martin': 'LMT', 'Raytheon': 'RTX', 'Northrop Grumman': 'NOC',
            'General Electric': 'GE', 'Caterpillar': 'CAT', 'Deere & Company': 'DE', '3M Company': 'MMM',
            'Honeywell': 'HON', 'Waste Management': 'WM', 'Republic Services': 'RSG'
        }
    }

def generate_market_data():
    """Generate comprehensive market data for all companies"""
    company_db = get_company_database()
    
    # Set seed for consistent data generation
    np.random.seed(42)
    
    # Flatten the database to get all companies and symbols
    all_stocks = []
    for category, companies in company_db.items():
        for company, symbol in companies.items():
            all_stocks.append((symbol, company, category))
    
    # Generate data for ALL companies (not just a subset)
    data = []
    for symbol, company, category in all_stocks:
        
        # Generate realistic price ranges based on category
        if category == 'Technology':
            base_price = np.random.uniform(50, 800)
        elif category == 'Finance':
            base_price = np.random.uniform(30, 400)
        elif category == 'Healthcare':
            base_price = np.random.uniform(40, 600)
        elif category == 'Energy':
            base_price = np.random.uniform(20, 300)
        elif category == 'Consumer':
            base_price = np.random.uniform(25, 500)
        elif category == 'Automotive':
            base_price = np.random.uniform(15, 400)
        elif category == 'Real Estate':
            base_price = np.random.uniform(10, 200)
        else:  # Industrial
            base_price = np.random.uniform(20, 350)
        
        change_pct = np.random.uniform(-10, 10)
        change_amount = base_price * (change_pct / 100)
        
        # Generate market cap based on company type
        market_cap = np.random.uniform(1, 3000)  # Billions
        
        # Generate volume based on market cap (larger companies = higher volume)
        volume = int(np.random.uniform(100000, 50000000) * (market_cap / 1000))
        
        data.append({
            'Symbol': symbol,
            'Company': company,
            'Category': category,
            'Price': round(base_price, 2),
            'Change': round(change_amount, 2),
            'Change_Pct': round(change_pct, 2),
            'Market_Cap': round(market_cap, 2),
            'Volume': volume,
            'Day_High': round(base_price * np.random.uniform(1.01, 1.08), 2),
            'Day_Low': round(base_price * np.random.uniform(0.92, 0.99), 2),
            'High_52w': round(base_price * np.random.uniform(1.1, 2.0), 2),
            'Low_52w': round(base_price * np.random.uniform(0.3, 0.9), 2),
            'PE_Ratio': round(np.random.uniform(8, 50), 2),
            'Dividend_Yield': round(np.random.uniform(0, 8), 2)
        })
    
    # Reset seed
    np.random.seed(None)
    
    return pd.DataFrame(data)

def generate_historical_data(symbol, days=365):
    """Generate historical price data for a symbol"""
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    
    # Generate realistic price movement
    base_price = np.random.uniform(100, 300)
    prices = [base_price]
    
    for i in range(1, days):
        # Random walk with slight upward bias
        change = np.random.normal(0.001, 0.02)  # 0.1% average daily growth, 2% volatility
        new_price = prices[-1] * (1 + change)
        prices.append(max(new_price, 10))  # Ensure price doesn't go below $10
    
    # Calculate other OHLC data
    data = []
    for i, (date, price) in enumerate(zip(dates, prices)):
        daily_volatility = np.random.uniform(0.005, 0.03)
        high = price * (1 + daily_volatility)
        low = price * (1 - daily_volatility)
        
        # Ensure OHLC relationships are maintained
        open_price = np.random.uniform(low, high)
        close_price = price
        
        data.append({
            'Date': date,
            'Open': round(open_price, 2),
            'High': round(high, 2),
            'Low': round(low, 2),
            'Close': round(close_price, 2),
            'Volume': np.random.randint(1000000, 50000000)
        })
    
    return pd.DataFrame(data)


def get_live_universe():
    """Return a balanced, bounded symbol set for the live market overview."""
    instruments = []
    for category, companies in get_company_database().items():
        instruments.extend((symbol, company, category) for company, symbol in list(companies.items())[:5])
    return instruments


@st.cache_data(ttl=300, show_spinner=False)
def load_live_market_data(instruments):
    """Cache provider responses briefly to reduce network calls and rate limiting."""
    return YahooFinanceService.get_market_snapshot(instruments)


@st.cache_data(ttl=300, show_spinner=False)
def load_live_history(symbol, days):
    """Cache a symbol history for the same refresh window as the snapshot."""
    return YahooFinanceService.get_history(symbol, days)

def create_market_overview_chart(df):
    """Create market overview chart"""
    # Sort by market cap for better visualization
    df_sorted = df.sort_values('Market_Cap', ascending=True)
    
    fig = go.Figure()
    
    # Color based on price change
    colors = ['#00D4AA' if change > 0 else '#FF6B6B' if change < 0 else '#4ECDC4' 
              for change in df_sorted['Change_Pct']]
    
    fig.add_trace(go.Bar(
        x=df_sorted['Symbol'],
        y=df_sorted['Change_Pct'],
        marker_color=colors,
        text=[f"{pct:+.1f}%" for pct in df_sorted['Change_Pct']],
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>' +
                      'Change: %{y:.2f}%<br>' +
                      '<extra></extra>'
    ))
    
    fig.update_layout(
        title="Market Overview - Daily Performance",
        xaxis_title="Stock Symbol",
        yaxis_title="Change (%)",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=False
    )
    
    # Add zero line
    fig.add_hline(y=0, line_dash="dash", line_color="white", opacity=0.5)
    
    return fig

def create_price_chart(df_historical, symbol):
    """Create candlestick price chart"""
    fig = go.Figure(data=go.Candlestick(
        x=df_historical['Date'],
        open=df_historical['Open'],
        high=df_historical['High'],
        low=df_historical['Low'],
        close=df_historical['Close'],
        increasing_line_color='#00D4AA',
        decreasing_line_color='#FF6B6B',
        name=symbol
    ))
    
    # Add moving averages
    df_historical['MA20'] = df_historical['Close'].rolling(window=20).mean()
    df_historical['MA50'] = df_historical['Close'].rolling(window=50).mean()
    
    fig.add_trace(go.Scatter(
        x=df_historical['Date'],
        y=df_historical['MA20'],
        mode='lines',
        name='MA20',
        line=dict(color='#FFA726', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=df_historical['Date'],
        y=df_historical['MA50'],
        mode='lines',
        name='MA50',
        line=dict(color='#42A5F5', width=2)
    ))
    
    fig.update_layout(
        title=f"{symbol} - Price Chart with Moving Averages",
        xaxis_title="Date",
        yaxis_title="Price ($)",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis_rangeslider_visible=False
    )
    
    return fig

def create_volume_chart(df_historical):
    """Create volume chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_historical['Date'],
        y=df_historical['Volume'],
        marker_color='#4ECDC4',
        opacity=0.7,
        name='Volume'
    ))
    
    fig.update_layout(
        title="Trading Volume",
        xaxis_title="Date",
        yaxis_title="Volume",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=False
    )
    
    return fig

def create_correlation_heatmap(df):
    """Create correlation heatmap for selected metrics"""
    # Select numeric columns for correlation
    numeric_cols = ['Price', 'Change_Pct', 'Volume', 'Market_Cap', 'PE_Ratio']
    correlation_matrix = df[numeric_cols].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        text=correlation_matrix.values,
        texttemplate='%{text:.2f}',
        textfont=dict(color='white'),
        hoverongaps=False
    ))
    
    fig.update_layout(
        title="Market Metrics Correlation",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    return fig

def main():
    """Main function for Market Data page"""
    load_custom_css()
    
    # Header - matching Start.py design
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2c3e50 100%); 
                color: #ffffff; padding: 2.5rem; border-radius: 12px; text-align: center; 
                margin-bottom: 2rem; box-shadow: 0 6px 20px rgba(0,0,0,0.4); 
                border: 1px solid #3a3a3a;">
        <h1 style="margin: 0; font-size: 3rem; font-weight: 700; color: #ffffff;">
            📈 Market Data Analysis
        </h1>
        <h3 style="font-weight: 300; font-size: 1.5rem; color: #bdc3c7; margin: 1rem 0;">
            Latest Available Market Data and Price History
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Live provider data. We intentionally do not fall back to random values:
    # a missing provider must be visible to the user instead of looking real.
    if st.sidebar.button("↻ Refresh live data", use_container_width=True):
        load_live_market_data.clear()
        load_live_history.clear()
        st.rerun()

    try:
        with st.spinner("Loading latest available market prices..."):
            market_df = load_live_market_data(tuple(get_live_universe()))
    except LiveDataUnavailable as exc:
        st.error(f"Live market data is currently unavailable: {exc}")
        st.info("No simulated prices are shown. Try refreshing in a few minutes.")
        return

    st.caption(
        "Live data source: Yahoo Finance via yfinance. Values are the latest available daily close "
        "and may be delayed; not investment advice."
    )
    
    # Sidebar controls
    st.sidebar.header("📊 Market Controls")
    
    # Global company search
    st.sidebar.markdown("### 🔍 Company Search")
    search_term = st.sidebar.text_input(
        "Search companies",
        placeholder="Type any company name (IBM, Apple, Tesla...)",
        help="Search across all companies and symbols"
    )
    
    # Filter data by search
    if search_term:
        search_mask = (
            market_df['Company'].str.contains(search_term, case=False, na=False) |
            market_df['Symbol'].str.contains(search_term, case=False, na=False)
        )
        search_results_df = market_df[search_mask]
        st.sidebar.info(f"🎯 Found {len(search_results_df)} companies matching '{search_term}'")
        
        if not search_results_df.empty:
            # Show specific company selection from search results
            searched_companies = st.sidebar.multiselect(
                "Select from search results",
                options=search_results_df['Company'].tolist(),
                default=[],
                help="Choose specific companies from search results"
            )
            
            if searched_companies:
                filtered_market_df = market_df[market_df['Company'].isin(searched_companies)]
            else:
                filtered_market_df = search_results_df
        else:
            st.sidebar.warning("No companies found. Try different keywords.")
            filtered_market_df = pd.DataFrame()  # Empty dataframe
    else:
        # Category filter when not searching
        st.sidebar.markdown("### 🏢 Browse by Industry")
        company_db = get_company_database()
        categories = list(company_db.keys())
        selected_categories = st.sidebar.multiselect(
            "Industries",
            options=categories,
            default=categories[:3],
            help="Select industry sectors to analyze"
        )
        
        # Filter market data by selected categories
        if selected_categories:
            filtered_market_df = market_df[market_df['Category'].isin(selected_categories)]
        else:
            filtered_market_df = market_df
    
    # Market cap filter
    with st.sidebar.expander("💰 Market Cap"):
        min_cap, max_cap = st.slider(
            "Range (Billions)",
            min_value=0.0,
            max_value=5000.0,
            value=(0.0, 5000.0),
            step=10.0
        )
        market_cap = pd.to_numeric(filtered_market_df['Market_Cap'], errors='coerce')
        filtered_market_df = filtered_market_df[
            market_cap.isna() | ((market_cap >= min_cap) & (market_cap <= max_cap))
        ]
    
    # Performance filter
    with st.sidebar.expander("📊 Performance"):
        min_change, max_change = st.slider(
            "Change Range (%)",
            min_value=-20.0,
            max_value=20.0,
            value=(-20.0, 20.0),
            step=0.5
        )
        filtered_market_df = filtered_market_df[
            (filtered_market_df['Change_Pct'] >= min_change) & 
            (filtered_market_df['Change_Pct'] <= max_change)
        ]
    
    # Data validation and user feedback
    if filtered_market_df.empty:
        st.error("🚫 No companies found with current filters!")
        st.markdown("""
        ### 💡 Suggestions:
        - **Clear search** and try different keywords
        - **Select more industries** for broader results
        - **Expand filter ranges** (market cap, performance)
        - **Reset all filters** using sidebar options
        """)
        
        # Quick reset button
        if st.button("🔄 Reset All Filters", type="primary", use_container_width=True):
            st.rerun()
        
        return  # Exit early if no data
    
    # Show data summary
    st.sidebar.markdown("### 📈 Current Results")
    st.sidebar.info(f"""
    **Total Companies:** {len(filtered_market_df)}  
    **Industries:** {len(filtered_market_df['Category'].unique())}  
    **Price Range:** ${filtered_market_df['Price'].min():.2f} - ${filtered_market_df['Price'].max():.2f}
    """)
    
    # Quick stats in sidebar
    avg_change = filtered_market_df['Change_Pct'].mean()
    if avg_change > 0:
        trend_emoji = "📈"
        trend_color = "🟢"
    else:
        trend_emoji = "📉" 
        trend_color = "🔴"
    
    st.sidebar.markdown(f"""
    **Market Trend:** {trend_color} {trend_emoji}  
    **Average Change:** {avg_change:.2f}%
    """)
    
    # Stock selector for detailed analysis
    available_stocks = filtered_market_df['Symbol'].tolist()
    if available_stocks:
        selected_stock = st.sidebar.selectbox(
            "📈 Stock Analysis",
            options=available_stocks,
            index=0
        )
    else:
        st.sidebar.error("No stocks match the selected criteria")
        selected_stock = market_df['Symbol'].iloc[0]
    
    # Time period selector
    time_period = st.sidebar.selectbox(
        "📊 Time Period",
        options=["1 Month", "3 Months", "6 Months", "1 Year"],
        index=3
    )
    
    # Convert time period to days
    period_days = {"1 Month": 30, "3 Months": 90, "6 Months": 180, "1 Year": 365}
    days = period_days[time_period]
    
    # Retrieve actual OHLCV history for the selected instrument.
    try:
        historical_df = load_live_history(selected_stock, days)
    except LiveDataUnavailable as exc:
        st.warning(f"Historical data is unavailable for {selected_stock}: {exc}")
        historical_df = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
    
    # Market overview metrics
    st.subheader("🌍 Market Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        gainers = len(filtered_market_df[filtered_market_df['Change_Pct'] > 0])
        st.markdown(f"""
        <div class="metric-card price-up">
            <h3>📈 Gainers</h3>
            <h2>{gainers}</h2>
            <p>Stocks up today</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        losers = len(filtered_market_df[filtered_market_df['Change_Pct'] < 0])
        st.markdown(f"""
        <div class="metric-card price-down">
            <h3>📉 Losers</h3>
            <h2>{losers}</h2>
            <p>Stocks down today</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_change = round(filtered_market_df['Change_Pct'].mean(), 2)
        status_class = "price-up" if avg_change > 0 else "price-down" if avg_change < 0 else "price-stable"
        st.markdown(f"""
        <div class="metric-card {status_class}">
            <h3>📊 Avg Change</h3>
            <h2>{avg_change}%</h2>
            <p>Market average</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        total_volume = filtered_market_df['Volume'].sum() / 1_000_000  # Convert to millions
        st.markdown(f"""
        <div class="metric-card price-stable">
            <h3>📊 Total Volume</h3>
            <h2>{total_volume:.0f}M</h2>
            <p>Shares traded</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Market overview chart
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.plotly_chart(create_market_overview_chart(filtered_market_df), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Stock analysis section
    st.subheader(f"🔍 {selected_stock} Analysis")
    
    # Stock metrics
    stock_data = market_df[market_df['Symbol'] == selected_stock].iloc[0]
    market_cap_display = "N/A" if pd.isna(stock_data['Market_Cap']) else f"${stock_data['Market_Cap']:.2f}B"
    pe_ratio_display = "N/A" if pd.isna(stock_data['PE_Ratio']) else f"{stock_data['PE_Ratio']:.2f}"
    day_high_display = "N/A" if pd.isna(stock_data['Day_High']) else f"${stock_data['Day_High']:.2f}"
    day_low_display = "N/A" if pd.isna(stock_data['Day_Low']) else f"${stock_data['Day_Low']:.2f}"
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        change_class = "price-up" if stock_data['Change'] > 0 else "price-down"
        st.markdown(f"""
        <div class="metric-card {change_class}">
            <h4>Current Price</h4>
            <h3>${stock_data['Price']}</h3>
            <p class="{'price-change-positive' if stock_data['Change'] > 0 else 'price-change-negative'}">
                {stock_data['Change']:+.2f} ({stock_data['Change_Pct']:+.2f}%)
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Market Cap</h4>
            <h3>{market_cap_display}</h3>
            <p>Not supplied by snapshot</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h4>P/E Ratio</h4>
            <h3>{pe_ratio_display}</h3>
            <p>Not supplied by snapshot</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Day High</h4>
            <h3>{day_high_display}</h3>
            <p>Today's high</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Day Low</h4>
            <h3>{day_low_display}</h3>
            <p>Today's low</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Price and volume charts
    col1, col2 = st.columns([2, 1])
    
    if historical_df.empty:
        st.info("No historical chart is available for the selected instrument.")
    else:
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.plotly_chart(create_price_chart(historical_df, selected_stock), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.plotly_chart(create_volume_chart(historical_df), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Market analysis
    st.subheader("📊 Market Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(create_correlation_heatmap(market_df), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Top performers table
        st.markdown("### 🏆 Top Performers")
        top_performers = filtered_market_df.nlargest(5, 'Change_Pct')[['Symbol', 'Company', 'Category', 'Change_Pct', 'Price']]
        st.dataframe(top_performers, use_container_width=True)
        
        st.markdown("### 📉 Worst Performers")
        worst_performers = filtered_market_df.nsmallest(5, 'Change_Pct')[['Symbol', 'Company', 'Category', 'Change_Pct', 'Price']]
        st.dataframe(worst_performers, use_container_width=True)
    
    # Market data table with category info
    st.subheader("📋 Complete Market Data")
    
    # Show filtered data summary
    st.info(f"Showing {len(filtered_market_df)} stocks from {len(selected_categories)} categories")
    
    # Display comprehensive market data
    display_columns = ['Symbol', 'Company', 'Category', 'Price', 'Change', 'Change_Pct', 
                      'Day_High', 'Day_Low', 'Volume', 'Market_Cap', 'PE_Ratio', 'Dividend_Yield']
    st.dataframe(
        filtered_market_df[display_columns].sort_values('Market_Cap', ascending=False),
        use_container_width=True,
        height=400
    )
    
    # Add refresh button
    if st.button("🔄 Refresh Data"):
        st.rerun()
    
    # Broker Links Section
    st.markdown("---")
    st.markdown("## 🏦 Trusted Brokers & Trading Platforms")
    
    # Global Brokers
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🌍 Global Brokers")
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 15px;
            margin: 10px 0;
            animation: slideInLeft 0.8s ease-out;
        ">
            <h4 style="color: white; margin: 0 0 15px 0;">🇺🇸 United States</h4>
            <div style="margin-bottom: 10px;">
                <a href="https://www.interactivebrokers.com" target="_blank" style="color: #00D4AA; text-decoration: none; font-weight: 600;">
                    📊 Interactive Brokers
                </a>
                <p style="color: #ddd; margin: 5px 0; font-size: 0.9rem;">Low-cost global trading platform</p>
            </div>
            <div style="margin-bottom: 10px;">
                <a href="https://www.fidelity.com" target="_blank" style="color: #00D4AA; text-decoration: none; font-weight: 600;">
                    🏛️ Fidelity Investments
                </a>
                <p style="color: #ddd; margin: 5px 0; font-size: 0.9rem;">No commission stock trading</p>
            </div>
            <div style="margin-bottom: 10px;">
                <a href="https://www.schwab.com" target="_blank" style="color: #00D4AA; text-decoration: none; font-weight: 600;">
                    🎯 Charles Schwab
                </a>
                <p style="color: #ddd; margin: 5px 0; font-size: 0.9rem;">Full-service investment platform</p>
            </div>
            <div style="margin-bottom: 10px;">
                <a href="https://www.tdameritrade.com" target="_blank" style="color: #00D4AA; text-decoration: none; font-weight: 600;">
                    📈 TD Ameritrade
                </a>
                <p style="color: #ddd; margin: 5px 0; font-size: 0.9rem;">Advanced trading tools</p>
            </div>
        </div>
        
        <div style="
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            padding: 20px;
            border-radius: 15px;
            margin: 10px 0;
            animation: slideInLeft 1s ease-out;
        ">
            <h4 style="color: white; margin: 0 0 15px 0;">🇪🇺 Europe</h4>
            <div style="margin-bottom: 10px;">
                <a href="https://www.degiro.com" target="_blank" style="color: #00D4AA; text-decoration: none; font-weight: 600;">
                    🚀 DEGIRO
                </a>
                <p style="color: #ddd; margin: 5px 0; font-size: 0.9rem;">Low-cost European broker</p>
            </div>
            <div style="margin-bottom: 10px;">
                <a href="https://www.etoro.com" target="_blank" style="color: #00D4AA; text-decoration: none; font-weight: 600;">
                    👥 eToro
                </a>
                <p style="color: #ddd; margin: 5px 0; font-size: 0.9rem;">Social trading platform</p>
            </div>
            <div style="margin-bottom: 10px;">
                <a href="https://www.trading212.com" target="_blank" style="color: #00D4AA; text-decoration: none; font-weight: 600;">
                    📱 Trading 212
                </a>
                <p style="color: #ddd; margin: 5px 0; font-size: 0.9rem;">Commission-free trading</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🇹🇷 Turkish Brokers")
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #FF6B6B 0%, #FF8E8E 100%);
            padding: 20px;
            border-radius: 15px;
            margin: 10px 0;
            animation: slideInRight 0.8s ease-out;
        ">
            <h4 style="color: white; margin: 0 0 15px 0;">🏦 Türkiye Brokerleri</h4>
            <div style="margin-bottom: 10px;">
                <a href="https://www.isyatirim.com.tr" target="_blank" style="color: #00D4AA; text-decoration: none; font-weight: 600;">
                    🏛️ İş Yatırım
                </a>
                <p style="color: #ddd; margin: 5px 0; font-size: 0.9rem;">Türkiye'nin lider yatırım bankası</p>
            </div>
            <div style="margin-bottom: 10px;">
                <a href="https://www.yapikredi.com.tr/yatirim-hizmetleri" target="_blank" style="color: #00D4AA; text-decoration: none; font-weight: 600;">
                    🏦 Yapı Kredi Yatırım
                </a>
                <p style="color: #ddd; margin: 5px 0; font-size: 0.9rem;">Kapsamlı yatırım çözümleri</p>
            </div>
            <div style="margin-bottom: 10px;">
                <a href="https://www.garanti.com.tr/tr/bireysel/yatirim" target="_blank" style="color: #00D4AA; text-decoration: none; font-weight: 600;">
                    💳 Garanti BBVA Yatırım
                </a>
                <p style="color: #ddd; margin: 5px 0; font-size: 0.9rem;">Dijital yatırım platformu</p>
            </div>
            <div style="margin-bottom: 10px;">
                <a href="https://www.qnbfinansyatirim.com" target="_blank" style="color: #00D4AA; text-decoration: none; font-weight: 600;">
                    🌟 QNB Finans Yatırım
                </a>
                <p style="color: #ddd; margin: 5px 0; font-size: 0.9rem;">Profesyonel yatırım danışmanlığı</p>
            </div>
            <div style="margin-bottom: 10px;">
                <a href="https://www.akbankyatirim.com.tr" target="_blank" style="color: #00D4AA; text-decoration: none; font-weight: 600;">
                    🏦 Akbank Yatırım
                </a>
                <p style="color: #ddd; margin: 5px 0; font-size: 0.9rem;">Güvenilir yatırım partneri</p>
            </div>
        </div>
        
        <div style="
            background: linear-gradient(135deg, #2ECC71 0%, #27AE60 100%);
            padding: 20px;
            border-radius: 15px;
            margin: 10px 0;
            animation: slideInRight 1s ease-out;
        ">
            <h4 style="color: white; margin: 0 0 15px 0;">📱 Digital Platforms</h4>
            <div style="margin-bottom: 10px;">
                <a href="https://www.gedik.com.tr" target="_blank" style="color: #00D4AA; text-decoration: none; font-weight: 600;">
                    🚀 Gedik Yatırım
                </a>
                <p style="color: #ddd; margin: 5px 0; font-size: 0.9rem;">Teknoloji odaklı broker</p>
            </div>
            <div style="margin-bottom: 10px;">
                <a href="https://www.odeabank.com.tr/tr-tr/bireysel/yatirim" target="_blank" style="color: #00D4AA; text-decoration: none; font-weight: 600;">
                    💎 Odea Bank Yatırım
                </a>
                <p style="color: #ddd; margin: 5px 0; font-size: 0.9rem;">Yenilikçi bankacılık</p>
            </div>
            <div style="margin-bottom: 10px;">
                <a href="https://www.matriks.com.tr" target="_blank" style="color: #00D4AA; text-decoration: none; font-weight: 600;">
                    📊 Matriks Bilgi Dağıtım
                </a>
                <p style="color: #ddd; margin: 5px 0; font-size: 0.9rem;">Gelişmiş analiz araçları</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Warning and disclaimer
    st.markdown("---")
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #FFA726 0%, #FFB74D 100%);
        padding: 15px;
        border-radius: 10px;
        margin: 20px 0;
        text-align: center;
        animation: pulse 3s infinite;
    ">
        <h4 style="color: white; margin: 0 0 10px 0;">⚠️ Investment Disclaimer</h4>
        <p style="color: white; margin: 0; font-size: 0.9rem;">
            <strong>Risk Warning:</strong> Trading stocks and financial instruments involves significant risk. 
            Past performance does not guarantee future results. Please conduct thorough research and consider 
            seeking advice from qualified financial advisors before making investment decisions.
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
