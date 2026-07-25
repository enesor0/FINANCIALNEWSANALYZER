"""Bridge between Streamlit pages and the React application shell."""

from pathlib import Path
from typing import Final

import streamlit as st
import streamlit.components.v1 as components


_FRONTEND_DIR: Final = Path(__file__).with_name("frontend") / "dist"
_shell_component = components.declare_component("financial_app_shell", path=str(_FRONTEND_DIR))

_PAGES: Final = {
    "home": "streamlit_app.py",
    "analysis": "pages/1_Financial_Analysis.py",
    "market": "pages/2_Market_Data.py",
    "support": "pages/3_Contact_Us.py",
}


def render_app_shell(active_page: str) -> None:
    """Render the React navigation shell and route a selected workspace."""
    selection = _shell_component(active_page=active_page, key="financial_app_shell", default=None)
    if selection in _PAGES and selection != active_page:
        st.switch_page(_PAGES[selection])
