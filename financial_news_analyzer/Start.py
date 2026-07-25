"""
Financial News Analyzer
Modern financial analysis platform for market intelligence

This application provides:
- Clean Architecture with layered design
- Professional financial analysis tools
- Latest available market-data visualization
- Comprehensive news sentiment analysis
- Global market coverage
- Use Case Pattern
"""
import streamlit as st
import sys
import os
from datetime import datetime
import logging
import importlib
from pathlib import Path
from typing import Optional, Dict, Any

# Add the repository root to the import path so the application is imported as
# a package.  This keeps the relative imports used by the Clean Architecture
# layers valid both locally and when Streamlit starts the app.
current_dir = Path(__file__).parent
repository_root = current_dir.parent
if str(repository_root) not in sys.path:
    sys.path.insert(0, str(repository_root))

from financial_news_analyzer.src.presentation import design_system

design_system = importlib.reload(design_system)
apply_design_system = design_system.apply_design_system
render_page_header = design_system.render_page_header

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class FinancialAnalyzerApp:
    """
    Main application class for financial news analysis
    
    Features:
    - Comprehensive market data analysis
    - Provider-linked news sentiment tracking
    - Interactive data visualization
    - Multi-platform broker integration
    """
    
    _instance: Optional['FinancialAnalyzerApp'] = None
    
    def __new__(cls):
        """Ensure singleton instance"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize application components"""
        if not hasattr(self, '_initialized'):
            self._initialize_app()
            self._initialized = True
    
    def _initialize_app(self):
        """Initialize application dependencies and components"""
        try:
            # Configure Streamlit page
            self._configure_page()
            
            # Initialize dependency container
            self._initialize_container()
            
            # Initialize UI components
            self._initialize_components()
            
            logging.info("Application initialized successfully")
            
        except Exception as e:
            logging.error(f"Failed to initialize application: {e}")
            st.error(f"Application initialization failed: {e}")
    
    def _configure_page(self):
        """Configure Streamlit page settings"""
        st.set_page_config(
            page_title="📊 Financial News Analyzer",
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="collapsed"
        )
    
    def _initialize_container(self):
        """Initialize dependency injection container"""
        try:
            from financial_news_analyzer.src.infrastructure.container import Container

            self._container = Container()
            health = self._container.health_check()
            if health["container_status"] != "healthy":
                logging.warning("Container health check: %s", health)
        except Exception as e:
            logging.error(f"Failed to initialize container: {e}")
            self._container = self._create_fallback_container()
    
    def _create_fallback_container(self):
        """Create a minimal fallback container for demo purposes"""
        class FallbackContainer:
            def health_check(self):
                return {
                    "container_status": "fallback",
                    "services_count": 0,
                    "services": {}
                }
        
        return FallbackContainer()
    
    def _initialize_components(self):
        """Initialize UI components"""
        try:
            from financial_news_analyzer.src.presentation.components.world_clock_component import WorldClockComponent

            self._world_clock = WorldClockComponent()
        except Exception as e:
            logging.error(f"Failed to initialize components: {e}")
            self._world_clock = self._create_fallback_world_clock()
    
    def _create_fallback_world_clock(self):
        """Create a comprehensive fallback world clock component"""
        class FallbackWorldClock:
            def render(self):
                # Global Markets Section in Sidebar
                st.sidebar.markdown("""
                <div style="
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 20px;
                    border-radius: 15px;
                    margin: 15px 0;
                    text-align: center;
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
                ">
                    <h2 style="color: white; margin: 0; font-size: 1.5rem;">🌍 Global Markets</h2>
                </div>
                """, unsafe_allow_html=True)
                
                # Market Status Cards
                import datetime
                import pytz
                
                # Define major markets with their timezones
                markets = {
                    "🇺🇸 NYSE": {"tz": "America/New_York", "open": 9, "close": 16},
                    "🇬🇧 LSE": {"tz": "Europe/London", "open": 8, "close": 16},
                    "🇯🇵 TSE": {"tz": "Asia/Tokyo", "open": 9, "close": 15},
                    "🇭🇰 HKEX": {"tz": "Asia/Hong_Kong", "open": 9, "close": 16},
                    "🇩🇪 FSE": {"tz": "Europe/Berlin", "open": 9, "close": 17}
                }
                
                for market_name, market_info in markets.items():
                    try:
                        tz = pytz.timezone(market_info["tz"])
                        market_time = datetime.datetime.now(tz)
                        current_hour = market_time.hour
                        
                        # Determine market status
                        if market_info["open"] <= current_hour < market_info["close"]:
                            status = "🟢 OPEN"
                            status_color = "#00D4AA"
                        else:
                            status = "🔴 CLOSED"
                            status_color = "#FF6B6B"
                        
                        # Market card
                        st.sidebar.markdown(f"""
                        <div style="
                            background: var(--secondary-bg, #262730);
                            padding: 12px;
                            border-radius: 10px;
                            margin: 8px 0;
                            border-left: 4px solid {status_color};
                            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
                        ">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <strong style="color: white; font-size: 0.9rem;">{market_name}</strong><br>
                                    <span style="color: #CCCCCC; font-size: 0.8rem;">{market_time.strftime('%H:%M')}</span>
                                </div>
                                <div style="text-align: right;">
                                    <span style="color: {status_color}; font-size: 0.8rem; font-weight: bold;">
                                        {status}
                                    </span>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    except Exception as e:
                        # Fallback for timezone issues
                        st.sidebar.markdown(f"""
                        <div style="
                            background: var(--secondary-bg, #262730);
                            padding: 12px;
                            border-radius: 10px;
                            margin: 8px 0;
                            border-left: 4px solid #4ECDC4;
                        ">
                            <strong style="color: white;">{market_name}</strong><br>
                            <span style="color: #CCCCCC; font-size: 0.8rem;">Loading...</span>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Quick Market Indices
                st.sidebar.markdown("""
                <div style="
                    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                    padding: 15px;
                    border-radius: 10px;
                    margin: 15px 0;
                    text-align: center;
                ">
                    <h4 style="color: white; margin: 0;">📊 Quick Indices</h4>
                </div>
                """, unsafe_allow_html=True)
                
                # Sample indices data
                import random
                indices = [
                    {"name": "S&P 500", "value": 4500 + random.randint(-100, 100), "change": random.uniform(-2, 2)},
                    {"name": "NASDAQ", "value": 14000 + random.randint(-200, 200), "change": random.uniform(-2, 2)},
                    {"name": "DOW", "value": 35000 + random.randint(-500, 500), "change": random.uniform(-2, 2)}
                ]
                
                for index in indices:
                    change_color = "#00D4AA" if index["change"] >= 0 else "#FF6B6B"
                    change_symbol = "+" if index["change"] >= 0 else ""
                    
                    st.sidebar.markdown(f"""
                    <div style="
                        background: rgba(255, 255, 255, 0.05);
                        padding: 8px;
                        border-radius: 8px;
                        margin: 5px 0;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                    ">
                        <span style="color: white; font-size: 0.85rem;">{index["name"]}</span>
                        <div style="text-align: right;">
                            <div style="color: white; font-size: 0.85rem;">{index["value"]:,.0f}</div>
                            <div style="color: {change_color}; font-size: 0.75rem;">
                                {change_symbol}{index["change"]:.2f}%
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        return FallbackWorldClock()
    
    def run(self):
        """Main application entry point"""
        try:
            # Apply custom styling
            self._apply_styling()
            apply_design_system()
            
            # Render main header
            self._render_header()
            
            # Always render sidebar - let Streamlit handle visibility
            self._render_sidebar()
            
            # Render main content
            self._render_main_content()
            
            # Render footer
            self._render_footer()
            
        except Exception as e:
            logging.error(f"Application runtime error: {e}")
            st.error("An error occurred while running the application")
    
    def _apply_styling(self):
        """Apply custom CSS styling"""
        st.markdown("""
        <style>
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
            
            @keyframes pulse {
                0% { box-shadow: 0 0 0 0 rgba(52, 73, 94, 0.7); }
                70% { box-shadow: 0 0 0 10px rgba(52, 73, 94, 0); }
                100% { box-shadow: 0 0 0 0 rgba(52, 73, 94, 0); }
            }
            
            /* Dark theme */
            .stApp {
                background-color: #1a1a1a !important;
                color: #ffffff;
                animation: fadeInUp 0.8s ease-out;
            }
            
            .main .block-container {
                background: #1a1a1a !important;
                padding: 2rem;
                border-radius: 15px;
                margin-top: 1rem;
                max-width: 100%;
                color: #ffffff;
                animation: fadeInUp 1s ease-out;
            }
            
            /* Modern cards */
            .feature-card {
                padding: 20px;
                border-radius: 12px;
                background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
                color: #ffffff;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                margin: 10px 0;
                border: 1px solid #3a3a3a;
                transition: all 0.3s ease;
            }
            
            .feature-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 6px 20px rgba(0,0,0,0.4);
                animation: pulse 2s infinite;
            }
            
            /* Modern buttons with enhanced smooth transitions */
            .stButton > button {
                background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%);
                border: 1px solid #4a4a4a;
                border-radius: 8px;
                color: #ffffff;
                font-weight: 600;
                padding: 0.75rem 2rem;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            }
            
            .stButton > button:hover {
                transform: translateY(-2px) scale(1.02);
                box-shadow: 0 4px 12px rgba(0, 212, 170, 0.3);
                background: linear-gradient(135deg, #3c5a78 0%, #34495e 100%);
            }
            
            .stButton > button:active {
                transform: translateY(-1px) scale(1.01);
                transition: all 0.1s ease-in-out;
            }
                box-shadow: 0 4px 12px rgba(0,0,0,0.4);
                background: linear-gradient(135deg, #3c5a78 0%, #34495e 100%);
            }
            
            /* Sidebar - only background styling, allow native Streamlit behavior with smooth transitions */
            section[data-testid="stSidebar"] > div {
                background: linear-gradient(180deg, #1a1a1a 0%, #2c3e50 100%) !important;
                color: #ffffff !important;
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
                color: #ffffff !important;
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
                font-weight: 600 !important;
                color: #ffffff !important;
                white-space: nowrap !important;
            }
            
            .stSelectbox > div > div, .stMultiSelect > div > div {
                min-width: 300px !important;
                font-size: 0.85rem !important;
            }
            
            /* Status indicators */
            .status-indicator {
                display: inline-block;
                padding: 4px 8px;
                border-radius: 12px;
                font-size: 0.8em;
                font-weight: bold;
                margin: 2px;
            }
            
            /* Metric card styling */
            .metric-card {
                background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
                padding: 20px;
                border-radius: 15px;
                border: 1px solid #3a3a3a;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
                transition: all 0.3s ease;
                margin: 10px 0;
                color: #ffffff;
            }
            
            .metric-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 30px rgba(0, 212, 170, 0.2);
            }
            
            .status-healthy {
                background-color: #27ae60;
                color: white;
            }
            
            .status-warning {
                background-color: #f39c12;
                color: white;
            }
            
            .status-error {
                background-color: #e74c3c;
                color: white;
            }
        </style>
        """, unsafe_allow_html=True)
    
    def _render_header(self):
        """Render application header"""
        render_page_header(
            "Financial News Analyzer",
            "Provider-linked news, explainable sentiment signals, and market context in one focused workspace.",
            eyebrow="Market intelligence workspace",
            badges=["Yahoo Finance linked data", "Explainable signals", "14 market clocks"],
        )
    
    def _render_sidebar(self):
        """Render sidebar components"""
        # Streamlit already renders the working multipage navigation at the top
        # of the sidebar. Keep this area compact so market clocks remain visible.
        st.sidebar.markdown("---")
        
        # World clock
        if self._world_clock:
            self._world_clock.render()
        else:
            st.sidebar.error("World clock component unavailable")
    
    def _render_main_content(self):
        """Render main application content"""
        self._render_workspace_actions()

        # Core features section
        self._render_features()

        st.caption(
            "Market prices and article metadata are retrieved from the provider when you open a workspace. "
            "No simulated feed or configuration dashboard is shown here."
        )

    def _render_workspace_actions(self):
        """Surface the two primary workflows before secondary information."""
        st.markdown("### Choose a workspace")
        st.caption("Start with the task you want to complete. You can return here any time from the sidebar.")
        news_col, market_col = st.columns(2)
        with news_col:
            st.page_link(
                "pages/1_Financial_Analysis.py",
                label="Open financial news research",
                icon="📰",
                use_container_width=True,
            )
            st.caption("Select companies, review linked stories, and compare sentiment signals.")
        with market_col:
            st.page_link(
                "pages/2_Market_Data.py",
                label="Open market data workspace",
                icon="📈",
                use_container_width=True,
            )
            st.caption("Explore current closes, price history, and category performance.")
        st.markdown("<div style='height: .75rem'></div>", unsafe_allow_html=True)
    
    def _render_features(self):
        """Render core features section"""
        st.markdown("### 🚀 Core Features")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="feature-card">
                <h4>📰 Financial News Analysis</h4>
                <p>Linked financial-news retrieval with a transparent keyword sentiment baseline.
                Every displayed item links to its provider source for verification.</p>
                <div style="margin-top: 15px;">
                    <span class="status-indicator status-healthy">Provider Links</span>
                    <span class="status-indicator status-healthy">Baseline Sentiment</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card">
                <h4>📊 Market Data Visualization</h4>
                <p>Interactive charts using the latest available daily OHLCV data. Values are
                cached briefly and clearly identify the external data provider.</p>
                <div style="margin-top: 15px;">
                    <span class="status-indicator status-healthy">Latest Daily Close</span>
                    <span class="status-indicator status-healthy">Interactive</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="feature-card">
                <h4>🌍 Global Market Coverage</h4>
                <p>Weekday market schedules across the Americas, Europe, Asia-Pacific, and
                MENA regions, displayed in each exchange's local timezone.</p>
                <div style="margin-top: 15px;">
                    <span class="status-indicator status-healthy">Weekday Schedules</span>
                    <span class="status-indicator status-healthy">Multi-timezone</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    def _render_quick_stats(self):
        """Render quick stats dashboard"""
        st.markdown("---")
        st.markdown("### 📈 Market Overview")
        st.caption("These cards describe the current application configuration; market values are available on the data pages.")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("News source", "Linked provider", "Yahoo Finance")
        with col2:
            st.metric("Sentiment", "Keyword baseline", "Explainable")
        with col3:
            st.metric("Market schedule", "Weekdays", "14 exchanges")
        with col4:
            st.metric("Refresh window", "5 minutes", "Provider cache")
    
    def _render_live_feed(self):
        """Render live market feed"""
        st.markdown("---")
        st.markdown("### 🧪 Demo Market Feed")
        st.caption("This feed is a product preview and is not sourced from a live market provider.")
        
        # Create sample live feed data with diverse companies
        import random
        companies = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "JPM", "JNJ", "XOM", "WMT", "PFE", "BA", "DIS", "NVDA", "META", "BRK.A"]
        events = ["Price Alert", "Volume Spike", "News Impact", "Technical Signal", "Market Update", "Earnings Report", "Analyst Rating"]
        messages = {
            "Price Alert": ["reaches new daily high", "breaks resistance level", "hits support zone"],
            "Volume Spike": ["unusual trading volume detected", "volume surge of 200%", "institutional buying"],
            "News Impact": ["earnings report drives sentiment", "analyst upgrade", "partnership announcement"], 
            "Technical Signal": ["moving average crossover", "RSI oversold signal", "bullish pattern"],
            "Market Update": ["sector rotation detected", "market volatility increase", "correlation alert"],
            "Earnings Report": ["beats earnings estimates", "revenue guidance updated", "quarterly results"],
            "Analyst Rating": ["price target raised", "recommendation upgrade", "coverage initiated"]
        }
        
        feed_items = []
        for i in range(8):
            symbol = random.choice(companies)
            event = random.choice(events)
            message = random.choice(messages[event])
            time_offset = random.randint(1, 30)
            
            # Determine sentiment
            if any(word in message for word in ["high", "upgrade", "beats", "raised"]):
                sentiment = "positive"
            elif any(word in message for word in ["volatility", "oversold", "support"]):
                sentiment = "negative"
            else:
                sentiment = "neutral"
                
            feed_items.append({
                "time": f"09:{30-time_offset:02d}",
                "symbol": symbol,
                "event": event,
                "message": message,
                "type": sentiment
            })
        
        for item in feed_items:
            type_colors = {
                "positive": "#00D4AA",
                "negative": "#FF6B6B", 
                "neutral": "#4ECDC4"
            }
            color = type_colors.get(item["type"], "#4ECDC4")
            
            st.markdown(f"""
            <div style="
                background: var(--secondary-bg);
                padding: 12px;
                border-radius: 8px;
                margin: 5px 0;
                border-left: 4px solid {color};
                display: flex;
                justify-content: space-between;
                align-items: center;
            ">
                <div>
                    <strong style="color: {color};">{item['symbol']} - {item['event']}</strong><br>
                    <span style="color: #CCCCCC; font-size: 0.9rem;">{item['message']}</span>
                </div>
                <div style="color: #888; font-size: 0.8rem;">
                    {item['time']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    def _render_technical_info(self):
        """Render technical information section"""
        with st.expander("🛠️ Technical Architecture & Information"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                **🏗️ Architecture:**
                - Clean Architecture (Domain, Application, Infrastructure)
                - SOLID Principles Implementation
                - Dependency Injection Pattern
                - Repository Pattern
                - Use Case Pattern
                - Observer Pattern
                - Strategy Pattern
                """)
            
            with col2:
                st.markdown("""
                **🖥️ Technology Stack:**
                - Python 3.11+ with Type Hints
                - Streamlit Framework
                - Domain-Driven Design
                - Comprehensive Error Handling
                - Logging and Monitoring
                - Responsive Design
                """)
            
            # Show system metrics if available
            if self._container:
                st.markdown("**📊 System Metrics:**")
                health = self._container.health_check()
                
                metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
                
                with metrics_col1:
                    st.metric("Services", health.get("services_count", 0))
                
                with metrics_col2:
                    status = health.get("container_status", "unknown")
                    st.metric("Status", status.title())
                
                with metrics_col3:
                    st.metric("Mode", "Active" if status == "healthy" else "Demo")
            else:
                st.markdown("**📊 System Metrics:**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Services", "Demo")
                with col2:
                    st.metric("Status", "Fallback")
                with col3:
                    st.metric("Mode", "Demo")
    
    def _render_footer(self):
        """Render application footer"""
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #666; margin-top: 30px;">
            <p>📊 Financial News Analyzer • Built with ❤️ for Financial Professionals</p>
            <p style="font-size: 0.9em;">
                Provider-linked data • Explainable analysis • Research tooling • Modern Architecture
            </p>
            <p style="font-size: 0.8em; margin-top: 10px;">
                Powered by Clean Code principles and SOLID design patterns
            </p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main application entry point"""
    try:
        app = FinancialAnalyzerApp()
        app.run()
        
    except Exception as e:
        logging.error(f"Critical application error: {e}")
        st.error(f"Critical error: {e}")
        st.info("Please refresh the page or contact support if the problem persists.")

if __name__ == "__main__":
    main()
