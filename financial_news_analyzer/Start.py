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
            page_title="📊 Financial News Analyzer",
            page_icon="📊",
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
            "Financial News Analyzer",
            "Provider-linked news, explainable sentiment signals, and market context in one focused workspace.",
            eyebrow="Market intelligence workspace",
            badges=["Yahoo Finance linked data", "Explainable signals", "14 market clocks"],
        )

    def _render_sidebar(self) -> None:
        st.sidebar.markdown("---")
        self._world_clock.render()

    def _render_main_content(self) -> None:
        st.markdown("### Choose a workspace")
        st.caption("Start with the task you want to complete. You can return here any time from the navigation bar.")
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

        st.markdown("### Core capabilities")
        col1, col2, col3 = st.columns(3)
        for column, title, body in (
            (col1, "📰 Financial news analysis", "Linked provider articles with transparent keyword sentiment."),
            (col2, "📊 Market data", "Current daily prices, history, and category performance."),
            (col3, "🌍 Market schedules", "Weekday exchange schedules across fourteen global markets."),
        ):
            with column:
                st.markdown(f"<section class='feature-card'><h4>{title}</h4><p>{body}</p></section>", unsafe_allow_html=True)

        st.caption(
            "Market prices and article metadata are requested from Yahoo Finance when you open a workspace. "
            "Data may be delayed or temporarily unavailable."
        )

    def _render_footer(self) -> None:
        st.markdown("---")
        st.caption("Financial News Analyzer · Provider-linked research tooling")


def main() -> None:
    try:
        FinancialAnalyzerApp().run()
    except Exception:
        logging.exception("Application failed to start")
        st.error("The application could not be started. Please refresh the page and try again.")


if __name__ == "__main__":
    main()
