"""Streamlit Cloud entry point for the legacy Streamlit interface.

NiceGUI runs as a standalone ASGI server and therefore needs a platform such as
Render, Railway, Fly.io, or a Docker host. Streamlit Community Cloud invokes
this file with ``streamlit run``, so it must remain a Streamlit application.
"""

from streamlit_app import main


if __name__ == "__main__":
    main()
