"""Shared brand and visual styling helpers."""

from __future__ import annotations

import streamlit as st


def apply_global_style() -> None:
    """Apply shared cocktail-bar styling across pages."""
    st.markdown(
        """
        <style>
        :root {
          --pd-bg: #120f0d;
          --pd-surface: rgba(34, 24, 18, 0.78);
          --pd-surface-strong: rgba(53, 38, 28, 0.92);
          --pd-border: rgba(212, 171, 102, 0.28);
          --pd-text: #f7efe2;
          --pd-muted: #d4c1a8;
          --pd-accent: #d4ab66;
          --pd-accent-deep: #8f3d2e;
          --pd-success: #2f7c66;
        }

        .stApp {
          background:
            radial-gradient(circle at top right, rgba(143, 61, 46, 0.28), transparent 28%),
            radial-gradient(circle at top left, rgba(212, 171, 102, 0.18), transparent 22%),
            linear-gradient(180deg, #191210 0%, #120f0d 100%);
          color: var(--pd-text);
        }

        .main .block-container {
          max-width: 1180px;
          padding-top: 2.2rem;
          padding-bottom: 3rem;
        }

        h1, h2, h3 {
          letter-spacing: 0.01em;
        }

        p, li, label, .stCaption, .stMarkdown, .stText, .stAlert {
          color: var(--pd-text);
        }

        [data-testid="stMetric"] {
          background: var(--pd-surface);
          border: 1px solid var(--pd-border);
          border-radius: 18px;
          padding: 0.8rem 1rem;
        }

        [data-testid="stForm"] {
          background: var(--pd-surface);
          border: 1px solid var(--pd-border);
          border-radius: 22px;
          padding: 1rem 1rem 0.25rem 1rem;
          backdrop-filter: blur(8px);
        }

        [data-testid="stVerticalBlock"] [data-testid="stVerticalBlockBorderWrapper"] {
          border-color: var(--pd-border);
          background: var(--pd-surface);
        }

        .stButton > button,
        .stDownloadButton > button,
        [data-testid="baseButton-secondary"] {
          border-radius: 999px;
          border: 1px solid rgba(212, 171, 102, 0.34);
          background: linear-gradient(135deg, var(--pd-accent) 0%, #bf8352 100%);
          color: #1b120e;
          font-weight: 700;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover {
          border-color: rgba(247, 239, 226, 0.46);
          color: #120f0d;
        }

        .stTextInput input,
        .stTextArea textarea,
        .stMultiSelect div[data-baseweb="select"],
        div[data-baseweb="select"] > div {
          background-color: rgba(255, 248, 240, 0.06);
          border-radius: 16px;
        }

        .pd-header {
          position: relative;
          overflow: hidden;
          margin-bottom: 1.25rem;
          padding: 1.4rem 1.5rem;
          border: 1px solid var(--pd-border);
          border-radius: 28px;
          background:
            linear-gradient(135deg, rgba(53, 38, 28, 0.96) 0%, rgba(22, 17, 14, 0.94) 72%),
            var(--pd-surface-strong);
          box-shadow: 0 18px 50px rgba(0, 0, 0, 0.25);
        }

        .pd-header::after {
          content: "";
          position: absolute;
          inset: auto -5% -50% auto;
          width: 220px;
          height: 220px;
          border-radius: 999px;
          background: radial-gradient(circle, rgba(212, 171, 102, 0.22) 0%, transparent 70%);
        }

        .pd-header-top {
          display: flex;
          align-items: center;
          gap: 0.9rem;
          margin-bottom: 0.75rem;
        }

        .pd-mark {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          width: 3rem;
          height: 3rem;
          border-radius: 50%;
          background: linear-gradient(135deg, var(--pd-accent) 0%, #b8644e 100%);
          color: #1b120e;
          font-size: 1rem;
          font-weight: 800;
          letter-spacing: 0.08em;
        }

        .pd-kicker {
          font-size: 0.76rem;
          text-transform: uppercase;
          letter-spacing: 0.18em;
          color: var(--pd-accent);
          margin-bottom: 0.15rem;
        }

        .pd-title {
          margin: 0;
          font-size: clamp(1.9rem, 4vw, 3.1rem);
          line-height: 1;
        }

        .pd-subtitle {
          margin: 0.4rem 0 0 0;
          max-width: 46rem;
          color: var(--pd-muted);
          font-size: 1rem;
          line-height: 1.6;
        }

        .pd-chip-row {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
          margin: 0.9rem 0 1rem;
        }

        .pd-chip {
          display: inline-flex;
          align-items: center;
          gap: 0.35rem;
          padding: 0.42rem 0.75rem;
          border-radius: 999px;
          background: rgba(255, 255, 255, 0.06);
          border: 1px solid rgba(212, 171, 102, 0.2);
          color: var(--pd-text);
          font-size: 0.88rem;
        }

        .pd-panel {
          padding: 1rem 1.1rem;
          border: 1px solid var(--pd-border);
          border-radius: 20px;
          background: var(--pd-surface);
        }

        @media (max-width: 900px) {
          .main .block-container {
            padding-top: 1.2rem;
            padding-left: 1rem;
            padding-right: 1rem;
          }

          .pd-header {
            padding: 1.15rem 1rem;
            border-radius: 22px;
          }

          .pd-header-top {
            align-items: flex-start;
          }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_brand_header(title: str, subtitle: str, kicker: str = "Pour Decisions") -> None:
    """Render a shared branded page header."""
    st.markdown(
        f"""
        <section class="pd-header">
          <div class="pd-header-top">
            <div class="pd-mark">PD</div>
            <div>
              <div class="pd-kicker">{kicker}</div>
              <h1 class="pd-title">{title}</h1>
            </div>
          </div>
          <p class="pd-subtitle">{subtitle}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )
