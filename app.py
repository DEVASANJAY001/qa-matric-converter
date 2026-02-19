import streamlit as st
import pandas as pd

st.title("DVX + SCA + YARD Merge Tool")

dvx_file = st.file_uploader("Upload DVX", type=["xlsx"])
sca_file = st.file_uploader("Upload SCA", type=["xlsx"])
yard_file = st.file_uploader("Upload YARD", type=["xlsx"])

if st.button("Merge Files"):

    if not dvx_file:
        st.error("Upload DVX file first")
        st.stop()

    # ---------------- LOAD ----------------
    dvx = pd.read_excel(dvx_file)
    dvx.columns = dvx.columns.str.strip()

    final_df = dvx.copy()

    key_col = "Defect Description Details"

    if key_col not in final_df.columns:
        st.error("DVX must contain 'Defect Description Details'")
        st.stop()

    # ---------------- SCA MERGE ----------------
    if sca_file:
        sca = pd.read_excel(sca_file)
        sca.columns = sca.columns.str.strip()

        if key_col in sca.columns:

            # find common columns between DVX & SCA
            common_cols_sca = list(set(dvx.columns).intersection(set(sca.columns)))
            common_cols_sca.remove(key_col)

            sca_subset = sca[[key_col] + common_cols_sca].drop_duplicates()

            final_df = final_df.merge(
                sca_subset,
                on=key_col,
                how="left",
                suffixes=("", "_sca")
            )

            # fill DVX blanks with SCA values
            for col in common_cols_sca:
                if col + "_sca" in final_df.columns:
                    final_df[col] = final_df[col].combine_first(final_df[col + "_sca"])
                    final_df.drop(columns=[col + "_sca"], inplace=True)

    # ---------------- YARD MERGE ----------------
    if yard_file:
        yard = pd.read_excel(yard_file)
        yard.columns = yard.columns.str.strip()

        if key_col in yard.columns:

            common_cols_yard = list(set(dvx.columns).intersection(set(yard.columns)))
            common_cols_yard.remove(key_col)

            yard_subset = yard[[key_col] + common_cols_yard].drop_duplicates()

            final_df = final_df.merge(
                yard_subset,
                on=key_col,
                how="left",
                suffixes=("", "_yard")
            )

            for col in common_cols_yard:
                if col + "_yard" in final_df.columns:
                    final_df[col] = final_df[col].combine_first(final_df[col + "_yard"])
                    final_df.drop(columns=[col + "_yard"], inplace=True)

    st.success("Final file ready")
    st.dataframe(final_df)

    final_df.to_excel("final.xlsx", index=False)

    with open("final.xlsx", "rb") as f:
        st.download_button(
            "Download Final Excel",
            f,
            file_name="Final_DVX.xlsx"
        )
