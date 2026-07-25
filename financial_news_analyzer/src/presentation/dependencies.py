"""Presentation-layer access to the composed application use cases."""

import streamlit as st

from ..bootstrap import ApplicationServices, build_application_services


@st.cache_resource(show_spinner=False)
def get_application_services() -> ApplicationServices:
    """Keep one stateless application object graph per Streamlit process."""
    return build_application_services()
