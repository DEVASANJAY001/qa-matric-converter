import streamlit as st
import pandas as pd

st.title("DVX + SCA + YARD Merge Tool")

st.write("Upload all 3 files. Final file keeps all DVX columns.")

dvx_file = st.file_uploader("Upload DVX Excel", type=["xlsx"])
sca_file = st.file_uploader("Upload SCA Excel", type=["xlsx"])
yard_file = st.file_uploader("Upload YARD Excel", type=["xlsx"])


def clean_columns(df):
    df.columns = df.columns.str.strip().str.lower()
    return df


if dvx_file and sca_file and yard_file:

    dvx = pd.read_excel(dvx_file)
    sca = pd.read_excel(sca_file)
    yard = pd.read_excel(yard_file)

    # Clean column names
    dvx = clean_columns(dvx)
    sca = clean_columns(sca)
    yard = clean_columns(yard)

    # KEY COLUMN
    key = "defect description details"

    if key not in dvx.columns:
        st.error("Column not found in DVX: Defect Description Details")
        st.stop()

    if key not in sca.columns:
        st.error("Column not found in SCA: Defect Description Details")
        st.stop()

    if key not in yard.columns:
        st.error("Column not found in YARD: Defect Description Details")
        st.stop()

    # -------- MERGE SCA --------
    sca_cols_needed = [
        "defect description details",
        "gravity",
        "defect responsibility"
    ]

    sca_small = sca[sca_cols_needed].drop_duplicates()

    merged = pd.merge(
        dvx,
        sca_small,
        on="defect description details",
        how="left",
        suffixes=("", "_sca")
    )

    # -------- MERGE YARD --------
    yard_small = yard.drop_duplicates(subset=[key])

    merged = pd.merge(
        merged,
        yard_small,
        on="defect description details",
        how="left",
        suffixes=("", "_yard")
    )

    st.success("Merge completed!")

    st.dataframe(merged.head())

    output = "FINAL_DVX_MERGED.xlsx"
    merged.to_excel(output, index=False)

    with open(output, "rb") as f:
        st.download_button(
            "Download Final Excel",
            f,
            file_name=output
        )
