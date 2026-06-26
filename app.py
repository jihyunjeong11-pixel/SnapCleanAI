import streamlit as st
import os

from detect import analyze_image
from quality import quality_score
from similarity import get_image_hash, compare_images

st.set_page_config(
    page_title="SnapClean AI",
    page_icon="📸",
    layout="wide"
)

st.title("📸 SnapClean AI")

st.write(
    "AI-powered photo organizer that detects objects, "
    "evaluates image quality, and identifies duplicate photos."
)

uploaded_files = st.file_uploader(
    "Upload Photos",
    accept_multiple_files=True,
    type=["jpg", "jpeg", "png"]
)

if uploaded_files:

    os.makedirs("uploads", exist_ok=True)

    photo_scores = []
    photo_hashes = []

    st.header("📷 Photo Analysis")

    for file in uploaded_files:

        filepath = os.path.join(
            "uploads",
            file.name
        )

        with open(filepath, "wb") as f:
            f.write(file.getbuffer())

        score = quality_score(filepath)

        person_count, objects = analyze_image(filepath)

        img_hash = get_image_hash(filepath)

        photo_scores.append(
            (
                file.name,
                filepath,
                score
            )
        )

        photo_hashes.append(
            (
                file.name,
                filepath,
                img_hash,
                score
            )
        )

        st.subheader(file.name)

        st.image(
            filepath,
            use_container_width=True
        )

        st.write(
            f"👥 People Detected: {person_count}"
        )

        st.write(
            f"🔍 Objects Found: {objects}"
        )

        st.write(
            f"⭐ Quality Score: {score:.2f}"
        )

        if score >= 1200:

            st.success(
                "✅ Best Quality Photo"
            )

            st.success(
                "Recommendation: KEEP"
            )

        elif score >= 700:

            st.info(
                "👍 Acceptable Quality"
            )

            st.info(
                "Recommendation: KEEP"
            )

        else:

            st.warning(
                "📷 Blurry Photo"
            )

            st.warning(
                "Recommendation: REVIEW OR DELETE"
            )

        st.divider()

    # ==========================
    # BEST PHOTO
    # ==========================

    if len(photo_scores) > 0:

        best_photo = max(
            photo_scores,
            key=lambda x: x[2]
        )

        st.header("🏆 Best Photo")

        col1, col2 = st.columns([1, 2])

        with col1:

            st.image(
                best_photo[1],
                use_container_width=True
            )

        with col2:

            st.success(
                f"📸 {best_photo[0]}"
            )

            st.success(
                f"⭐ Quality Score: {best_photo[2]:.2f}"
            )

            st.write(
                "This image has the highest quality score among uploaded photos."
            )

    # ==========================
    # SIMILAR PHOTO GROUPS
    # ==========================

    if len(photo_hashes) > 1:

        st.header(
            "📂 Similar Photo Groups"
        )

        delete_candidates = []

        visited = set()

        for i in range(len(photo_hashes)):

            if i in visited:
                continue

            current_group = [
                photo_hashes[i]
            ]

            for j in range(
                i + 1,
                len(photo_hashes)
            ):

                distance = compare_images(
                    photo_hashes[i][2],
                    photo_hashes[j][2]
                )

                if distance < 8:

                    current_group.append(
                        photo_hashes[j]
                    )

                    visited.add(j)

            if len(current_group) > 1:

                st.subheader(
                    "Similar Group"
                )

                for item in current_group:

                    st.write(
                        f"📷 {item[0]} | Quality Score: {item[3]:.2f}"
                    )

                best = max(
                    current_group,
                    key=lambda x: x[3]
                )

                st.success(
                    f"✅ KEEP: {best[0]}"
                )

                for item in current_group:

                    if item[0] != best[0]:

                        delete_candidates.append(
                            item[0]
                        )

        st.header(
            "🗑️ Delete Candidates"
        )

        if delete_candidates:

            for candidate in delete_candidates:

                st.warning(
                    candidate
                )

        else:

            st.success(
                "No duplicate photos detected."
            )

st.markdown("---")

st.caption(
    "Built with Python, YOLOv8, OpenCV, ImageHash, and Streamlit"
)