"""Mixing progress tracker widget."""

import streamlit as st


def mixing_progress(current_step: int, total_steps: int) -> None:
    """Render a labeled progress bar for the mixing simulation."""
    total_steps = max(total_steps, 0)
    current_step = max(current_step, 0)

    if total_steps == 0:
        st.info("No mixing steps are available for this recipe.")
        return

    if current_step >= total_steps:
        st.caption(f"Completed {total_steps}/{total_steps} steps")
        st.progress(1.0)
        return

    progress = (current_step + 1) / total_steps
    st.caption(f"Step {current_step + 1} of {total_steps}")
    st.progress(progress)
