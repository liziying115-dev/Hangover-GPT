"""HangoverGPT 🍹 — Streamlit entry point."""

import streamlit as st

st.set_page_config(
    page_title="HangoverGPT 🍹",
    page_icon="🍹",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("HangoverGPT 🍹")
st.write("Welcome! Open **Results** in the sidebar to match cocktails to your bar.")
