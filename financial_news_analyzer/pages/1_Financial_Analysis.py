"""
Financial News Analysis Page
Provider-linked financial news with explainable sentiment scoring
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import sys
import importlib
from html import escape
from pathlib import Path

repository_root = Path(__file__).resolve().parents[2]
if str(repository_root) not in sys.path:
    sys.path.insert(0, str(repository_root))

from financial_news_analyzer.src.domain.services.sentiment_analysis_service import FinancialSentimentAnalyzer
from financial_news_analyzer.src.infrastructure.services.yahoo_finance_service import (
    LiveDataUnavailable,
    YahooFinanceService,
)
from financial_news_analyzer.src.presentation import design_system

design_system = importlib.reload(design_system)
apply_design_system = design_system.apply_design_system
render_page_header = design_system.render_page_header

# Page configuration
st.set_page_config(
    page_title="📊 Financial Analysis",
    page_icon="📊",
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
    
    .sentiment-positive {
        border-left: 4px solid #00D4AA;
        background: linear-gradient(135deg, #2c3e50 0%, rgba(0, 212, 170, 0.1) 100%);
    }
    
    .sentiment-negative {
        border-left: 4px solid #FF6B6B;
        background: linear-gradient(135deg, #2c3e50 0%, rgba(255, 107, 107, 0.1) 100%);
    }
    
    .sentiment-neutral {
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
        animation: slideInRight 1s ease-out;
        background-size: 200% 200%;
        animation: gradient-shift 3s ease-in-out infinite, slideInRight 1s ease-out;
    }
    
    @keyframes gradient-shift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
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
    
    /* Quick selection buttons */
    .quick-selection-button {
        background: linear-gradient(135deg, var(--accent-color) 0%, #2ECC71 100%);
        border: none;
        border-radius: 10px;
        padding: 10px 15px;
        font-size: 0.8rem;
        font-weight: 600;
        color: white;
        transition: all 0.3s ease;
        margin: 2px;
        box-shadow: 0 3px 10px rgba(0, 212, 170, 0.3);
        width: 100% !important;
        white-space: nowrap;
        text-overflow: ellipsis;
        overflow: hidden;
    }
    
    .quick-selection-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0, 212, 170, 0.5);
        background: linear-gradient(135deg, #2ECC71 0%, var(--accent-color) 100%);
    }
    
    /* Quick selection container styling */
    .stButton[data-baseweb="button"] {
        width: 100% !important;
    }
    
    .stButton > button[kind="secondary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        border-radius: 8px !important;
        color: white !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        padding: 0.5rem 1rem !important;
        font-size: 0.85rem !important;
        width: 100% !important;
        box-shadow: 0 3px 10px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5) !important;
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
    }
    
    /* Clear button styling */
    .clear-button {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E8E 100%);
        border: none;
        border-radius: 8px;
        color: white;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .clear-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
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
    
    /* Chart containers with animations */
    .chart-container {
        background: var(--gradient-1);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        animation: fadeInUp 0.8s ease-out;
        transition: all 0.3s ease;
    }
    
    .chart-container:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

def get_company_database():
    """Get comprehensive company database with categories"""
    return {
        'Technology': [
            'Apple', 'Microsoft', 'Google', 'Amazon', 'Meta', 'Netflix', 'NVIDIA', 'Adobe', 'Salesforce', 'Oracle',
            'IBM', 'Intel', 'AMD', 'Qualcomm', 'Broadcom', 'Texas Instruments', 'Applied Materials', 'Micron',
            'Advanced Micro Devices', 'Cisco Systems', 'VMware', 'ServiceNow', 'Snowflake', 'CrowdStrike', 'Zoom',
            'Slack', 'Dropbox', 'Box', 'Atlassian', 'Splunk', 'Palantir', 'Unity', 'Roblox', 'Shopify', 'Square',
            'PayPal', 'Stripe', 'Twilio', 'MongoDB', 'Datadog', 'Okta', 'Zscaler', 'Cloudflare', 'GitLab'
        ],
        'Finance': [
            'JPMorgan Chase', 'Bank of America', 'Wells Fargo', 'Citigroup', 'Goldman Sachs', 'Morgan Stanley',
            'American Express', 'Visa', 'Mastercard', 'BlackRock', 'Charles Schwab', 'Berkshire Hathaway',
            'Aon', 'Marsh & McLennan', 'Progressive', 'Allstate', 'Travelers', 'AIG', 'MetLife', 'Prudential',
            'Aflac', 'Lincoln National', 'Principal Financial', 'Raymond James', 'E*TRADE', 'TD Ameritrade',
            'Fidelity', 'Vanguard', 'State Street', 'Northern Trust', 'BNY Mellon', 'Capital One', 'Discover',
            'Synchrony Financial', 'Ally Financial', 'LendingClub', 'SoFi', 'Robinhood', 'Coinbase'
        ],
        'Healthcare': [
            'Johnson & Johnson', 'Pfizer', 'UnitedHealth', 'Merck', 'AbbVie', 'Bristol Myers Squibb', 'Eli Lilly',
            'Amgen', 'Gilead Sciences', 'Regeneron', 'Vertex Pharmaceuticals', 'Biogen', 'Moderna', 'Novavax',
            'Abbott Laboratories', 'Danaher', 'Thermo Fisher Scientific', 'Intuitive Surgical', 'Medtronic',
            'Boston Scientific', 'Stryker', 'Zimmer Biomet', 'Edwards Lifesciences', 'Illumina', 'IQVIA',
            'Anthem', 'Humana', 'Cigna', 'Aetna', 'Centene', 'Molina Healthcare', 'WellCare', 'Teladoc',
            'Veracyte', 'Exact Sciences', 'Guardant Health', 'Foundation Medicine', '10x Genomics'
        ],
        'Energy': [
            'ExxonMobil', 'Chevron', 'ConocoPhillips', 'EOG Resources', 'Pioneer Natural Resources', 'Schlumberger',
            'Halliburton', 'Baker Hughes', 'Kinder Morgan', 'Enterprise Products Partners', 'Plains All American',
            'Enbridge', 'TC Energy', 'Suncor Energy', 'Canadian Natural Resources', 'Imperial Oil', 'Cenovus',
            'NextEra Energy', 'Duke Energy', 'Southern Company', 'Dominion Energy', 'American Electric Power',
            'Exelon', 'Sempra Energy', 'Public Service Enterprise Group', 'Consolidated Edison', 'Xcel Energy',
            'Tesla Energy', 'First Solar', 'SunPower', 'Enphase Energy', 'SolarEdge', 'Bloom Energy'
        ],
        'Consumer': [
            'Walmart', 'Target', 'Home Depot', 'Lowes', 'Costco', 'Best Buy', 'Macys', 'Nordstrom', 'TJX Companies',
            'Ross Stores', 'Dollar General', 'Dollar Tree', 'CVS Health', 'Walgreens', 'Rite Aid', 'Amazon Retail',
            'eBay', 'Etsy', 'Wayfair', 'Overstock', 'Chewy', 'Petco', 'PetSmart', 'GameStop', 'Barnes & Noble',
            'Coca-Cola', 'PepsiCo', 'Nestle', 'Unilever', 'Procter & Gamble', 'Colgate-Palmolive', 'Kimberly-Clark',
            'General Mills', 'Kellogg', 'Kraft Heinz', 'Tyson Foods', 'Hormel', 'ConAgra', 'Campbell Soup'
        ],
        'Automotive': [
            'Tesla', 'Ford', 'General Motors', 'Stellantis', 'Toyota', 'Honda', 'Nissan', 'Hyundai', 'BMW',
            'Mercedes-Benz', 'Volkswagen', 'Audi', 'Porsche', 'Ferrari', 'Lucid Motors', 'Rivian', 'NIO',
            'XPeng', 'Li Auto', 'BYD', 'Geely', 'Great Wall Motors', 'SAIC Motor', 'Magna International',
            'Aptiv', 'Lear Corporation', 'BorgWarner', 'Eaton', 'Cummins', 'PACCAR', 'Navistar', 'Thor Industries'
        ],
        'Real Estate': [
            'American Tower', 'Prologis', 'Crown Castle', 'Equinix', 'Public Storage', 'Welltower', 'Realty Income',
            'Simon Property Group', 'Digital Realty Trust', 'SBA Communications', 'Extra Space Storage', 'AvalonBay',
            'Equity Residential', 'Boston Properties', 'Ventas', 'Host Hotels & Resorts', 'Kimco Realty',
            'Federal Realty', 'Regency Centers', 'Brixmor Property', 'CBRE Group', 'Jones Lang LaSalle',
            'Cushman & Wakefield', 'Colliers', 'Marcus & Millichap', 'Realogy', 'Compass', 'Zillow', 'Redfin'
        ],
        'Industrial': [
            'Boeing', 'Lockheed Martin', 'Raytheon', 'Northrop Grumman', 'General Dynamics', 'Honeywell',
            'General Electric', 'Caterpillar', 'Deere & Company', 'Illinois Tool Works', '3M Company',
            'Emerson Electric', 'Parker-Hannifin', 'Eaton Corporation', 'Ingersoll Rand', 'Stanley Black & Decker',
            'Fastenal', 'W.W. Grainger', 'MSC Industrial', 'Cintas', 'Waste Management', 'Republic Services',
            'Rollins', 'Pentair', 'A.O. Smith', 'Xylem', 'Danaher Corporation', 'Fortive', 'Roper Technologies'
        ]
    }

def generate_news_headline_and_link(company, news_type, sentiment):
    """Generate realistic news headlines and links for companies"""
    
    # Company symbol mapping for more realistic URLs
    company_symbols = {
        'Apple': 'AAPL', 'Microsoft': 'MSFT', 'Google': 'GOOGL', 'Amazon': 'AMZN',
        'Tesla': 'TSLA', 'Meta': 'META', 'Netflix': 'NFLX', 'IBM': 'IBM',
        'JPMorgan Chase': 'JPM', 'Bank of America': 'BAC', 'Wells Fargo': 'WFC',
        'Goldman Sachs': 'GS', 'Johnson & Johnson': 'JNJ', 'Pfizer': 'PFE',
        'ExxonMobil': 'XOM', 'Chevron': 'CVX', 'Coca-Cola': 'KO', 'PepsiCo': 'PEP'
    }
    
    symbol = company_symbols.get(company, company.replace(' ', '').upper()[:4])
    
    # News headline templates based on type and sentiment
    headlines = {
        'Earnings': {
            'Positive': [
                f"{company} Reports Strong Q3 Earnings, Beats Wall Street Expectations",
                f"{company} Delivers Record Quarterly Revenue Growth",
                f"{company} Exceeds Profit Forecasts in Latest Earnings Report"
            ],
            'Negative': [
                f"{company} Misses Earnings Estimates, Stock Falls",
                f"{company} Reports Disappointing Quarterly Results",
                f"{company} Faces Revenue Decline in Latest Quarter"
            ],
            'Neutral': [
                f"{company} Releases Q3 Financial Results",
                f"{company} Reports Mixed Quarterly Performance",
                f"{company} Announces Quarterly Earnings Update"
            ]
        },
        'Product Launch': {
            'Positive': [
                f"{company} Unveils Revolutionary New Product Line",
                f"{company} Launches Innovative Technology Solution",
                f"{company} Introduces Game-Changing Product Innovation"
            ],
            'Negative': [
                f"{company} Product Launch Faces Technical Issues",
                f"{company} Delays Major Product Release",
                f"{company} New Product Receives Mixed Market Response"
            ],
            'Neutral': [
                f"{company} Announces New Product Development",
                f"{company} Reveals Upcoming Product Portfolio",
                f"{company} Updates Product Roadmap"
            ]
        },
        'Market Analysis': {
            'Positive': [
                f"Analysts Upgrade {company} Stock Rating",
                f"{company} Shows Strong Market Position",
                f"Bullish Outlook for {company} Shares"
            ],
            'Negative': [
                f"Market Concerns Over {company} Performance",
                f"Analysts Downgrade {company} Stock",
                f"{company} Faces Market Headwinds"
            ],
            'Neutral': [
                f"Market Analysis: {company} Stock Review",
                f"{company} Market Performance Update",
                f"Investment Analysis: {company} Outlook"
            ]
        },
        'Merger': {
            'Positive': [
                f"{company} Announces Strategic Merger Deal",
                f"{company} Completes Major Acquisition",
                f"{company} Merger Creates Market Leader"
            ],
            'Negative': [
                f"{company} Merger Talks Fall Through",
                f"{company} Acquisition Faces Regulatory Issues",
                f"{company} Merger Delayed Due to Complications"
            ],
            'Neutral': [
                f"{company} Explores Merger Opportunities",
                f"{company} Merger Under Review",
                f"{company} Announces Merger Discussions"
            ]
        }
    }
    
    # Default headlines for other news types
    default_headlines = {
        'Positive': f"{company} Shows Strong Performance",
        'Negative': f"{company} Faces Challenges",
        'Neutral': f"{company} Business Update"
    }
    
    # Select headline
    if news_type in headlines:
        headline = np.random.choice(headlines[news_type][sentiment])
    else:
        headline = default_headlines[sentiment]
    
    # Generate realistic news links
    sources_urls = {
        'Reuters': f"https://www.reuters.com/business/{symbol.lower()}-{news_type.lower()}-{datetime.now().strftime('%Y-%m-%d')}",
        'Bloomberg': f"https://www.bloomberg.com/news/articles/{datetime.now().strftime('%Y-%m-%d')}/{symbol.lower()}-{news_type.lower()}",
        'CNBC': f"https://www.cnbc.com/{datetime.now().strftime('%Y/%m/%d')}/{symbol.lower()}-{news_type.lower()}.html",
        'Financial Times': f"https://www.ft.com/content/{symbol.lower()}-{news_type.lower()}-{datetime.now().strftime('%Y%m%d')}",
        'Wall Street Journal': f"https://www.wsj.com/articles/{symbol.lower()}-{news_type.lower()}-{datetime.now().strftime('%Y%m%d')}"
    }
    
    source = np.random.choice(list(sources_urls.keys()))
    link = sources_urls[source]
    
    return headline, link

def generate_sample_news_data(selected_companies=None):
    """Generate sample financial news data for demonstration"""
    company_db = get_company_database()
    
    # Define news types and sentiments
    news_types = ['Earnings', 'Product Launch', 'Market Analysis', 'Merger', 'Partnership', 'Regulation', 
                  'IPO', 'Acquisition', 'Dividend', 'Stock Split', 'Guidance Update', 'Leadership Change']
    sentiments = ['Positive', 'Negative', 'Neutral']
    
    # If specific companies are selected, use ONLY them
    if selected_companies and len(selected_companies) > 0:
        # Set seed for reproducible results based on selected companies
        seed_value = hash(tuple(sorted(selected_companies))) % 10000
        np.random.seed(seed_value)
        
        target_companies = selected_companies
        # Generate guaranteed news for each selected company
        news_per_company = 8
        
        data = []
        
        # Ensure each selected company gets exactly the specified amount of news
        for company in target_companies:
            for i in range(news_per_company):
                date = datetime.now() - timedelta(days=np.random.randint(0, 30))
                news_type = np.random.choice(news_types)
                sentiment = np.random.choice(sentiments)
                
                # Generate sentiment score based on sentiment
                if sentiment == 'Positive':
                    score = np.random.uniform(0.5, 1.0)
                elif sentiment == 'Negative':
                    score = np.random.uniform(-1.0, -0.5)
                else:
                    score = np.random.uniform(-0.2, 0.2)
                
                # Generate realistic news headlines and links
                news_headline, news_link = generate_news_headline_and_link(company, news_type, sentiment)
                
                data.append({
                    'Date': date.strftime('%Y-%m-%d'),
                    'Company': company,  # Exact company name from selection
                    'News_Type': news_type,
                    'Sentiment': sentiment,
                    'Sentiment_Score': score,
                    'Impact_Score': np.random.uniform(0.1, 1.0),
                    'Source': np.random.choice(['Reuters', 'Bloomberg', 'CNBC', 'Financial Times', 'Wall Street Journal']),
                    'Headline': news_headline,
                    'News_Link': news_link
                })
        
        # Reset seed
        np.random.seed(None)
    else:
        # If no specific selection, use all companies
        all_companies = []
        for category, companies in company_db.items():
            all_companies.extend(companies)
        target_companies = all_companies[:50]  # Limit for performance
        news_count = 100
        
        data = []
        for i in range(news_count):
            date = datetime.now() - timedelta(days=np.random.randint(0, 30))
            company = np.random.choice(target_companies)
            news_type = np.random.choice(news_types)
            sentiment = np.random.choice(sentiments)
            
            # Generate sentiment score based on sentiment
            if sentiment == 'Positive':
                score = np.random.uniform(0.5, 1.0)
            elif sentiment == 'Negative':
                score = np.random.uniform(-1.0, -0.5)
            else:
                score = np.random.uniform(-0.2, 0.2)
            
            # Generate realistic news headlines and links
            news_headline, news_link = generate_news_headline_and_link(company, news_type, sentiment)
            
            data.append({
                'Date': date.strftime('%Y-%m-%d'),
                'Company': company,
                'News_Type': news_type,
                'Sentiment': sentiment,
                'Sentiment_Score': score,
                'Impact_Score': np.random.uniform(0.1, 1.0),
                'Source': np.random.choice(['Reuters', 'Bloomberg', 'CNBC', 'Financial Times', 'Wall Street Journal']),
                'Headline': news_headline,
                'News_Link': news_link
            })
    
    return pd.DataFrame(data)


def categorize_news(title: str) -> str:
    """Assign a transparent keyword category to a provider headline."""
    normalized = title.lower()
    if any(word in normalized for word in ('earnings', 'revenue', 'guidance', 'quarter')):
        return 'Earnings'
    if any(word in normalized for word in ('acquire', 'acquisition', 'merger', 'takeover')):
        return 'Merger & Acquisition'
    if any(word in normalized for word in ('ceo', 'cfo', 'executive', 'appoints')):
        return 'Leadership Change'
    if any(word in normalized for word in ('regulator', 'sec ', 'lawsuit', 'antitrust')):
        return 'Regulatory Update'
    return 'Market Analysis'


@st.cache_data(ttl=300, show_spinner=False)
def load_live_news(companies):
    """Fetch provider articles and derive sentiment from their actual text."""
    analyzer = FinancialSentimentAnalyzer()
    rows = []
    seen_links = set()
    for company in companies:
        for article in YahooFinanceService.search_news(company):
            score = analyzer.analyze_text(f"{article['title']} {article['summary']}").score
            sentiment = 'Positive' if score > 0.2 else 'Negative' if score < -0.2 else 'Neutral'
            if not article['link'] or article['link'] in seen_links:
                continue
            seen_links.add(article['link'])
            rows.append({
                'Date': article['published_at'].date().isoformat(),
                'Company': article['company'],
                'News_Type': categorize_news(article['title']),
                'Sentiment': sentiment,
                'Sentiment_Score': round(score, 3),
                'Impact_Score': round(min(abs(score), 1.0), 3),
                'Source': article['source'],
                'Headline': article['title'],
                'News_Link': article['link'],
                'Data_Source': article['data_source'],
            })
    return pd.DataFrame(rows)

def create_sentiment_chart(df):
    """Create sentiment analysis chart"""
    sentiment_counts = df['Sentiment'].value_counts()
    
    fig = go.Figure(data=[
        go.Bar(
            x=sentiment_counts.index,
            y=sentiment_counts.values,
            marker_color=['#00D4AA', '#FF6B6B', '#4ECDC4'],
            text=sentiment_counts.values,
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="News Sentiment Distribution",
        xaxis_title="Sentiment",
        yaxis_title="Number of Articles",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=False
    )
    
    return fig

def create_timeline_chart(df):
    """Create sentiment timeline chart"""
    df_timeline = df.groupby(['Date', 'Sentiment']).size().reset_index(name='Count')
    
    fig = px.line(
        df_timeline, 
        x='Date', 
        y='Count', 
        color='Sentiment',
        title="Sentiment Timeline",
        color_discrete_map={
            'Positive': '#00D4AA',
            'Negative': '#FF6B6B',
            'Neutral': '#4ECDC4'
        }
    )
    
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    return fig

def create_company_sentiment_chart(df):
    """Create company-wise sentiment analysis"""
    company_sentiment = df.groupby(['Company', 'Sentiment']).size().unstack(fill_value=0)
    
    fig = go.Figure()
    
    for sentiment in ['Positive', 'Negative', 'Neutral']:
        if sentiment in company_sentiment.columns:
            color = {'Positive': '#00D4AA', 'Negative': '#FF6B6B', 'Neutral': '#4ECDC4'}[sentiment]
            fig.add_trace(go.Bar(
                name=sentiment,
                x=company_sentiment.index,
                y=company_sentiment[sentiment],
                marker_color=color
            ))
    
    fig.update_layout(
        title="Company-wise Sentiment Analysis",
        xaxis_title="Company",
        yaxis_title="Number of Articles",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        barmode='stack'
    )
    
    return fig

def main():
    """Main function for Financial Analysis page"""
    load_custom_css()
    apply_design_system()

    if st.sidebar.button("↻ Refresh live news", use_container_width=True):
        load_live_news.clear()
        st.session_state.pop('cached_df', None)
        st.rerun()
    
    render_page_header(
        "Financial news, made actionable",
        "Follow selected companies, compare the current news tone, and open each original source before deciding what matters.",
        eyebrow="Research desk",
        badges=["Source links included", "Keyword sentiment", "Company-first workflow"],
    )

    st.caption(
        "News source: Yahoo Finance via yfinance. Sentiment is a transparent keyword baseline, "
        "not investment advice."
    )
    
    # Quick tips for new users
    if not st.session_state.get('tips_dismissed', False):
        tip_col1, tip_col2 = st.columns([4, 1])
        
        with tip_col1:
            st.info("💡 **New here?** Start with 🔥 Popular button in sidebar, then select 🎯 Top Companies for instant analysis!")
        
        with tip_col2:
            if st.button("✖️ Dismiss", key="dismiss_tips"):
                st.session_state.tips_dismissed = True
                st.rerun()
    
    # Help section
    with st.expander("ℹ️ How to Use This Page", expanded=False):
        st.markdown("""
        ### 🚀 Quick Start Guide
        
        **1. Choose Industry Categories:**
        - Use the quick selection buttons (Popular, All Markets, Healthcare, Energy)
        - Or manually select from the dropdown list
        
        **2. Select Companies:**
        - **🎯 Top Companies:** Automatically selects top performers
        - **⭐ Popular Picks:** Pre-selected famous companies  
        - **🔍 Custom Selection:** Search and pick specific companies
        
        **3. Advanced Filtering:**
        - Filter by news types (Earnings, Mergers, etc.)
        - Choose sentiment (Positive, Negative, Neutral)
        - Set impact score levels
        
        **4. Analysis Results:**
        - View key metrics and trends
        - Interactive charts and visualizations
        - Detailed news sentiment analysis
        
        💡 **Tip:** Start with "Popular Picks" for a quick overview!
        """)
    
    # Get company database
    company_db = get_company_database()

    if 'active_companies' not in st.session_state:
        st.session_state.active_companies = [
            'Apple', 'Microsoft', 'Google', 'Amazon', 'Meta', 'Tesla'
        ]
    
    # Sidebar filters
    st.sidebar.header("🔍 Analysis Filters")
    
    # Quick preset buttons with improved layout and functionality
    st.sidebar.markdown("### 🚀 Quick Selection")
    
    # Create 2x2 button layout
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("🔥 Popular", key="popular", use_container_width=True, 
                    help="Technology & Finance sectors"):
            # Clear any existing selections first
            for key in list(st.session_state.keys()):
                if key.startswith(('multi_', 'browse_')):
                    del st.session_state[key]
            st.session_state.selected_categories = ['Technology', 'Finance']
            st.session_state.active_companies = [
                'Apple', 'Microsoft', 'Google', 'Amazon', 'Meta', 'JPMorgan Chase'
            ]
            st.session_state.preset_applied = True
            st.sidebar.success("✅ Popular sectors selected!")
            st.rerun()
    
    with col2:
        if st.button("📈 All Markets", key="all_markets", use_container_width=True,
                    help="All industry sectors"):
            # Clear any existing selections first
            for key in list(st.session_state.keys()):
                if key.startswith(('multi_', 'browse_')):
                    del st.session_state[key]
            st.session_state.selected_categories = list(company_db.keys())
            st.session_state.active_companies = [
                'Apple', 'JPMorgan Chase', 'Johnson & Johnson', 'ExxonMobil',
                'Walmart', 'Tesla', 'American Tower', 'Boeing'
            ]
            st.session_state.preset_applied = True
            st.sidebar.success("✅ All markets selected!")
            st.rerun()
    
    col3, col4 = st.sidebar.columns(2)
    
    with col3:
        if st.button("💊 Healthcare", key="healthcare", use_container_width=True,
                    help="Healthcare & Pharmaceutical companies"):
            # Clear any existing selections first
            for key in list(st.session_state.keys()):
                if key.startswith(('multi_', 'browse_')):
                    del st.session_state[key]
            st.session_state.selected_categories = ['Healthcare']
            st.session_state.active_companies = ['Johnson & Johnson', 'Pfizer', 'Merck', 'Abbott Laboratories']
            st.session_state.preset_applied = True
            st.sidebar.success("✅ Healthcare selected!")
            st.rerun()
    
    with col4:
        if st.button("⚡ Energy", key="energy", use_container_width=True,
                    help="Energy & Oil companies"):
            # Clear any existing selections first
            for key in list(st.session_state.keys()):
                if key.startswith(('multi_', 'browse_')):
                    del st.session_state[key]
            st.session_state.selected_categories = ['Energy']
            st.session_state.active_companies = ['ExxonMobil', 'Chevron', 'ConocoPhillips', 'NextEra Energy']
            st.session_state.preset_applied = True
            st.sidebar.success("✅ Energy selected!")
            st.rerun()
    
    # Initialize session state
    if 'selected_categories' not in st.session_state:
        st.session_state.selected_categories = ['Technology', 'Finance', 'Healthcare']
    
    # Use session state for categories if preset was applied
    default_categories = st.session_state.selected_categories if 'preset_applied' in st.session_state else ['Technology', 'Finance', 'Healthcare']
    
    selected_categories = st.sidebar.multiselect(
        "🏢 Industries",
        options=list(company_db.keys()),
        default=default_categories,
        help="Choose industry sectors for analysis"
    )
    
    # Update session state
    st.session_state.selected_categories = selected_categories
    
    # Clear preset flag
    if 'preset_applied' in st.session_state:
        del st.session_state.preset_applied
    
    # Get companies from selected categories
    available_companies = []
    for category in selected_categories:
        available_companies.extend(company_db[category])
    
    # Date range filter
    date_range = st.sidebar.date_input(
        "📅 Date Range",
        value=[datetime.now() - timedelta(days=30), datetime.now()],
        max_value=datetime.now(),
        help="Choose time period for news analysis"
    )
    
    # Smart company selection
    st.sidebar.markdown("### 🏭 Company Selection")
    
    # Global search box for all companies
    search_term = st.sidebar.text_input(
        "🔍 Quick Search",
        placeholder="Type any company name (IBM, Apple, Tesla...)",
        help="Search across all companies and categories"
    )
    
    # Get all available companies from database
    all_available_companies = []
    for category in company_db.keys():
        all_available_companies.extend(company_db[category])
    
    # Filter companies based on search
    if search_term:
        filtered_companies = [comp for comp in all_available_companies 
                            if search_term.lower() in comp.lower()]
        st.sidebar.info(f"🎯 Found {len(filtered_companies)} companies matching '{search_term}'")
        
        # Show search results
        if filtered_companies:
            st.sidebar.markdown("**Search Results:**")
            search_selected = st.sidebar.multiselect(
                "Select from search results",
                options=filtered_companies,
                default=[],
                help="Choose companies from search results"
            )
        else:
            st.sidebar.warning("No companies found. Try different keywords.")
            search_selected = []
    else:
        search_selected = []
    
    # Category-based selection
    st.sidebar.markdown("### 📂 Browse by Category")
    
    # Quick selection buttons with proper session state handling
    st.sidebar.markdown("**🚀 Quick Picks:**")
    
    # Create 2x2 grid for better layout
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("🔥 Tech Giants", key="tech_giants", use_container_width=True, 
                    help="Apple, Microsoft, Google, Amazon, Meta, Tesla"):
            # Clear existing selections
            for key in list(st.session_state.keys()):
                if key.startswith('multi_'):
                    del st.session_state[key]
            # Set new selection
            st.session_state.active_companies = ['Apple', 'Microsoft', 'Google', 'Amazon', 'Meta', 'Tesla']
            st.rerun()
    
    with col2:
        if st.button("🏦 Finance", key="finance_top", use_container_width=True,
                    help="JPMorgan Chase, Bank of America, Wells Fargo, Goldman Sachs"):
            # Clear existing selections
            for key in list(st.session_state.keys()):
                if key.startswith('multi_'):
                    del st.session_state[key]
            # Set new selection
            st.session_state.active_companies = ['JPMorgan Chase', 'Bank of America', 'Wells Fargo', 'Goldman Sachs']
            st.rerun()
    
    col3, col4 = st.sidebar.columns(2)
    
    with col3:
        if st.button("💊 Healthcare", key="healthcare_pick", use_container_width=True,
                    help="Johnson & Johnson, Pfizer, Merck, Abbott"):
            # Clear existing selections
            for key in list(st.session_state.keys()):
                if key.startswith('multi_'):
                    del st.session_state[key]
            # Set new selection
            st.session_state.active_companies = ['Johnson & Johnson', 'Pfizer', 'Merck', 'Abbott Laboratories']
            st.rerun()
    
    with col4:
        if st.button("⚡ Energy", key="energy_pick", use_container_width=True,
                    help="ExxonMobil, Chevron, ConocoPhillips"):
            # Clear existing selections
            for key in list(st.session_state.keys()):
                if key.startswith('multi_'):
                    del st.session_state[key]
            # Set new selection
            st.session_state.active_companies = ['ExxonMobil', 'Chevron', 'ConocoPhillips', 'NextEra Energy']
            st.rerun()
    
    active_selection = st.session_state.active_companies
    
    # Category selection for detailed browsing (only if no search or quick selection)
    if not search_term:
        st.sidebar.markdown("**🗂️ Browse by Industry:**")
        
        browse_categories = st.sidebar.multiselect(
            "Select industries to explore",
            options=list(company_db.keys()),
            default=['Technology'] if not selected_categories else selected_categories[:2],
            help="Choose industry sectors to browse companies",
            key="browse_industries"
        )
        
        # Show companies from selected categories in a more compact way
        category_selected = []
        if browse_categories:
            for category in browse_categories:
                category_companies = company_db[category]
                
                with st.sidebar.expander(f"📂 {category} ({len(category_companies)} companies)", expanded=False):
                    # Add select all/none buttons for each category
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button("✅ All", key=f"all_{category}", use_container_width=True,
                                   help=f"Select all {category} companies"):
                            st.session_state[f"multi_{category}"] = category_companies
                            st.rerun()
                    with col_b:
                        if st.button("❌ None", key=f"none_{category}", use_container_width=True,
                                   help=f"Deselect all {category} companies"):
                            st.session_state[f"multi_{category}"] = []
                            st.rerun()
                    
                    # Multiselect for companies in this category
                    selected_from_category = st.multiselect(
                        f"Companies in {category}:",
                        options=category_companies,
                        default=st.session_state.get(f"multi_{category}", []),
                        key=f"multi_{category}",
                        help=f"Choose specific companies from {category} sector"
                    )
                    category_selected.extend(selected_from_category)
    else:
        category_selected = []
    
    # Combine selections
    selected_companies = list(dict.fromkeys(active_selection + search_selected + category_selected))
    
    # Show current selection
    if selected_companies:
        st.sidebar.success(f"✅ {len(selected_companies)} companies selected")
        with st.sidebar.expander("📋 Selected Companies", expanded=False):
            for i, comp in enumerate(selected_companies[:10], 1):
                st.markdown(f"{i}. **{comp}**")
            if len(selected_companies) > 10:
                st.caption(f"... and {len(selected_companies) - 10} more")
        
        # Clear selection button with confirmation
        if st.sidebar.button("🗑️ Clear All Selections", use_container_width=True, 
                            type="secondary", help="Clear all selected companies"):
            # Clear all related session state
            keys_to_clear = [key for key in st.session_state.keys() 
                           if key.startswith(('multi_', 'company_', 'browse_'))]
            for key in keys_to_clear:
                del st.session_state[key]
            st.session_state.active_companies = []
            st.sidebar.success("✅ All selections cleared!")
            st.rerun()
    else:
        st.sidebar.warning("⚠️ No companies selected")
        st.sidebar.info("💡 Use search box or browse categories to select companies")
    
    # Retrieve linked provider news only for user-selected companies. A failed
    # request is shown as a failed request; no simulated article is substituted.
    if 'last_selected_companies' not in st.session_state:
        st.session_state.last_selected_companies = []
    
    # Only regenerate if companies changed or no cache exists
    if (selected_companies != st.session_state.last_selected_companies or
        'cached_df' not in st.session_state or
        ('Data_Source' not in st.session_state.cached_df.columns if 'cached_df' in st.session_state else False)):
        
        if 'cached_df' in st.session_state:
            del st.session_state.cached_df
        if not selected_companies:
            df = pd.DataFrame()
        else:
            requested_companies = tuple(selected_companies[:6])
            try:
                with st.spinner("Loading linked financial news..."):
                    df = load_live_news(requested_companies)
            except LiveDataUnavailable as exc:
                st.error(f"Live news is currently unavailable: {exc}")
                return
            if len(selected_companies) > len(requested_companies):
                st.info("To protect the live provider, this refresh analyzes the first 6 selected companies.")
        st.session_state.last_selected_companies = selected_companies.copy() if selected_companies else []
        st.session_state.cached_df = df
        
        # Clear any filter states that might be invalid now
        if 'selected_news_types' in st.session_state:
            del st.session_state.selected_news_types
        if 'selected_sentiments' in st.session_state:
            del st.session_state.selected_sentiments
    else:
        df = st.session_state.cached_df

    if not selected_companies:
        st.info("👆 Select one or more companies from the sidebar to load linked news articles.")
        return
    
    if df.empty and selected_companies:
        st.warning("No linked news articles were returned for the selected companies. Try another company or refresh later.")
        return

    # Show provider coverage for the active selection.
    if selected_companies:
        st.sidebar.markdown("### 📊 Data Summary")
        generated_companies = list(df['Company'].unique())
        st.sidebar.markdown(f"**Articles returned for:** {len(generated_companies)} companies")
        
        # Show exact matching
        st.sidebar.markdown("### ✅ Company Matching Check")
        for selected in selected_companies:
            if selected in generated_companies:
                count = len(df[df['Company'] == selected])
                st.sidebar.markdown(f"✅ **{selected}**: {count} source articles")
            else:
                st.sidebar.markdown(f"❌ **{selected}**: NO DATA FOUND!")
        
        # Show if any unexpected companies appeared
        unexpected = [comp for comp in generated_companies if comp not in selected_companies]
        if unexpected:
            st.sidebar.markdown("### ⚠️ Unexpected Companies:")
            for comp in unexpected[:3]:
                count = len(df[df['Company'] == comp])
                st.sidebar.markdown(f"❓ **{comp}**: {count} news")
        else:
            st.sidebar.markdown("### ✅ Selected-company coverage")
            st.sidebar.markdown("All displayed articles were returned for selected companies.")
    
    # Quick news headlines in sidebar
    if selected_companies and not df.empty:
        with st.sidebar.expander("📰 Latest Headlines", expanded=True):
            latest_news = df.sort_values('Date', ascending=False).head(5)
            for idx, row in latest_news.iterrows():
                sentiment_emoji = "🟢" if row['Sentiment'] == 'Positive' else "🔴" if row['Sentiment'] == 'Negative' else "🟡"
                st.markdown(f"""
                <div style="
                    background: #f8f9fa;
                    padding: 8px;
                    border-radius: 5px;
                    margin: 5px 0;
                    border-left: 3px solid {'#28a745' if row['Sentiment'] == 'Positive' else '#dc3545' if row['Sentiment'] == 'Negative' else '#ffc107'};
                ">
                    <small><strong>{escape(str(row['Company']))}</strong></small><br>
                    <small>{sentiment_emoji} {escape(str(row['Headline']))[:60]}...</small><br>
                    <small style="color: #666;">{escape(str(row['Source']))} • {row['Date']}</small>
                </div>
                """, unsafe_allow_html=True)
                
                # Add link button for each headline
                if st.button(f"📖 Read", key=f"sidebar_link_{idx}", help="Read full article"):
                    st.markdown(f"**🔗 Article Link:** [{row['Source']}]({row['News_Link']})")
    
    # Advanced filters in expander
    with st.sidebar.expander("🔧 Advanced", expanded=False):
        st.markdown("### 📰 News Filters")
        
        # News type filter with better UX
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 All News", key="all_news", use_container_width=True):
                st.session_state.selected_news_types = list(df['News_Type'].unique())
        
        with col2:
            if st.button("💼 Business Only", key="business_news", use_container_width=True):
                st.session_state.selected_news_types = ['Earnings', 'Merger', 'Acquisition']
        
        # Initialize news types
        if 'selected_news_types' not in st.session_state:
            st.session_state.selected_news_types = list(df['News_Type'].unique())
        
        selected_news_types = st.multiselect(
            "📝 News Types",
            options=df['News_Type'].unique(),
            default=st.session_state.selected_news_types,
            help="Filter by type of financial news"
        )
        st.session_state.selected_news_types = selected_news_types
        
        st.markdown("### 😊 Sentiment Filters")
        
        # Sentiment filter with visual indicators
        sentiment_options = {
            "📈 Positive": "Positive",
            "📉 Negative": "Negative", 
            "😐 Neutral": "Neutral"
        }
        
        selected_sentiment_keys = st.multiselect(
            "Sentiment Types",
            options=list(sentiment_options.keys()),
            default=list(sentiment_options.keys()),
            help="Filter by news sentiment"
        )
        
        selected_sentiments = [sentiment_options[key] for key in selected_sentiment_keys]
        
        st.markdown("### 🎯 Sentiment Range")
        
        # Impact score filter with better visualization
        impact_range = st.select_slider(
            "Sentiment Range",
            options=[
                "Very Negative (-1.0 to -0.6)",
                "Negative (-0.6 to -0.2)", 
                "Neutral (-0.2 to +0.2)",
                "Positive (+0.2 to +0.6)",
                "Very Positive (+0.6 to +1.0)",
                "All Levels"
            ],
            value="All Levels",
            help="Filter by the explainable sentiment score"
        )
        
        # Convert impact range to numeric values
        if impact_range == "Very Negative (-1.0 to -0.6)":
            min_impact, max_impact = -1.0, -0.6
        elif impact_range == "Negative (-0.6 to -0.2)":
            min_impact, max_impact = -0.6, -0.2
        elif impact_range == "Neutral (-0.2 to +0.2)":
            min_impact, max_impact = -0.2, 0.2
        elif impact_range == "Positive (+0.2 to +0.6)":
            min_impact, max_impact = 0.2, 0.6
        elif impact_range == "Very Positive (+0.6 to +1.0)":
            min_impact, max_impact = 0.6, 1.0
        else:  # All Levels
            min_impact, max_impact = -1.0, 1.0
        
        # Show current filter summary
        st.markdown("---")
        st.markdown("### 📋 Filter Summary")
        st.info(f"""
        **Companies:** {len(selected_companies) if selected_companies else 0}  
        **News Types:** {len(selected_news_types)}  
        **Sentiments:** {len(selected_sentiments)}  
        **Sentiment range:** {impact_range}
        """)
        
        # Reset filters button
        if st.button("🔄 Reset All Filters", use_container_width=True):
            # Clear all session state
            keys_to_clear = [key for key in st.session_state.keys() 
                           if key.startswith(('company_', 'selected_'))]
            for key in keys_to_clear:
                del st.session_state[key]
            st.rerun()
    
    # Filter data
    df_filtered = df.copy()

    if len(date_range) == 2:
        start_date, end_date = date_range
        dates = pd.to_datetime(df_filtered['Date'], errors='coerce').dt.date
        df_filtered = df_filtered[(dates >= start_date) & (dates <= end_date)]
    
    if selected_companies:
        df_filtered = df_filtered[df_filtered['Company'].isin(selected_companies)]
    
    if selected_news_types:
        df_filtered = df_filtered[df_filtered['News_Type'].isin(selected_news_types)]
    
    if selected_sentiments:
        df_filtered = df_filtered[df_filtered['Sentiment'].isin(selected_sentiments)]
    
    # Filter by impact score
    df_filtered = df_filtered[
        (df_filtered['Sentiment_Score'] >= min_impact) & 
        (df_filtered['Sentiment_Score'] <= max_impact)
    ]
    
    # Check if any data remains after filtering
    if df_filtered.empty:
        st.warning("⚠️ No data found with current filters!")
        st.markdown("""
        ### 💡 Suggestions:
        - Try selecting more **industry categories**
        - Choose **"All Markets"** for broader analysis  
        - Use **"Top Companies"** selection mode
        - Expand the **date range**
        - Reset filters using the **🔄 Reset All Filters** button
        """)
        return
    
    if not selected_companies:
        st.info("👆 Please select companies from the sidebar to start analysis")
        st.markdown("""
        ### 🚀 Quick Start:
        1. Click **🔥 Popular** for most traded companies
        2. Or click **📈 All Markets** for comprehensive view
        3. Or choose **🎯 Top Companies** for auto-selection
        """)
        return
    
    # Show which companies actually have data
    companies_with_data = list(df_filtered['Company'].unique())
    selected_companies_with_data = [comp for comp in selected_companies if comp in companies_with_data]
    
    if not selected_companies_with_data:
        st.error("❌ None of the selected companies have data in the current filters!")
        st.markdown(f"""
        **Selected Companies:** {', '.join(selected_companies)}  
        **Companies with Data:** {', '.join(companies_with_data[:10])}
        """)
        return
    
    # Display analysis summary
    st.success(f"✅ Analyzing {len(selected_companies_with_data)} companies: {', '.join(selected_companies_with_data[:5])}" + 
               (f" and {len(selected_companies_with_data)-5} more" if len(selected_companies_with_data) > 5 else ""))
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card summary-card sentiment-positive">
            <h3>📈 Positive News</h3>
            <h2>{}</h2>
            <p>Articles with positive sentiment</p>
        </div>
        """.format(len(df_filtered[df_filtered['Sentiment'] == 'Positive'])), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card summary-card sentiment-negative">
            <h3>📉 Negative News</h3>
            <h2>{}</h2>
            <p>Articles with negative sentiment</p>
        </div>
        """.format(len(df_filtered[df_filtered['Sentiment'] == 'Negative'])), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card summary-card sentiment-neutral">
            <h3>⚖️ Neutral News</h3>
            <h2>{}</h2>
            <p>Articles with neutral sentiment</p>
        </div>
        """.format(len(df_filtered[df_filtered['Sentiment'] == 'Neutral'])), unsafe_allow_html=True)
    
    with col4:
        avg_sentiment = df_filtered['Sentiment_Score'].mean()
        st.markdown("""
        <div class="metric-card summary-card">
            <h3>🎯 Avg Sentiment</h3>
            <h2>{:.2f}</h2>
            <p>Overall sentiment score</p>
        </div>
        """.format(avg_sentiment), unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(create_sentiment_chart(df_filtered), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(create_timeline_chart(df_filtered), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Company analysis
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.plotly_chart(create_company_sentiment_chart(df_filtered), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent news from the selected live provider.
    st.subheader("Latest coverage")
    
    # Display filtered data with links
    if not df_filtered.empty:
        df_display = df_filtered.sort_values('Date', ascending=False).head(15)
        
        st.caption("Open an item to read it on the original publisher site.")
        
        for idx, row in df_display.iterrows():
            sentiment = str(row['Sentiment']).lower()
            sentiment_class = sentiment if sentiment in {"positive", "negative", "neutral"} else "neutral"
            headline = escape(str(row['Headline']))
            company = escape(str(row['Company']))
            source = escape(str(row['Source']))
            news_type = escape(str(row['News_Type']))
            article_url = escape(str(row['News_Link']), quote=True)
            article_date = escape(str(row['Date']))
            st.markdown(
                f'<article class="news-card {sentiment_class}">'
                f'<h4>{headline}</h4>'
                f'<div class="news-meta">{company} · {article_date} · {source} · {news_type}</div>'
                f'<div class="news-footer"><span class="sentiment-chip {sentiment_class}">'
                f'{escape(str(row["Sentiment"]))} sentiment · score {row["Sentiment_Score"]:.2f}'
                f'</span><a class="article-link" href="{article_url}" target="_blank" '
                f'rel="noopener noreferrer">Read original article ↗</a></div></article>',
                unsafe_allow_html=True,
            )
        
        # Traditional table view toggle
        with st.expander("📊 View as Data Table", expanded=False):
            st.dataframe(
                df_display[['Date', 'Company', 'Headline', 'News_Type', 'Sentiment', 'Sentiment_Score', 'Source', 'News_Link']],
                use_container_width=True,
                column_config={
                    "News_Link": st.column_config.LinkColumn(
                        "Article Link",
                        help="Click to read full article",
                        validate="^https://.*",
                        max_chars=100,
                        display_text="🔗 Read Article"
                    ),
                    "Headline": st.column_config.TextColumn(
                        "News Headline",
                        width="large",
                        help="News article headline"
                    )
                }
            )
    else:
        st.warning("No data available for the selected filters.")
    
    # Analysis insights
    st.subheader("💡 Key Insights")
    
    insights_col1, insights_col2 = st.columns(2)
    
    with insights_col1:
        st.markdown("""
        <div class="metric-card">
            <h4>🔍 Sentiment Analysis Summary</h4>
            <ul>
                <li>Most covered company: <strong>{}</strong></li>
                <li>Dominant sentiment: <strong>{}</strong></li>
                <li>Average sentiment score: <strong>{:.2f}</strong></li>
                <li>Total articles analyzed: <strong>{}</strong></li>
            </ul>
        </div>
        """.format(
            df_filtered['Company'].value_counts().index[0] if not df_filtered.empty else "N/A",
            df_filtered['Sentiment'].value_counts().index[0] if not df_filtered.empty else "N/A",
            df_filtered['Sentiment_Score'].mean() if not df_filtered.empty else 0,
            len(df_filtered)
        ), unsafe_allow_html=True)
    
    with insights_col2:
        st.markdown("""
        <div class="metric-card">
            <h4>📊 Sentiment Signal Summary</h4>
            <ul>
                <li>High absolute-sentiment news: <strong>{}%</strong></li>
                <li>Most active news type: <strong>{}</strong></li>
                <li>Top news source: <strong>{}</strong></li>
                <li>Sentiment volatility: <strong>{}</strong></li>
            </ul>
        </div>
        """.format(
            int((df_filtered['Impact_Score'] > 0.7).sum() / len(df_filtered) * 100) if not df_filtered.empty else 0,
            df_filtered['News_Type'].value_counts().index[0] if not df_filtered.empty else "N/A",
            df_filtered['Source'].value_counts().index[0] if not df_filtered.empty else "N/A",
            "High" if df_filtered['Sentiment_Score'].std() > 0.5 else "Moderate" if not df_filtered.empty else "N/A"
        ), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
