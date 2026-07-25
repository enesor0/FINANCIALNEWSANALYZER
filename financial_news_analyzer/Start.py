"""Entry point for the Financial News Analyzer Streamlit app."""

import logging
import sys
from pathlib import Path

import streamlit as st


repository_root = Path(__file__).resolve().parent.parent
if str(repository_root) not in sys.path:
    sys.path.insert(0, str(repository_root))

from financial_news_analyzer.src.presentation import design_system
from financial_news_analyzer.src.presentation.app_shell import render_app_shell
from financial_news_analyzer.src.presentation.components.world_clock_component import WorldClockComponent
from financial_news_analyzer.src.presentation.dependencies import get_application_services


class FinancialAnalyzerApp:
    """Render the home workspace and global market-clock sidebar."""

    def __init__(self) -> None:
        st.set_page_config(
            page_title="Financial News Analyzer",
            page_icon="📈",
            layout="wide",
            initial_sidebar_state="collapsed",
        )
        services = get_application_services()
        self._world_clock = WorldClockComponent(services.get_market_schedules)

    def run(self) -> None:
        design_system.apply_design_system()
        render_app_shell("home")
        self._render_header()
        self._render_sidebar()
        self._render_main_content()
        self._render_footer()

    def _render_header(self) -> None:
        design_system.render_page_header(
            "See the signal behind the market story.",
            "Research company news, compare explainable sentiment signals, and put daily price movement in context—without the usual dashboard noise.",
            eyebrow="Financial intelligence workspace",
            badges=["Linked original sources", "Transparent sentiment", "Live market context"],
        )

    def _render_sidebar(self) -> None:
        st.sidebar.markdown("---")
        self._world_clock.render()

    def _render_main_content(self) -> None:
        st.markdown(
            """
            <div class="section-kicker">Start here</div>
            <div class="section-heading">Choose your research path</div>
            <p class="section-copy">Move from a headline to context, or begin with the market and inspect the companies driving it.</p>
            """,
            unsafe_allow_html=True,
        )
        news_col, market_col = st.columns(2)
        with news_col:
            st.page_link(
                "pages/1_Financial_Analysis.py",
                label="Research company news",
                icon="📰",
                use_container_width=True,
            )
            st.markdown(
                """
                <section class="workspace-card">
                    <span class="card-icon">NEWS</span>
                    <h4>Understand the current narrative</h4>
                    <p>Build a company watchlist, filter live coverage, compare sentiment, and open every story at its original source.</p>
                </section>
                """,
                unsafe_allow_html=True,
            )
        with market_col:
            st.page_link(
                "pages/2_Market_Data.py",
                label="Explore market performance",
                icon="📈",
                use_container_width=True,
            )
            st.markdown(
                """
                <section class="workspace-card">
                    <span class="card-icon">DATA</span>
                    <h4>Put price moves in context</h4>
                    <p>Compare the latest closes, scan sector performance, and inspect price and volume history for a selected symbol.</p>
                </section>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            """
            <div class="section-kicker">What you can do</div>
            <div class="section-heading">One workspace, three useful views</div>
            <p class="section-copy">Designed for quick orientation first, then deeper research when you need it.</p>
            """,
            unsafe_allow_html=True,
        )
        col1, col2, col3 = st.columns(3)
        for column, icon, title, body in (
            (col1, "01", "News intelligence", "Follow selected companies and compare the tone of recent, source-linked coverage."),
            (col2, "02", "Market performance", "Scan daily movement, historical price action, volume, and category averages."),
            (col3, "03", "Global sessions", "Check weekday trading schedules across fourteen major financial markets."),
        ):
            with column:
                st.markdown(
                    f"<section class='feature-card'><span class='card-icon'>{icon}</span>"
                    f"<h4>{title}</h4><p>{body}</p></section>",
                    unsafe_allow_html=True,
                )

        st.caption(
            "Market prices and article metadata are requested from Yahoo Finance when you open a workspace. "
            "Data may be delayed or temporarily unavailable."
        )

    def _render_footer(self) -> None:
        st.markdown("---")
        st.caption("Financial News Analyzer · Research support, not investment advice")


def main() -> None:
    try:
        FinancialAnalyzerApp().run()
    except Exception:
        logging.exception("Application failed to start")
        st.error("The application could not be started. Please refresh the page and try again.")


if __name__ == "__main__":
    main()
