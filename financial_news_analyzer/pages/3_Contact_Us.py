import streamlit as st  # type: ignore
from datetime import datetime
import sys
import importlib
from pathlib import Path

repository_root = Path(__file__).resolve().parents[2]
if str(repository_root) not in sys.path:
    sys.path.insert(0, str(repository_root))

from financial_news_analyzer.src.presentation import design_system
from financial_news_analyzer.src.presentation.app_shell import render_app_shell
from financial_news_analyzer.src.presentation.support import build_support_mailto, validate_support_request

design_system = importlib.reload(design_system)
apply_design_system = design_system.apply_design_system
render_page_header = design_system.render_page_header

# Page configuration
st.set_page_config(
    page_title="✉️ Contact Us",
    page_icon="✉️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def load_custom_css():
    """Load custom CSS for consistent styling"""
    st.markdown("""
    <style>
    /* Main theme colors - matching other pages */
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
        --contact-gradient: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
    }
    
    /* Hide some Streamlit default elements but keep hamburger menu */
    footer {visibility: hidden;}
    
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
    .contact-card {
        background: var(--gradient-1);
        padding: 25px;
        border-radius: 15px;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        margin: 15px 0;
        color: var(--text-primary);
        animation: slideInLeft 0.6s ease-out;
    }
    
    .contact-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0, 212, 170, 0.2);
        animation: glow 2s infinite;
    }
    
    .info-card {
        background: var(--contact-gradient);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        margin: 10px 0;
        color: var(--text-primary);
        animation: slideInRight 0.6s ease-out;
    }
    
    .info-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 25px rgba(255, 107, 107, 0.3);
    }
    
    /* Contact method cards */
    .contact-method {
        background: var(--gradient-2);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid var(--border-color);
        margin: 10px 0;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .contact-method:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .contact-method a {
        color: var(--text-primary);
        text-decoration: none;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    .contact-method a:hover {
        color: var(--accent-color);
    }
    
    /* Social links */
    .social-links {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin: 20px 0;
    }
    
    .social-link {
        display: inline-block;
        padding: 12px;
        background: var(--gradient-3);
        border-radius: 50%;
        transition: all 0.3s ease;
        text-decoration: none;
        color: white;
        font-size: 1.5rem;
    }
    
    .social-link:hover {
        transform: scale(1.1) rotate(5deg);
        box-shadow: 0 5px 15px rgba(79, 172, 254, 0.4);
    }
    
    /* Office hours card */
    .office-hours {
        background: linear-gradient(135deg, #2ECC71 0%, #27AE60 100%);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin: 15px 0;
    }
    
    /* FAQ section */
    .faq-item {
        background: var(--gradient-1);
        padding: 15px;
        margin: 10px 0;
        border-radius: 10px;
        border-left: 4px solid var(--accent-color);
        transition: all 0.3s ease;
    }
    
    .faq-item:hover {
        transform: translateX(10px);
        box-shadow: 0 4px 15px rgba(0, 212, 170, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    """Main function for Contact Us page"""
    load_custom_css()
    apply_design_system()
    render_app_shell("support")

    render_page_header(
        "How can we help?",
        "Reach the team for product support, feedback, or questions about the research workflow.",
        eyebrow="Support center",
        badges=["Email support", "Product feedback", "Research questions"],
    )

    st.subheader("Contact support")
    contact_col, guidance_col = st.columns([1.1, 1])
    with contact_col:
        st.markdown(
            """
            <section class="support-panel">
                <h3>Email us</h3>
                <p>For product questions, feedback, or a reproducible issue report, send one clear message to:</p>
                <p><a class="article-link" href="mailto:enesor8@gmail.com">enesor8@gmail.com ↗</a></p>
                <p>We aim to reply within one business day. Please do not send account, card, or other sensitive information.</p>
            </section>
            """,
            unsafe_allow_html=True,
        )
    with guidance_col:
        st.markdown(
            """
            <section class="support-panel">
                <h3>Write a useful request</h3>
                <ul>
                    <li>Describe what you expected and what happened instead.</li>
                    <li>Include the company, filter, or page you were using.</li>
                    <li>For a bug, attach a screenshot and the browser/device details.</li>
                </ul>
            </section>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Send a request")
    st.caption("Your message stays in your browser until you choose to open the prepared email draft.")
    with st.form("support_request", clear_on_submit=False):
        form_col1, form_col2 = st.columns(2)
        with form_col1:
            requester_name = st.text_input("Your name", placeholder="How should we address you?")
        with form_col2:
            requester_email = st.text_input("Email address", placeholder="you@example.com")
        request_topic = st.selectbox(
            "Topic",
            ["Product question", "Bug report", "Data question", "Feature request", "Other"],
        )
        request_message = st.text_area(
            "Message",
            placeholder="Tell us what you were trying to do, what happened, and any relevant company or filter.",
            height=150,
        )
        send_request = st.form_submit_button("Prepare email request", use_container_width=True)

    if send_request:
        validation_error = validate_support_request(requester_name, requester_email, request_message)
        if validation_error:
            st.error(validation_error)
        else:
            st.session_state.support_mailto = build_support_mailto(
                request_topic,
                requester_name,
                requester_email,
                request_message,
            )

    if support_mailto := st.session_state.get("support_mailto"):
        st.success("Your request is ready. Open it in your email app to review and send it.")
        st.link_button("Open prepared email", support_mailto, use_container_width=True)

    st.markdown("### Quick answers")
    with st.expander("Where does the data come from?"):
        st.write("News and market information is requested from Yahoo Finance through yfinance when a workspace is opened. Provider data may be delayed or unavailable.")
    with st.expander("Is this investment advice?"):
        st.write("No. The application is a research tool. Review original sources and seek qualified advice before making financial decisions.")
    with st.expander("How do I report a display problem?"):
        st.write("Email a screenshot, the affected page, the filters you selected, and your browser/device details so the issue can be reproduced.")

    return

    # Legacy contact content retained below for source history only.
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="contact-method">
            <h3>📧 Email</h3>
            <a href="mailto:enesor8@gmail.com">enesor8@gmail.com</a>
            <p style="margin-top: 10px; font-size: 0.9rem; color: #bdc3c7;">
                Response within 24 hours
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="contact-method">
            <h3>💬 Support</h3>
            <p style="color: #00D4AA; font-weight: 600;">Email Support</p>
            <p style="margin-top: 10px, 0.9rem; color: #bdc3c7;">
                Contact by email
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="contact-method">
            <h3>🌐 Social</h3>
            <div class="social-links">
                <a href="#" class="social-link" title="LinkedIn">💼</a>
                <a href="#" class="social-link" title="Twitter">🐦</a>
                <a href="#" class="social-link" title="GitHub">💻</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Main contact information
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="contact-card">
            <h3 style="margin-top: 0;">📝 Contact Information</h3>
            <p style="color: #bdc3c7; margin-bottom: 20px;">
                Get in touch with us through the following methods:
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Simple contact information display
        st.markdown("### 📧 Email Contact")
        st.markdown("""
        <div style="background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%); 
                    padding: 20px; border-radius: 10px; margin: 15px 0;">
            <h4 style="color: #00D4AA; margin-top: 0;">📧 Primary Email</h4>
            <p style="font-size: 1.2rem; color: #ffffff;">
                <a href="mailto:enesor8@gmail.com" style="color: #00D4AA; text-decoration: none;">
                    enesor8@gmail.com
                </a>
            </p>
            <p style="color: #bdc3c7; margin-bottom: 0;">
                Click the email address above to send us a message directly.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 💬 What to Include in Your Email")
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 20px; border-radius: 10px; margin: 15px 0;">
            <h4 style="color: #ffffff; margin-top: 0;">📝 Email Guidelines</h4>
            <ul style="color: #ffffff; margin: 0;">
                <li><strong>Subject:</strong> Brief description of your inquiry</li>
                <li><strong>Your Name:</strong> How should we address you?</li>
                <li><strong>Issue Type:</strong> Technical Support, Feature Request, Bug Report, etc.</li>
                <li><strong>Description:</strong> Detailed explanation of your question or issue</li>
                <li><strong>Platform:</strong> Browser/device you're using (if reporting bugs)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🔧 Common Topics")
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%); 
                    padding: 20px; border-radius: 10px; margin: 15px 0;">
            <h4 style="color: #ffffff; margin-top: 0;">📋 Frequently Asked About</h4>
            <div style="color: #ffffff;">
                <p><strong>🛠️ Technical Support:</strong> App errors, loading issues, performance problems</p>
                <p><strong>💡 Feature Requests:</strong> New functionality, improvements, suggestions</p>
                <p><strong>🐛 Bug Reports:</strong> Unexpected behavior, data issues, display problems</p>
                <p><strong>💼 Business Inquiries:</strong> Partnerships, collaborations, enterprise solutions</p>
                <p><strong>📊 Data Questions:</strong> Market data accuracy, sources, update frequency</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Contact information card
        st.markdown("""
        <div class="info-card">
            <h3 style="margin-top: 0;">📍 Contact Information</h3>
            <div style="margin: 15px 0;">
                <strong>📧 Email:</strong><br>
                <a href="mailto:enesor8@gmail.com" style="color: white;">enesor8@gmail.com</a>
            </div>
            <div style="margin: 15px 0;">
                <strong>🌐 Website:</strong><br>
                <span style="color: #00D4AA;">Financial News Analyzer</span>
            </div>
            <div style="margin: 15px 0;">
                <strong>💼 Services:</strong><br>
                • Financial Analysis<br>
                • Market Data<br>
                • Investment Insights<br>
                • Technical Support
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Office hours
        st.markdown("""
        <div class="office-hours">
            <h4 style="margin-top: 0;">🕒 Response Hours</h4>
            <p><strong>Monday - Friday:</strong> 9:00 AM - 6:00 PM</p>
            <p><strong>Saturday:</strong> 10:00 AM - 4:00 PM</p>
            <p><strong>Sunday:</strong> Closed</p>
            <p style="font-size: 0.9rem; margin-top: 15px;">
                <em>Response times are not guaranteed.</em>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick tips
        st.markdown("""
        <div class="contact-card">
            <h4 style="margin-top: 0;">💡 Quick Tips</h4>
            <ul style="color: #bdc3c7; padding-left: 20px;">
                <li>Include specific details about your issue</li>
                <li>Mention your platform/browser if reporting bugs</li>
                <li>Check our FAQ section first</li>
                <li>Be as descriptive as possible</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # FAQ Section
    st.markdown("---")
    st.subheader("❓ Frequently Asked Questions")
    
    faq_col1, faq_col2 = st.columns(2)
    
    with faq_col1:
        with st.expander("🔒 Is my data secure?", expanded=False):
            st.write("""
            This demo does not collect account data. Verify the security and privacy
            practices of the platform hosting the application before sharing personal information.
            """)
        
        with st.expander("📊 How do I access premium features?", expanded=False):
            st.write("""
            Premium features are currently in development. Contact us to be notified 
            when they become available or to discuss enterprise solutions.
            """)
        
        with st.expander("🛠️ Technical support hours?", expanded=False):
            st.write("""
            Contact availability is not guaranteed; use the published email address
            for questions or bug reports.
            """)
    
    with faq_col2:
        with st.expander("💰 Is there a cost for using the platform?", expanded=False):
            st.write("""
            The basic financial analysis tools are free. Premium features and 
            enterprise solutions are available on request.
            """)
        
        with st.expander("📱 Mobile app availability?", expanded=False):
            st.write("""
            We're currently focused on the web platform. Mobile optimization 
            is on our roadmap for future releases.
            """)
        
        with st.expander("🔄 How often is data updated?", expanded=False):
            st.write("""
            Market and news data are refreshed on demand and may be delayed by the
            external provider.
            """)
    
    # Footer with additional links
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <p style="color: #95a5a6;">
            <strong>Need immediate help?</strong> 
            <a href="mailto:enesor8@gmail.com" style="color: #00D4AA;">Send us an email</a> 
            and we'll respond as quickly as possible.
        </p>
        <p style="color: #7f8c8d; font-size: 0.9rem;">
            Financial News Analyzer © 2024 - Professional Financial Analysis Platform
        </p>
    </div>
    """, unsafe_allow_html=True)

try:
    main()
except Exception as e:
    st.error(f"Bir hata oluştu: {e}")
