"""Reusable Streamlit exercise preview with YouTube and coaching details."""

from __future__ import annotations

import streamlit as st

from exercise_data import resolve_video_link


def render_exercise_preview(exercise: dict) -> None:
    youtube_url, youtube_search_url = resolve_video_link(exercise)

    st.markdown(
        """
        <style>
            .exercise-card {
                border-radius: 18px;
                padding: 14px;
                background: linear-gradient(145deg, #0f172a 0%, #1e293b 100%);
                border: 1px solid rgba(255, 255, 255, 0.08);
                box-shadow: 0 10px 28px rgba(0,0,0,0.25);
                margin-bottom: 0.8rem;
            }
            .exercise-title {font-size: 1.15rem; font-weight: 700; color: #f8fafc; margin-bottom: 0.45rem;}
            .badge-wrap {display: flex; gap: 0.4rem; flex-wrap: wrap; margin-bottom: 0.35rem;}
            .badge {display: inline-block; padding: 2px 10px; border-radius: 999px; font-size: 0.72rem; font-weight: 600;}
            .badge-day {background: #dbeafe; color: #1e3a8a;}
            .badge-muscle {background: #dcfce7; color: #14532d;}
            .tip-box {border-radius: 10px; background: rgba(34, 197, 94, 0.12); padding: 0.6rem 0.75rem; border: 1px solid rgba(34, 197, 94, 0.35);}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="exercise-card">
            <div class="exercise-title">{exercise['name']}</div>
            <div class="badge-wrap">
              <span class="badge badge-day">{exercise['day_type']}</span>
              <span class="badge badge-muscle">{exercise['muscle_group']}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if youtube_url:
        st.video(youtube_url)
        st.link_button("▶️ Open on YouTube", youtube_url, use_container_width=True)
    elif youtube_search_url:
        st.link_button("🔎 Find demo on YouTube", youtube_search_url, use_container_width=True)
    else:
        st.info("No video link available yet. Please try another exercise.")

    with st.expander("How to perform"):
        for step in exercise.get("instructions", []):
            st.markdown(f"- {step}")

    with st.expander("Common mistakes"):
        for mistake in exercise.get("common_mistakes", []):
            st.markdown(f"- {mistake}")

    st.markdown(
        f"<div class='tip-box'><strong>Tip:</strong> {exercise.get('tips', '')}</div>",
        unsafe_allow_html=True,
    )
