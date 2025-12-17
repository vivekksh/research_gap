import streamlit as st
from pathlib import Path
import shutil
import subprocess
import json
import sys

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="AI Research Gap Discovery",
    layout="wide"
)

st.title("LooPX")
st.markdown(
    """
    Upload research papers (**PDF format**) from **any domain**.  
    The system analyzes *limitations* across papers and automatically
    discovers **recurring, unresolved research gaps**.
    """
)

st.divider()

# -------------------- FILE UPLOAD --------------------
uploaded_files = st.file_uploader(
    "📤 Upload Research Papers",
    type=["pdf"],
    accept_multiple_files=True
)

# -------------------- ANALYSIS PIPELINE --------------------
if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} paper(s) uploaded.")

    if st.button("🚀 Analyze Papers"):
        with st.spinner("Analyzing papers and discovering research gaps..."):
            try:
                # Prepare papers directory
                papers_dir = Path("data/papers")
                if papers_dir.exists():
                    shutil.rmtree(papers_dir)
                papers_dir.mkdir(parents=True, exist_ok=True)

                # Save uploaded PDFs
                for file in uploaded_files:
                    with open(papers_dir / file.name, "wb") as f:
                        f.write(file.read())

                # Run pipeline using SAME Python executable
                subprocess.run(
                    [sys.executable, "scripts/process_papers.py"],
                    check=True
                )
                subprocess.run(
                    [sys.executable, "scripts/cluster_limitations.py"],
                    check=True
                )

            except Exception as e:
                st.error("❌ Analysis failed. See error details below.")
                st.exception(e)
                st.stop()

        st.success("🎉 Analysis complete!")

        # -------------------- DISPLAY RESULTS --------------------
        results_path = Path("output/gap_results.json")
        text_path = Path("output/gap_results.txt")

        if not results_path.exists():
            st.error("❌ Results file not found. Analysis may have failed.")
            st.stop()

        gaps = json.loads(results_path.read_text(encoding="utf-8"))

        st.divider()
        st.header("📊 Discovered Research Gaps")

        for gap in gaps:
            with st.container(border=True):
                st.subheader(f"🔹 Gap {gap['gap_id']}: {gap['title']}")

                col1, col2 = st.columns([4, 1])
                with col2:
                    st.metric(
                        label="Mentions",
                        value=gap["frequency"]
                    )

                st.markdown("**Description**")
                st.write(gap["description"])

                st.markdown("**Supporting Evidence from Papers**")
                for sent in gap["evidence"]:
                    st.markdown(f"- {sent}")

        st.divider()

        # -------------------- DOWNLOAD --------------------
        if text_path.exists():
            st.download_button(
                label="📥 Download Research Gaps (Text)",
                data=text_path.read_text(encoding="utf-8"),
                file_name="research_gaps.txt"
            )
  
  
  # app.py

# import streamlit as st
# import os
# from scripts.process_papers import process_papers
# from scripts.cluster_limitations import cluster_limitations

# st.set_page_config(page_title="LOOPX", layout="wide")

# st.title("LOOPX – Research Gap Discovery")
# st.write(
#     "Upload academic research papers (PDF). "
#     "LOOPX will analyze limitations and identify recurring research gaps."
# )

# uploaded_files = st.file_uploader(
#     "Upload research papers",
#     type=["pdf"],
#     accept_multiple_files=True
# )

# if uploaded_files:
#     os.makedirs("data/papers", exist_ok=True)

#     # Save uploaded PDFs
#     for file in uploaded_files:
#         with open(os.path.join("data/papers", file.name), "wb") as f:
#             f.write(file.read())

#     if st.button("Analyze Papers"):
#         with st.spinner("Analyzing papers and discovering research gaps..."):
#             process_papers(
#                 papers_dir="data/papers",
#                 output_file="output/all_limitations.txt"
#             )

#             cluster_limitations(
#                 input_file="output/all_limitations.txt",
#                 output_file="output/gap_clusters.txt"
#             )

#         st.success("Analysis complete!")

#         if os.path.exists("output/gap_clusters.txt"):
#             with open("output/gap_clusters.txt", "r", encoding="utf-8") as f:
#                 st.text(f.read())
