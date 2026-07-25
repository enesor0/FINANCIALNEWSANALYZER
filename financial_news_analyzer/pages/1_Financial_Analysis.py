"""
Financial News Analysis Page
Provider-linked financial news with explainable sentiment scoring
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import importlib
from html import escape
from pathlib import Path

repository_root = Path(__file__).resolve().parents[2]
if str(repository_root) not in sys.path:
    sys.path.insert(0, str(repository_root))

from financial_news_analyzer.src.application.exceptions import DataProviderUnavailable
from financial_news_analyzer.src.presentation import design_system
from financial_news_analyzer.src.presentation.app_shell import render_app_shell
from financial_news_analyzer.src.presentation.dependencies import get_application_services

design_system = importlib.reload(design_system)
apply_design_system = design_system.apply_design_system
render_page_header = design_system.render_page_header

# Page configuration
st.set_page_config(
    page_title="News Research · Financial News Analyzer",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

@st.cache_data(ttl=300, show_spinner=False)
def load_live_news(companies):
    """Adapt application results to the tabular representation used by this view."""
    rows = []
    analyses = get_application_services().analyze_financial_news.execute(companies)
    for analysis in analyses:
        article = analysis.article
        if not article.url:
            continue
        score = analysis.sentiment.score
        sentiment = 'Positive' if score > 0.2 else 'Negative' if score < -0.2 else 'Neutral'
        rows.append({
            'Date': article.published_at.date().isoformat(),
            'Company': article.company,
            'News_Type': analysis.category.value,
            'Sentiment': sentiment,
            'Sentiment_Score': round(score, 3),
            'Impact_Score': round(analysis.impact_score, 3),
            'Source': article.source,
            'Headline': article.title,
            'News_Link': article.url,
            'Data_Source': 'Yahoo Finance via yfinance',
        })
    return pd.DataFrame(rows)

def create_sentiment_chart(df):
    """Create sentiment analysis chart"""
    sentiment_counts = df['Sentiment'].value_counts()
    sentiment_colors = {
        'Positive': '#10B981',
        'Negative': '#F43F5E',
        'Neutral': '#94A3B8',
    }
    
    fig = go.Figure(data=[
        go.Bar(
            x=sentiment_counts.index,
            y=sentiment_counts.values,
            marker_color=[sentiment_colors[label] for label in sentiment_counts.index],
            text=sentiment_counts.values,
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="News Sentiment Distribution",
        xaxis_title="Sentiment",
        yaxis_title="Number of Articles",
        template="plotly_white",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#475569'),
        showlegend=False
    )
    
    return design_system.style_plotly_chart(fig)

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
            'Positive': '#10B981',
            'Negative': '#F43F5E',
            'Neutral': '#94A3B8'
        }
    )
    
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#475569')
    )
    
    return design_system.style_plotly_chart(fig)

def create_company_sentiment_chart(df):
    """Create company-wise sentiment analysis"""
    company_sentiment = df.groupby(['Company', 'Sentiment']).size().unstack(fill_value=0)
    
    fig = go.Figure()
    
    for sentiment in ['Positive', 'Negative', 'Neutral']:
        if sentiment in company_sentiment.columns:
            color = {'Positive': '#10B981', 'Negative': '#F43F5E', 'Neutral': '#94A3B8'}[sentiment]
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
        template="plotly_white",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#475569'),
        barmode='stack'
    )
    
    return design_system.style_plotly_chart(fig)

def main():
    """Main function for Financial Analysis page"""
    apply_design_system()
    render_app_shell("analysis")

    if st.sidebar.button("↻ Refresh live news", use_container_width=True):
        load_live_news.clear()
        st.session_state.pop('cached_df', None)
        st.rerun()
    
    render_page_header(
        "Turn headlines into a clearer market view.",
        "Build a focused company watchlist, compare the tone of recent coverage, and verify every signal at the original source.",
        eyebrow="News research",
        badges=["Original sources linked", "Explainable scoring", "Five-minute cache"],
    )

    st.caption(
        "News source: Yahoo Finance via yfinance. Sentiment is a transparent keyword baseline, "
        "not investment advice."
    )
    
    st.info("Start with a watchlist preset in the sidebar, or search for a company. Advanced article filters stay tucked away until you need them.")
    
    # Get company database
    company_db = get_company_database()

    if 'active_companies' not in st.session_state:
        st.session_state.active_companies = [
            'Apple', 'Microsoft', 'Google', 'Amazon', 'Meta', 'Tesla'
        ]
    
    # Sidebar filters
    st.sidebar.header("Research controls")
    st.sidebar.caption("Choose a watchlist, then refine the articles only if needed.")
    st.sidebar.markdown("### Industries")
    
    # Initialize session state
    if 'selected_categories' not in st.session_state:
        st.session_state.selected_categories = ['Technology', 'Finance', 'Healthcare']
    
    selected_categories = st.sidebar.multiselect(
        "Filter company browser",
        options=list(company_db.keys()),
        default=st.session_state.selected_categories,
        help="Choose industry sectors for analysis"
    )
    
    # Update session state
    st.session_state.selected_categories = selected_categories
    
    # Date range filter
    date_range = st.sidebar.date_input(
        "📅 Date Range",
        value=[datetime.now() - timedelta(days=30), datetime.now()],
        max_value=datetime.now(),
        help="Choose time period for news analysis"
    )
    
    # Smart company selection
    st.sidebar.markdown("### Companies")
    
    # Global search box for all companies
    search_term = st.sidebar.text_input(
        "Search all companies",
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
    st.sidebar.markdown("### Watchlist presets")
    
    # Quick selection buttons with proper session state handling
    # Create 2x2 grid for better layout
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("Tech leaders", key="tech_giants", use_container_width=True,
                    help="Apple, Microsoft, Google, Amazon, Meta, Tesla"):
            # Clear existing selections
            for key in list(st.session_state.keys()):
                if key.startswith('multi_'):
                    del st.session_state[key]
            # Set new selection
            st.session_state.active_companies = ['Apple', 'Microsoft', 'Google', 'Amazon', 'Meta', 'Tesla']
            st.rerun()
    
    with col2:
        if st.button("Financials", key="finance_top", use_container_width=True,
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
        if st.button("Healthcare", key="healthcare_pick", use_container_width=True,
                    help="Johnson & Johnson, Pfizer, Merck, Abbott"):
            # Clear existing selections
            for key in list(st.session_state.keys()):
                if key.startswith('multi_'):
                    del st.session_state[key]
            # Set new selection
            st.session_state.active_companies = ['Johnson & Johnson', 'Pfizer', 'Merck', 'Abbott Laboratories']
            st.rerun()
    
    with col4:
        if st.button("Energy", key="energy_pick", use_container_width=True,
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
        st.sidebar.markdown("### Custom watchlist")
        
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
            except DataProviderUnavailable as exc:
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
        generated_companies = list(df['Company'].unique())
        st.sidebar.markdown("### Coverage")
        st.sidebar.caption(
            f"{len(df)} articles returned across {len(generated_companies)} of "
            f"{len(selected_companies)} selected companies."
        )
        with st.sidebar.expander("Coverage by company", expanded=False):
            for selected in selected_companies[:8]:
                count = len(df[df['Company'] == selected])
                status = "Available" if count else "No result"
                st.markdown(f"**{selected}** · {status} ({count})")
            if len(selected_companies) > 8:
                st.caption(f"{len(selected_companies) - 8} more companies are in the watchlist.")
    
    # Advanced filters in expander
    with st.sidebar.expander("Advanced article filters", expanded=False):
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
            <h4>Positive news</h4>
            <h2>{}</h2>
            <p>Articles with positive sentiment</p>
        </div>
        """.format(len(df_filtered[df_filtered['Sentiment'] == 'Positive'])), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card summary-card sentiment-negative">
            <h4>Negative news</h4>
            <h2>{}</h2>
            <p>Articles with negative sentiment</p>
        </div>
        """.format(len(df_filtered[df_filtered['Sentiment'] == 'Negative'])), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card summary-card sentiment-neutral">
            <h4>Neutral news</h4>
            <h2>{}</h2>
            <p>Articles with neutral sentiment</p>
        </div>
        """.format(len(df_filtered[df_filtered['Sentiment'] == 'Neutral'])), unsafe_allow_html=True)
    
    with col4:
        avg_sentiment = df_filtered['Sentiment_Score'].mean()
        st.markdown("""
        <div class="metric-card summary-card">
            <h4>Average sentiment</h4>
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
    st.subheader("Key insights")
    
    insights_col1, insights_col2 = st.columns(2)
    
    with insights_col1:
        st.markdown("""
        <div class="metric-card">
            <h4>Sentiment summary</h4>
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
            <h4>Signal quality</h4>
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
