"""Shared visual system for the native Streamlit workspaces."""

from html import escape

import streamlit as st


def apply_design_system() -> None:
    """Apply the shared product palette, spacing, and component treatments."""
    st.markdown(
        """
        <style>
        :root {
            --ink-950: #0B1220;
            --ink-900: #111C2E;
            --ink-800: #1C2A3F;
            --ink-700: #34445C;
            --ink-500: #64748B;
            --ink-400: #94A3B8;
            --blue-700: #1D4ED8;
            --blue-600: #2563EB;
            --blue-100: #DBEAFE;
            --blue-50: #EFF6FF;
            --green-700: #047857;
            --green-100: #D1FAE5;
            --red-700: #BE123C;
            --red-100: #FFE4E6;
            --amber-700: #A16207;
            --amber-100: #FEF3C7;
            --surface: #FFFFFF;
            --surface-soft: #F8FAFC;
            --canvas: #F3F6FA;
            --line: #E2E8F0;
            --line-strong: #CBD5E1;
            --shadow-sm: 0 1px 2px rgba(15, 23, 42, .04);
            --shadow-md: 0 12px 32px rgba(15, 23, 42, .07);
        }

        * { box-sizing: border-box; }
        #MainMenu, footer { visibility: hidden; }
        [data-testid="stHeader"], [data-testid="stSidebarNav"] { display: none !important; }
        html { color-scheme: light; }
        .stApp {
            background:
                radial-gradient(circle at 92% 2%, rgba(37, 99, 235, .08), transparent 24rem),
                linear-gradient(180deg, #F8FAFC 0, var(--canvas) 36rem) !important;
            color: var(--ink-900) !important;
            font-family: Inter, Aptos, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }
        .main .block-container {
            max-width: 1280px;
            padding: .75rem 2rem 4.5rem !important;
            margin: 0 auto;
        }

        [data-testid="stSidebar"] {
            min-width: 322px !important;
            border-right: 1px solid var(--line);
            box-shadow: 10px 0 30px rgba(15, 23, 42, .035);
        }
        [data-testid="stSidebar"] > div:first-child { background: #F8FAFC !important; }
        [data-testid="stSidebarContent"] { padding-top: 1rem; }
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: var(--ink-900) !important;
            font-family: inherit !important;
            letter-spacing: -.02em;
        }
        [data-testid="stSidebar"] h2 { font-size: 1.05rem !important; }
        [data-testid="stSidebar"] h3 {
            margin-top: 1.15rem !important;
            font-size: .72rem !important;
            letter-spacing: .1em !important;
            text-transform: uppercase;
            color: var(--ink-500) !important;
        }

        .app-hero {
            position: relative;
            isolation: isolate;
            overflow: hidden;
            padding: clamp(1.65rem, 4vw, 3.15rem);
            margin: .65rem 0 1.8rem;
            border: 1px solid rgba(255, 255, 255, .08);
            border-radius: 24px;
            background:
                linear-gradient(120deg, rgba(255, 255, 255, .04), transparent 48%),
                linear-gradient(135deg, #0B1220 0%, #122642 62%, #183B6B 100%);
            box-shadow: 0 20px 50px rgba(15, 23, 42, .18);
            color: #FFFFFF;
        }
        .app-hero::before,
        .app-hero::after {
            content: "";
            position: absolute;
            z-index: -1;
            border-radius: 999px;
            pointer-events: none;
        }
        .app-hero::before {
            width: 25rem;
            height: 25rem;
            right: -11rem;
            top: -15rem;
            background: rgba(96, 165, 250, .22);
            filter: blur(1px);
        }
        .app-hero::after {
            width: 13rem;
            height: 13rem;
            right: 18%;
            bottom: -10rem;
            background: rgba(45, 212, 191, .13);
        }
        .eyebrow {
            margin-bottom: .72rem;
            color: #93C5FD;
            font-size: .7rem;
            font-weight: 800;
            letter-spacing: .14em;
            text-transform: uppercase;
        }
        .hero-title {
            max-width: 52rem;
            margin: 0;
            color: #FFFFFF !important;
            font-size: clamp(2rem, 4.5vw, 3.75rem);
            font-weight: 760;
            letter-spacing: -.055em;
            line-height: 1.02;
        }
        .app-hero p {
            max-width: 45rem;
            margin: .95rem 0 0;
            color: #CBD5E1 !important;
            font-size: clamp(.95rem, 1.8vw, 1.08rem);
            line-height: 1.65;
        }
        .hero-badges { display: flex; flex-wrap: wrap; gap: .5rem; margin-top: 1.35rem; }
        .hero-badge {
            padding: .38rem .68rem;
            border: 1px solid rgba(255, 255, 255, .15);
            border-radius: 999px;
            background: rgba(255, 255, 255, .07);
            color: #E2E8F0;
            font-size: .75rem;
            font-weight: 700;
            backdrop-filter: blur(10px);
        }

        h1, h2, h3, h4,
        [data-testid="stMarkdownContainer"] h1,
        [data-testid="stMarkdownContainer"] h2,
        [data-testid="stMarkdownContainer"] h3,
        [data-testid="stMarkdownContainer"] h4 {
            color: var(--ink-900) !important;
        }
        h1, h2, h3 { letter-spacing: -.035em; }
        h2 { margin-top: 2.2rem !important; }
        p, li, [data-testid="stCaptionContainer"] { color: var(--ink-500) !important; }
        [data-testid="stCaptionContainer"] { opacity: 1 !important; line-height: 1.55; }
        a, .article-link { color: var(--blue-700) !important; font-weight: 700; }
        hr { border-color: var(--line) !important; }

        .section-kicker {
            margin: 2.1rem 0 .35rem;
            color: var(--blue-700);
            font-size: .7rem;
            font-weight: 800;
            letter-spacing: .12em;
            text-transform: uppercase;
        }
        .section-heading {
            margin: 0 0 .35rem;
            color: var(--ink-900);
            font-size: clamp(1.35rem, 2vw, 1.75rem);
            font-weight: 760;
            letter-spacing: -.035em;
        }
        .section-copy { margin: 0 0 1.15rem; color: var(--ink-500); line-height: 1.6; }

        [data-testid="stPageLink"] a {
            min-height: 60px;
            padding: .85rem 1rem;
            border: 1px solid var(--line) !important;
            border-radius: 14px !important;
            background: var(--surface) !important;
            box-shadow: var(--shadow-sm);
            color: var(--ink-900) !important;
            transition: border-color .16s ease, box-shadow .16s ease, transform .16s ease;
        }
        [data-testid="stPageLink"] a:hover {
            transform: translateY(-1px);
            border-color: #93C5FD !important;
            box-shadow: 0 10px 24px rgba(37, 99, 235, .09);
        }
        [data-testid="stPageLink"] p { color: var(--ink-900) !important; font-weight: 750 !important; }

        .feature-card, .metric-card, .contact-method, .contact-card, .info-card,
        .support-panel, .news-card, .workspace-card {
            border: 1px solid var(--line) !important;
            border-radius: 18px !important;
            background: var(--surface) !important;
            box-shadow: var(--shadow-sm) !important;
            color: var(--ink-900) !important;
        }
        .feature-card, .workspace-card {
            min-height: 205px;
            height: calc(100% - .75rem);
            padding: 1.4rem !important;
        }
        .feature-card .card-icon, .workspace-card .card-icon {
            display: grid;
            place-items: center;
            width: 40px;
            height: 40px;
            margin-bottom: 1.25rem;
            border-radius: 12px;
            background: var(--blue-50);
            color: var(--blue-700);
            font-size: .78rem;
            font-weight: 850;
            letter-spacing: .03em;
        }
        .feature-card h4, .workspace-card h4 { margin: 0 0 .55rem !important; font-size: 1rem; }
        .feature-card p, .workspace-card p { margin: 0; font-size: .9rem; line-height: 1.6; }
        .feature-card:hover, .workspace-card:hover, .support-panel:hover, .news-card:hover {
            border-color: #BFDBFE !important;
            box-shadow: var(--shadow-md) !important;
        }

        .metric-card {
            min-height: 132px;
            height: calc(100% - .65rem);
            padding: 1rem 1.1rem !important;
            position: relative;
            overflow: hidden;
        }
        .summary-card { min-height: 132px; height: calc(100% - .65rem); }
        .metric-card::before {
            content: "";
            position: absolute;
            inset: 0 auto 0 0;
            width: 3px;
            background: var(--blue-600);
        }
        .metric-card.sentiment-positive::before, .metric-card.price-up::before { background: #10B981; }
        .metric-card.sentiment-negative::before, .metric-card.price-down::before { background: #F43F5E; }
        .metric-card.sentiment-neutral::before, .metric-card.price-stable::before { background: var(--ink-400); }
        .metric-card h2, .metric-card h3, .metric-card h4 { margin: 0 !important; font-family: inherit !important; }
        .metric-card h2 { margin-top: .45rem !important; font-size: 1.85rem; letter-spacing: -.04em; }
        .metric-card h3 { font-size: 1.35rem; }
        .metric-card h4 {
            color: var(--ink-500) !important;
            font-size: .72rem;
            letter-spacing: .06em;
            text-transform: uppercase;
        }
        .metric-card p { margin: .45rem 0 0; font-size: .8rem; }
        .metric-card ul { margin: .8rem 0 0; padding-left: 1.1rem; }
        .price-change-positive { color: var(--green-700) !important; font-weight: 750; }
        .price-change-negative { color: var(--red-700) !important; font-weight: 750; }

        [data-testid="stMetric"] {
            min-height: 108px;
            padding: 1rem;
            border: 1px solid var(--line);
            border-radius: 16px;
            background: var(--surface);
            box-shadow: var(--shadow-sm);
        }
        [data-testid="stMetricLabel"] { color: var(--ink-500) !important; }
        [data-testid="stMetricValue"] { color: var(--ink-900) !important; font-weight: 760; }
        [data-testid="stMetricDelta"] { color: var(--green-700) !important; }

        .stApp .stButton > button,
        .stApp [data-testid="stDownloadButton"] > button,
        .stApp .stLinkButton > a {
            min-height: 42px;
            border: 1px solid var(--line-strong) !important;
            border-radius: 11px !important;
            background: var(--surface) !important;
            color: var(--ink-800) !important;
            box-shadow: var(--shadow-sm) !important;
            font-weight: 720 !important;
            transition: transform .15s ease, border-color .15s ease, box-shadow .15s ease;
        }
        .stApp .stButton > button:hover,
        .stApp [data-testid="stDownloadButton"] > button:hover,
        .stApp .stLinkButton > a:hover {
            transform: translateY(-1px);
            border-color: #93C5FD !important;
            color: var(--blue-700) !important;
            box-shadow: 0 7px 16px rgba(37, 99, 235, .08) !important;
        }
        .stApp .stButton > button[kind="primary"],
        .stApp [data-testid="stFormSubmitButton"] > button,
        .stApp .stLinkButton > a {
            border-color: var(--blue-600) !important;
            background: var(--blue-600) !important;
            color: #FFFFFF !important;
        }
        .stApp .stButton > button[kind="primary"]:hover,
        .stApp [data-testid="stFormSubmitButton"] > button:hover,
        .stApp .stLinkButton > a:hover {
            border-color: var(--blue-700) !important;
            background: var(--blue-700) !important;
            color: #FFFFFF !important;
        }
        button:focus-visible, a:focus-visible, input:focus-visible, textarea:focus-visible {
            outline: 3px solid rgba(37, 99, 235, .25) !important;
            outline-offset: 2px;
        }

        [data-baseweb="input"] > div,
        [data-baseweb="select"] > div,
        [data-baseweb="textarea"] {
            border-color: var(--line-strong) !important;
            border-radius: 11px !important;
            background: var(--surface) !important;
        }
        [data-baseweb="input"]:focus-within > div,
        [data-baseweb="select"]:focus-within > div,
        [data-baseweb="textarea"]:focus-within {
            border-color: var(--blue-600) !important;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, .1) !important;
        }
        [data-baseweb="input"] input,
        [data-baseweb="select"] *,
        [data-baseweb="textarea"] textarea { color: var(--ink-900) !important; }
        [data-testid="stTextInput"] input::placeholder,
        [data-testid="stTextArea"] textarea::placeholder { color: var(--ink-400) !important; opacity: 1; }
        [data-testid="stMultiSelect"] [data-baseweb="tag"] {
            border: 1px solid #BFDBFE !important;
            border-radius: 8px !important;
            background: var(--blue-50) !important;
        }
        [data-testid="stMultiSelect"] [data-baseweb="tag"] span,
        [data-testid="stMultiSelect"] [data-baseweb="tag"] svg {
            color: var(--blue-700) !important;
            fill: var(--blue-700) !important;
        }

        [data-testid="stExpander"] {
            overflow: hidden;
            border: 1px solid var(--line) !important;
            border-radius: 14px !important;
            background: rgba(255, 255, 255, .82);
            box-shadow: var(--shadow-sm);
        }
        [data-testid="stForm"] {
            padding: 1.35rem;
            border: 1px solid var(--line);
            border-radius: 18px;
            background: var(--surface);
            box-shadow: var(--shadow-sm);
        }
        [data-testid="stDataFrame"], [data-testid="stTable"] {
            overflow: hidden;
            border: 1px solid var(--line);
            border-radius: 16px;
            background: var(--surface);
        }
        .stPlotlyChart {
            overflow: hidden;
            padding: .35rem;
            border: 1px solid var(--line);
            border-radius: 18px;
            background: var(--surface);
            box-shadow: var(--shadow-sm);
        }
        .stTabs [data-baseweb="tab-list"] { gap: .35rem; border-bottom: 1px solid var(--line); }
        .stTabs [data-baseweb="tab"] {
            height: 42px;
            border-radius: 10px 10px 0 0;
            color: var(--ink-500);
            font-weight: 700;
        }
        .stTabs [aria-selected="true"] { color: var(--blue-700) !important; background: var(--blue-50); }
        [data-testid="stAlert"] { border-radius: 14px; border: 1px solid var(--line); }

        .news-card {
            min-height: 140px;
            padding: 1.15rem 1.25rem;
            margin: .7rem 0;
            border-left: 4px solid #10B981 !important;
        }
        .news-card.negative { border-left-color: #F43F5E !important; }
        .news-card.neutral { border-left-color: var(--ink-400) !important; }
        .news-card h4 { margin: 0 0 .6rem !important; font-size: 1.02rem; line-height: 1.45; }
        .news-meta { margin-bottom: .9rem; color: var(--ink-500); font-size: .8rem; }
        .news-footer { display: flex; justify-content: space-between; align-items: center; gap: .8rem; flex-wrap: wrap; }
        .sentiment-chip {
            padding: .3rem .62rem;
            border-radius: 999px;
            background: var(--green-100);
            color: var(--green-700);
            font-size: .74rem;
            font-weight: 750;
        }
        .sentiment-chip.negative { background: var(--red-100); color: var(--red-700); }
        .sentiment-chip.neutral { background: #E2E8F0; color: var(--ink-700); }
        .support-panel { min-height: 255px; padding: 1.4rem; }
        .support-panel h3 { margin: 0 0 .7rem !important; }
        .support-panel p, .support-panel li { line-height: 1.65; }
        .live-note { color: var(--ink-500); font-size: .85rem; }

        @media (max-width: 900px) {
            .main .block-container { padding: .55rem 1rem 3rem !important; }
            .app-hero { border-radius: 20px; }
            [data-testid="stHorizontalBlock"] { gap: .7rem; }
        }
        @media (max-width: 720px) {
            [data-testid="stSidebar"] { min-width: min(88vw, 322px) !important; }
            .app-hero { margin-top: .25rem; padding: 1.45rem; }
            .hero-title { font-size: 2.05rem; }
            .feature-card, .workspace-card, .metric-card, .summary-card, .news-card, .support-panel {
                height: auto;
                min-height: 0;
            }
            .news-footer { align-items: flex-start; flex-direction: column; }
        }
        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after { scroll-behavior: auto !important; transition: none !important; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_page_header(
    title: str,
    description: str,
    *,
    eyebrow: str,
    badges: list[str] | None = None,
) -> None:
    """Render a concise product header in the shared visual system."""
    badge_html = "".join(
        f'<span class="hero-badge">{escape(badge)}</span>' for badge in badges or []
    )
    st.markdown(
        f'<section class="app-hero">'
        f'<div class="eyebrow">{escape(eyebrow)}</div>'
        f'<div class="hero-title" role="heading" aria-level="1">{escape(title)}</div>'
        f'<p>{escape(description)}</p>'
        f'<div class="hero-badges">{badge_html}</div>'
        f'</section>',
        unsafe_allow_html=True,
    )


def style_plotly_chart(figure):
    """Apply the light product theme to a Plotly figure."""
    figure.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#475569", family="Inter, Arial, sans-serif", size=12),
        title=dict(font=dict(color="#111C2E", size=17), x=0.02, xanchor="left"),
        margin=dict(l=48, r=24, t=64, b=48),
        hoverlabel=dict(
            bgcolor="#111C2E",
            bordercolor="#111C2E",
            font=dict(color="#FFFFFF"),
        ),
    )
    figure.update_xaxes(
        gridcolor="#EEF2F7",
        linecolor="#CBD5E1",
        zerolinecolor="#CBD5E1",
        title_font=dict(color="#64748B"),
    )
    figure.update_yaxes(
        gridcolor="#EEF2F7",
        linecolor="#CBD5E1",
        zerolinecolor="#CBD5E1",
        title_font=dict(color="#64748B"),
    )
    return figure
