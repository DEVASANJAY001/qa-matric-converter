import streamlit as st
import pandas as pd

st.set_page_config(page_title="DVX Merge Tool", layout="wide")
st.title("📊 DVX + SCA + YARD → Final Database")

st.write("Upload DVX, SCA and YARD files to generate final merged Excel")

# ---------------- FILE UPLOAD ----------------
dvx_file = st.file_uploader("Upload DVX File", type=["xlsx"])
sca_file = st.file_uploader("Upload SCA File", type=["xlsx"])
yard_file = st.file_uploader("Upload YARD File", type=["xlsx"])

# ---------------- PROCESS ----------------
if st.button("Generate Final File"):

    if not dvx_file:
        st.error("Upload DVX file first")
        st.stop()

    # -------- LOAD DVX --------
    dvx_df = pd.read_excel(dvx_file)
    st.success("DVX Loaded")

    # -------- LOAD SCA --------
    if sca_file:
        sca_df = pd.read_excel(sca_file)
    else:
        sca_df = pd.DataFrame()

    # -------- LOAD YARD --------
    if yard_file:
        yard_df = pd.read_excel(yard_file)
    else:
        yard_df = pd.DataFrame()

    # ---------------- CLEAN COLUMN NAMES ----------------
    dvx_df.columns = dvx_df.columns.str.strip()
    sca_df.columns = sca_df.columns.str.strip()
    yard_df.columns = yard_df.columns.str.strip()

    # ---------------- RENAME TO MATCH DVX ----------------
    if not sca_df.empty:
        sca_df.rename(columns={
            "Defect Description": "Defect Description Details",
            "Defect Responsibility": "Defect Responsibility",
            "Gravity": "Gravity"
        }, inplace=True)

    if not yard_df.empty:
        yard_df.rename(columns={
            "Description": "Defect Description Details",
            "Defect Responsibility": "Defect Responsibility",
            "Gravity": "Gravity"
        }, inplace=True)

    # ---------------- COMMON COLUMNS ----------------
    common_cols = [
        "Defect Description Details",
        "Gravity",
        "Defect Responsibility"
    ]

    # ensure DVX has key column
    if "Defect Description Details" not in dvx_df.columns:
        st.error("DVX must contain 'Defect Description Details'")
        st.stop()

    final_df = dvx_df.copy()

    # ---------------- MERGE SCA ----------------
    if not sca_df.empty and "Defect Description Details" in sca_df.columns:
        sca_subset = sca_df[[c for c in common_cols if c in sca_df.columns]].drop_duplicates()
        final_df = pd.merge(
            final_df,
            sca_subset,
            on="Defect Description Details",
            how="left",
            suffixes=("", "_sca")
        )

    # ---------------- MERGE YARD ----------------
    if not yard_df.empty and "Defect Description Details" in yard_df.columns:
        yard_subset = yard_df[[c for c in common_cols if c in yard_df.columns]].drop_duplicates()
        final_df = pd.merge(
            final_df,
            yard_subset,
            on="Defect Description Details",
            how="left",
            suffixes=("", "_yard")
        )

    st.success("Final file generated")

    st.dataframe(final_df, use_container_width=True)

    # ---------------- DOWNLOAD ----------------
    output_file = "final_merged.xlsx"
    final_df.to_excel(output_file, index=False)

    with open(output_file, "rb") as f:
        st.download_button(
            label="⬇ Download Final Excel",
            data=f,
            file_name="Final_Database.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
