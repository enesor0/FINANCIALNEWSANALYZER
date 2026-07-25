"""
Market Data Analysis Page
Latest available market-data visualization and price history
"""

import streamlit as st          # type: ignore
import pandas as pd # type: ignore
import plotly.express as px # type: ignore
import plotly.graph_objects as go  # type: ignore
import sys
import importlib
from pathlib import Path

repository_root = Path(__file__).resolve().parents[2]
if str(repository_root) not in sys.path:
    sys.path.insert(0, str(repository_root))

from financial_news_analyzer.src.application.exceptions import DataProviderUnavailable
from financial_news_analyzer.src.domain.entities.market_data import MarketInstrument
from financial_news_analyzer.src.presentation import design_system
from financial_news_analyzer.src.presentation.app_shell import render_app_shell
from financial_news_analyzer.src.presentation.dependencies import get_application_services

design_system = importlib.reload(design_system)
apply_design_system = design_system.apply_design_system
render_page_header = design_system.render_page_header

# Page configuration
st.set_page_config(
    page_title="📈 Market Data",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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

def get_live_universe():
    """Return a balanced, bounded symbol set for the live market overview."""
    instruments = []
    for category, companies in get_company_database().items():
        instruments.extend((symbol, company, category) for company, symbol in list(companies.items())[:3])
    return instruments

@st.cache_data(ttl=300, show_spinner=False)
def load_live_market_data(instruments):
    """Adapt the snapshot use-case result for the existing Plotly view."""
    snapshot = get_application_services().get_market_snapshot.execute(
        MarketInstrument(symbol, company, category) for symbol, company, category in instruments
    )
    return pd.DataFrame([
        {
            'Symbol': quote.instrument.symbol,
            'Company': quote.instrument.name,
            'Category': quote.instrument.category,
            'Price': round(quote.price, 2),
            'Change': round(quote.change, 2),
            'Change_Pct': round(quote.change_percent, 2),
            'Market_Cap': None,
            'Volume': quote.volume,
            'Day_High': quote.day_high,
            'Day_Low': quote.day_low,
            'High_52w': None,
            'Low_52w': None,
            'PE_Ratio': None,
            'Dividend_Yield': None,
            'Last_Updated': quote.observed_at,
            'Data_Source': quote.provider,
        }
        for quote in snapshot.quotes
    ])


@st.cache_data(ttl=300, show_spinner=False)
def load_live_history(symbol, days):
    """Adapt historical price bars for the existing Plotly view."""
    history = get_application_services().get_price_history.execute(symbol, days)
    return pd.DataFrame([
        {
            'Date': bar.observed_at,
            'Open': bar.open_price,
            'High': bar.high_price,
            'Low': bar.low_price,
            'Close': bar.close_price,
            'Volume': bar.volume,
        }
        for bar in history.bars
    ])

def create_market_overview_chart(df):
    """Create market overview chart"""
    # Sort by market cap for better visualization
    df_sorted = df.sort_values('Market_Cap', ascending=True)
    
    fig = go.Figure()
    
    # Color based on price change
    colors = ['#7B9669' if change > 0 else '#404E3B' if change < 0 else '#6C8480'
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
        increasing_line_color='#7B9669',
        decreasing_line_color='#404E3B',
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
        line=dict(color='#BAC8B1', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=df_historical['Date'],
        y=df_historical['MA50'],
        mode='lines',
        name='MA50',
        line=dict(color='#6C8480', width=2)
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
        marker_color='#6C8480',
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

def create_category_performance_chart(df):
    """Show the actual average daily return for each displayed category."""
    category_returns = df.groupby('Category', as_index=False)['Change_Pct'].mean()
    category_returns = category_returns.sort_values('Change_Pct')
    colors = ['#7B9669' if value >= 0 else '#404E3B' for value in category_returns['Change_Pct']]
    fig = go.Figure(data=go.Bar(
        x=category_returns['Category'],
        y=category_returns['Change_Pct'],
        marker_color=colors,
        text=[f"{value:+.2f}%" for value in category_returns['Change_Pct']],
        textposition='auto',
    ))
    fig.update_layout(
        title="Average Daily Performance by Category",
        xaxis_title="Category",
        yaxis_title="Average change (%)",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
    )
    return fig

def main():
    """Main function for Market Data page"""
    apply_design_system()
    render_app_shell("market")
    
    render_page_header(
        "Market data without the noise",
        "Compare the latest available closes, inspect price history, and narrow the universe with focused controls.",
        eyebrow="Market workspace",
        badges=["Latest daily close", "Interactive charts", "Yahoo Finance provider"],
    )
    
    # Live provider data. We intentionally do not fall back to random values:
    # a missing provider must be visible to the user instead of looking real.
    if st.sidebar.button("↻ Refresh live data", use_container_width=True):
        load_live_market_data.clear()
        load_live_history.clear()
        st.rerun()

    try:
        with st.spinner("Loading latest available market prices..."):
            market_df = load_live_market_data(tuple(get_live_universe()))
    except DataProviderUnavailable as exc:
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
    except DataProviderUnavailable as exc:
        st.warning(f"Historical data is unavailable for {selected_stock}: {exc}")
        historical_df = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
    
    # Market overview metrics
    st.subheader("🌍 Market Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        gainers = len(filtered_market_df[filtered_market_df['Change_Pct'] > 0])
        st.markdown(f"""
        <div class="metric-card summary-card price-up">
            <h3>📈 Gainers</h3>
            <h2>{gainers}</h2>
            <p>Stocks up today</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        losers = len(filtered_market_df[filtered_market_df['Change_Pct'] < 0])
        st.markdown(f"""
        <div class="metric-card summary-card price-down">
            <h3>📉 Losers</h3>
            <h2>{losers}</h2>
            <p>Stocks down today</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_change = round(filtered_market_df['Change_Pct'].mean(), 2)
        status_class = "price-up" if avg_change > 0 else "price-down" if avg_change < 0 else "price-stable"
        st.markdown(f"""
        <div class="metric-card summary-card {status_class}">
            <h3>📊 Avg Change</h3>
            <h2>{avg_change}%</h2>
            <p>Market average</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        total_volume = filtered_market_df['Volume'].sum() / 1_000_000  # Convert to millions
        st.markdown(f"""
        <div class="metric-card summary-card price-stable">
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
        <div class="metric-card summary-card {change_class}">
            <h4>Current Price</h4>
            <h3>${stock_data['Price']}</h3>
            <p class="{'price-change-positive' if stock_data['Change'] > 0 else 'price-change-negative'}">
                {stock_data['Change']:+.2f} ({stock_data['Change_Pct']:+.2f}%)
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card summary-card">
            <h4>Market Cap</h4>
            <h3>{market_cap_display}</h3>
            <p>Not supplied by snapshot</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card summary-card">
            <h4>P/E Ratio</h4>
            <h3>{pe_ratio_display}</h3>
            <p>Not supplied by snapshot</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card summary-card">
            <h4>Day High</h4>
            <h3>{day_high_display}</h3>
            <p>Today's high</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="metric-card summary-card">
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
        st.plotly_chart(create_category_performance_chart(filtered_market_df), use_container_width=True)
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

    st.caption(
        "Live market values are supplied by Yahoo Finance and may be delayed. "
        "This workspace does not include broker promotions, simulated prices, or investment recommendations."
    )
    return

    # Legacy static broker content retained below for source history only.
    st.markdown("---")
    st.markdown("## 🏦 External Broker & Platform Links")
    st.caption("These links are informational only, not endorsements or investment recommendations. Verify eligibility, fees, and regulation independently.")
    
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
                <a href="https://www.interactivebrokers.com" target="_blank" style="color: #7B9669; text-decoration: none; font-weight: 600;">
                    📊 Interactive Brokers
                </a>
                <p style="color: #ddd; margin: 5px 0; font-size: 0.9rem;">Low-cost global trading platform</p>
            </div>
            <div style="margin-bottom: 10px;">
                <a href="https://www.fidelity.com" target="_blank" style="color: #7B9669; text-decoration: none; font-weight: 600;">
                    🏛️ Fidelity Investments
                </a>
                <p style="color: #ddd; margin: 5px 0; font-size: 0.9rem;">No commission stock trading</p>
            </div>
            <div style="margin-bottom: 10px;">
                <a href="https://www.schwab.com" target="_blank" style="color: #7B9669; text-decoration: none; font-weight: 600;">
                    🎯 Charles Schwab
                </a>
                <p style="color: #ddd; margin: 5px 0; font-size: 0.9rem;">Full-service investment platform</p>
            </div>
            <div style="margin-bottom: 10px;">
                <a href="https://www.tdameritrade.com" target="_blank" style="color: #7B9669; text-decoration: none; font-weight: 600;">
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
                <a href="https://www.degiro.com" target="_blank" style="color: #7B9669; text-decoration: none; font-weight: 600;">
                    🚀 DEGIRO
                </a>
                <p style="color: #ddd; margin: 5px 0; font-size: 0.9rem;">Low-cost European broker</p>
            </div>
            <div style="margin-bottom: 10px;">
                <a href="https://www.etoro.com" target="_blank" style="color: #7B9669; text-decoration: none; font-weight: 600;">
                    👥 eToro
                </a>
                <p style="color: #ddd; margin: 5px 0; font-size: 0.9rem;">Social trading platform</p>
            </div>
            <div style="margin-bottom: 10px;">
                <a href="https://www.trading212.com" target="_blank" style="color: #7B9669; text-decoration: none; font-weight: 600;">
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
            background: linear-gradient(135deg, #404E3B 0%, #6C8480 100%);
            padding: 20px;
            border-radius: 15px;
            margin: 10px 0;
            animation: slideInRight 0.8s ease-out;
        ">
            <h4 style="color: white; margin: 0 0 15px 0;">🏦 Türkiye Brokerleri</h4>
            <div style="margin-bottom: 10px;">
                <a href="https://www.isyatirim.com.tr" target="_blank" style="color: #7B9669; text-decoration: none; font-weight: 600;">
                    🏛️ İş Yatırım
                </a>
                <p style="color: #ddd; margin: 5px 0; font-size: 0.9rem;">Türkiye'nin lider yatırım bankası</p>
            </div>
            <div style="margin-bottom: 10px;">
                <a href="https://www.yapikredi.com.tr/yatirim-hizmetleri" target="_blank" style="color: #7B9669; text-decoration: none; font-weight: 600;">
                    🏦 Yapı Kredi Yatırım
                </a>
                <p style="color: #ddd; margin: 5px 0; font-size: 0.9rem;">Kapsamlı yatırım çözümleri</p>
            </div>
            <div style="margin-bottom: 10px;">
                <a href="https://www.garanti.com.tr/tr/bireysel/yatirim" target="_blank" style="color: #7B9669; text-decoration: none; font-weight: 600;">
                    💳 Garanti BBVA Yatırım
                </a>
                <p style="color: #ddd; margin: 5px 0; font-size: 0.9rem;">Dijital yatırım platformu</p>
            </div>
            <div style="margin-bottom: 10px;">
                <a href="https://www.qnbfinansyatirim.com" target="_blank" style="color: #7B9669; text-decoration: none; font-weight: 600;">
                    🌟 QNB Finans Yatırım
                </a>
                <p style="color: #ddd; margin: 5px 0; font-size: 0.9rem;">Profesyonel yatırım danışmanlığı</p>
            </div>
            <div style="margin-bottom: 10px;">
                <a href="https://www.akbankyatirim.com.tr" target="_blank" style="color: #7B9669; text-decoration: none; font-weight: 600;">
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
                <a href="https://www.gedik.com.tr" target="_blank" style="color: #7B9669; text-decoration: none; font-weight: 600;">
                    🚀 Gedik Yatırım
                </a>
                <p style="color: #ddd; margin: 5px 0; font-size: 0.9rem;">Teknoloji odaklı broker</p>
            </div>
            <div style="margin-bottom: 10px;">
                <a href="https://www.odeabank.com.tr/tr-tr/bireysel/yatirim" target="_blank" style="color: #7B9669; text-decoration: none; font-weight: 600;">
                    💎 Odea Bank Yatırım
                </a>
                <p style="color: #ddd; margin: 5px 0; font-size: 0.9rem;">Yenilikçi bankacılık</p>
            </div>
            <div style="margin-bottom: 10px;">
                <a href="https://www.matriks.com.tr" target="_blank" style="color: #7B9669; text-decoration: none; font-weight: 600;">
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
        background: linear-gradient(135deg, #6C8480 0%, #BAC8B1 100%);
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
