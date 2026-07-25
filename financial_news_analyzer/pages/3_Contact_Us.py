import streamlit as st  # type: ignore
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
    page_title="Support · Financial News Analyzer",
    page_icon="✉️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def main():
    """Main function for Contact Us page"""
    apply_design_system()
    render_app_shell("support")

    render_page_header(
        "Get help without the back-and-forth.",
        "Send product feedback, report an issue, or ask a question about the research workflow.",
        eyebrow="Support center",
        badges=["One-business-day target", "No data stored", "Email handoff"],
    )

    st.markdown(
        """
        <div class="section-kicker">Contact</div>
        <div class="section-heading">Choose the clearest route</div>
        <p class="section-copy">A little context helps us give you a useful answer on the first reply.</p>
        """,
        unsafe_allow_html=True,
    )
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

    st.markdown(
        """
        <div class="section-kicker">Message builder</div>
        <div class="section-heading">Prepare a support request</div>
        """,
        unsafe_allow_html=True,
    )
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

    st.markdown(
        """
        <div class="section-kicker">Before you write</div>
        <div class="section-heading">Quick answers</div>
        """,
        unsafe_allow_html=True,
    )
    with st.expander("Where does the data come from?"):
        st.write("News and market information is requested from Yahoo Finance through yfinance when a workspace is opened. Provider data may be delayed or unavailable.")
    with st.expander("Is this investment advice?"):
        st.write("No. The application is a research tool. Review original sources and seek qualified advice before making financial decisions.")
    with st.expander("How do I report a display problem?"):
        st.write("Email a screenshot, the affected page, the filters you selected, and your browser/device details so the issue can be reproduced.")

try:
    main()
except Exception:
    st.error("The support page could not be loaded. Please refresh and try again.")
