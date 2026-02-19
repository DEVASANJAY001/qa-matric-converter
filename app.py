import streamlit as st
import pandas as pd

st.set_page_config(page_title="DVX Merge Tool", layout="wide")

st.title("DVX + SCA + YARD → Final Merge Tool")

st.write("Upload all 3 files. Final file will keep all DVX columns.")

# Uploaders
dvx_file = st.file_uploader("Upload DVX Excel", type=["xlsx"])
sca_file = st.file_uploader("Upload SCA Excel", type=["xlsx"])
yard_file = st.file_uploader("Upload YARD Excel", type=["xlsx"])

if dvx_file and sca_file and yard_file:

    dvx = pd.read_excel(dvx_file)
    sca = pd.read_excel(sca_file)
    yard = pd.read_excel(yard_file)

    # Clean column names
    dvx.columns = dvx.columns.str.strip()
    sca.columns = sca.columns.str.strip()
    yard.columns = yard.columns.str.strip()

    key = "Defect Description Details"

    if key not in dvx.columns:
        st.error(f"{key} not found in DVX")
        st.stop()

    if key not in sca.columns:
        st.error(f"{key} not found in SCA")
        st.stop()

    if key not in yard.columns:
        st.error(f"{key} not found in YARD")
        st.stop()

    st.success("Files loaded successfully")

    # ===== COMMON COLUMNS =====
    sca_common = [c for c in sca.columns if c in dvx.columns and c != key]
    yard_common = [c for c in yard.columns if c in dvx.columns and c != key]

    sca_use = sca[[key] + sca_common]
    yard_use = yard[[key] + yard_common]

    final = dvx.copy()

    # merge SCA
    final = final.merge(
        sca_use,
        on=key,
        how="left",
        suffixes=("", "_sca")
    )

    # merge YARD
    final = final.merge(
        yard_use,
        on=key,
        how="left",
        suffixes=("", "_yard")
    )

    st.subheader("Preview Final Data")
    st.dataframe(final.head(50), use_container_width=True)

    # download
    output = final.to_excel(index=False, engine="openpyxl")

    import io
    buffer = io.BytesIO()
    final.to_excel(buffer, index=False)
    buffer.seek(0)

    st.download_button(
        label="Download Final Excel",
        data=buffer,
        file_name="FINAL_OUTPUT.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:
    st.info("Upload DVX, SCA and YARD files to begin")
