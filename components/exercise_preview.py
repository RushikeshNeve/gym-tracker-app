from __future__ import annotations

import streamlit as st


def _badge(text: str) -> str:
    return f"<span style='display:inline-block;background:#ecfeff;color:#0f766e;padding:4px 10px;border-radius:999px;font-size:0.75rem;margin:2px'>{text}</span>"


def render_exercise_preview(exercise: dict, key_prefix: str = "preview") -> None:
    if not exercise:
        return

    st.markdown(
        """
        <style>
        .exercise-card {border:1px solid #e5e7eb;border-radius:16px;padding:12px;background:#ffffff;box-shadow:0 4px 18px rgba(0,0,0,0.06);}
        .exercise-title {font-size:1.2rem;font-weight:700;margin:0 0 6px 0;}
        .exercise-muted {font-size:0.8rem;color:#6b7280;margin-bottom:8px;}
        .placeholder {height:190px;border:1px dashed #cbd5e1;border-radius:12px;display:flex;align-items:center;justify-content:center;background:#f8fafc;color:#64748b;font-weight:600;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        image_1_url = exercise.get("image_1_url", "")
        image_2_url = exercise.get("image_2_url", "")

        if image_1_url:
            show_alt = image_2_url and st.toggle("Show alternate preview", key=f"{key_prefix}_alt")
            st.image(image_2_url if show_alt else image_1_url, use_container_width=True)
            if image_2_url and not show_alt:
                st.caption("Alternative angle available. Toggle to view image 2.")
        else:
            st.markdown("<div class='placeholder'>No preview available</div>", unsafe_allow_html=True)

        st.markdown(f"<p class='exercise-title'>{exercise.get('name', 'Exercise')}</p>", unsafe_allow_html=True)
        st.markdown(
            "".join(
                [
                    _badge(exercise.get("day_type", "")),
                    _badge(exercise.get("muscle_group", "")),
                    _badge(exercise.get("level", "Unknown")),
                    _badge(exercise.get("equipment", "Body Only")),
                ]
            ),
            unsafe_allow_html=True,
        )

        with st.expander("Instructions", expanded=False):
            instructions = exercise.get("instructions") or []
            if instructions:
                for idx, step in enumerate(instructions, start=1):
                    st.markdown(f"{idx}. {step}")
            else:
                st.caption("No instructions available yet.")

        with st.expander("Muscles worked", expanded=False):
            st.write("Primary:", ", ".join(exercise.get("primary_muscles") or ["Unknown"]))
            st.write("Secondary:", ", ".join(exercise.get("secondary_muscles") or ["None listed"]))

        if exercise.get("video_url"):
            st.link_button("Open exercise video", exercise["video_url"])
        else:
            st.caption("Video: coming soon")
