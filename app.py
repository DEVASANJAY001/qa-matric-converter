import streamlit as st
import pandas as pd

st.title("DVX + SCA + YARD Final Builder")

dvx_file = st.file_uploader("Upload DVX", type=["xlsx"])
sca_file = st.file_uploader("Upload SCA", type=["xlsx"])
yard_file = st.file_uploader("Upload YARD", type=["xlsx"])

if st.button("Generate Final"):

    if not dvx_file:
        st.error("Upload DVX first")
        st.stop()

    # ---------------- LOAD DVX ----------------
    dvx = pd.read_excel(dvx_file)
    dvx.columns = dvx.columns.str.strip()

    dvx_cols = dvx.columns.tolist()
    key = "Defect Description Details"

    final_df = dvx.copy()

    # ---------------- SCA ----------------
    if sca_file:
        sca = pd.read_excel(sca_file)
        sca.columns = sca.columns.str.strip()

        if key in sca.columns:

            # only common cols
            sca_common = ["Defect Description Details", "Gravity"]
            sca_common = [c for c in sca_common if c in sca.columns]

            sca_subset = sca[sca_common].drop_duplicates()

            # create DVX format rows
            sca_rows = pd.DataFrame(columns=dvx_cols)

            for _, row in sca_subset.iterrows():
                new_row = {col: "" for col in dvx_cols}

                for col in sca_common:
                    if col in dvx_cols:
                        new_row[col] = row[col]

                sca_rows = pd.concat([sca_rows, pd.DataFrame([new_row])], ignore_index=True)

            final_df = pd.concat([final_df, sca_rows], ignore_index=True)

    # ---------------- YARD ----------------
    if yard_file:
        yard = pd.read_excel(yard_file)
        yard.columns = yard.columns.str.strip()

        if key in yard.columns:

            yard_subset = yard[[key]].drop_duplicates()

            yard_rows = pd.DataFrame(columns=dvx_cols)

            for _, row in yard_subset.iterrows():
                new_row = {col: "" for col in dvx_cols}
                new_row[key] = row[key]

                yard_rows = pd.concat([yard_rows, pd.DataFrame([new_row])], ignore_index=True)

            final_df = pd.concat([final_df, yard_rows], ignore_index=True)

    st.success("Final ready")
    st.dataframe(final_df)

    final_df.to_excel("final.xlsx", index=False)

    with open("final.xlsx", "rb") as f:
        st.download_button("Download Final Excel", f, file_name="Final.xlsx")
