from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import streamlit as st

from db import PHOTO_TYPES, get_progress_photos, insert_progress_photo, save_progress_photo_file
from utils import render_chip_row, status_banner

st.title("Progress Photos")
selected_date = st.date_input("Photo date", value=date.today())
log_date = selected_date.isoformat()
today_photos = get_progress_photos(log_date)

render_chip_row(
    [
        (f"Today photos: {len(today_photos)}", "success" if not today_photos.empty else "warn"),
        ("Local storage only", "neutral"),
        ("Front / Side / Back supported", "neutral"),
    ]
)

with st.form("photo_form"):
    photo_type = st.selectbox("Photo type", PHOTO_TYPES)
    photo_notes = st.text_area("Notes", placeholder="Lighting, posture, how you felt, check-in notes")
    uploaded = st.file_uploader("Upload progress photo", type=["jpg", "jpeg", "png"], accept_multiple_files=False)
    submitted = st.form_submit_button("Save Progress Photo")

if submitted:
    if uploaded is None:
        status_banner("Choose a photo before saving.", "warning")
    else:
        file_path = save_progress_photo_file(uploaded, log_date, photo_type)
        insert_progress_photo({"date": log_date, "photo_type": photo_type, "file_path": file_path, "notes": photo_notes})
        st.success("Progress photo saved.")
        st.rerun()

st.markdown("### Today Status")
if today_photos.empty:
    status_banner("No photo saved for the selected day yet.", "warning")
else:
    status_banner("Progress photo logged for the selected day.", "success")
    st.dataframe(today_photos[["date", "photo_type", "file_path", "notes"]], use_container_width=True, hide_index=True)

st.markdown("### Weekly Gallery")
all_photos = get_progress_photos()
if all_photos.empty:
    st.info("No progress photo metadata yet.")
else:
    weekly = all_photos.copy()
    weekly["date"] = weekly["date"].astype(str)
    recent_week = {(selected_date - timedelta(days=i)).isoformat() for i in range(6, -1, -1)}
    weekly = weekly[weekly["date"].isin(recent_week)]
    if weekly.empty:
        st.info("No photos in the selected week's window.")
    else:
        for _, row in weekly.iterrows():
            with st.container(border=True):
                st.caption(f"{row['date']} • {row['photo_type']}")
                file_path = Path(str(row["file_path"]))
                if file_path.exists():
                    st.image(str(file_path), use_container_width=True)
                else:
                    st.warning(f"Missing image file. Metadata kept at {row['file_path']}")
                if row["notes"]:
                    st.write(row["notes"])

st.markdown("### Comparison View")
if all_photos.empty:
    st.info("Upload at least two photos to compare.")
else:
    photo_options = all_photos.apply(lambda row: f"{row['date']} • {row['photo_type']} • {Path(str(row['file_path'])).name}", axis=1).tolist()
    before_label = st.selectbox("Before", photo_options, index=0)
    current_label = st.selectbox("Current", photo_options, index=len(photo_options) - 1)
    before_row = all_photos.iloc[photo_options.index(before_label)]
    current_row = all_photos.iloc[photo_options.index(current_label)]
    c1, c2 = st.columns(2)
    with c1:
        st.caption(before_label)
        before_path = Path(str(before_row["file_path"]))
        if before_path.exists():
            st.image(str(before_path), use_container_width=True)
        else:
            st.warning("Before image file missing.")
    with c2:
        st.caption(current_label)
        current_path = Path(str(current_row["file_path"]))
        if current_path.exists():
            st.image(str(current_path), use_container_width=True)
        else:
            st.warning("Current image file missing.")
