import streamlit as st
import io

from eda.loader import load_dataset
from eda.overview import dataset_overview
from eda.quality import data_quality
from eda.statistics import (
    get_column_types,
    numeric_statistics,
    categorical_statistics
)
from eda.visualization import (
    sample_data,
    plot_numeric,
    plot_categorical
)
from eda.report import generate_excel_report


# ---------------- PAGE CONFIG ----------------
st.set_page_config(layout="wide")
st.title("Smart Data Exploration Platform")
st.write("Upload any CSV or Excel dataset to perform automatic EDA")

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader(
    "Upload Dataset",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    df = load_dataset(uploaded_file)

    # ---------------- OVERVIEW ----------------
    st.header("📌 Dataset Overview")
    overview = dataset_overview(df)
    st.json(overview)

    if len(df) > 100000:
        st.warning(
            "Large dataset detected. Visualizations use sampled data for performance."
        )

    # ---------------- PREVIEW ----------------
    st.header("🔍 Data Preview (First 100 Rows)")
    st.dataframe(df.head(100))

    # ---------------- QUALITY ----------------
    st.header("🧹 Data Quality Analysis")
    quality = data_quality(df)

    st.subheader("Missing Values")
    missing_df = quality["Missing Count"][quality["Missing Count"] > 0]
    st.dataframe(missing_df)

    st.write("Duplicate Rows:", quality["Duplicate Rows"])

    # ---------------- STATISTICS ----------------
    st.header("📊 Statistical Summary")
    numeric_cols, categorical_cols = get_column_types(df)

    numeric_stats = None
    categorical_stats = {}

    if numeric_cols:
        st.subheader("Numeric Columns")
        numeric_stats = numeric_statistics(df, numeric_cols)
        st.dataframe(numeric_stats)

    if categorical_cols:
        st.subheader("Categorical Columns (Top 10 Values)")
        categorical_stats = categorical_statistics(df, categorical_cols)
        for col, values in categorical_stats.items():
            st.write(f"**{col}**")
            st.dataframe(values)

    # ---------------- VISUALIZATION ----------------
    st.header("📈 Visual Exploration")
    sampled_df = sample_data(df)

    plot_section = st.radio(
        "Choose Data Type to Visualize",
        ["Numeric", "Categorical"]
    )

    # ---- NUMERIC PLOTS ----
    if plot_section == "Numeric" and numeric_cols:
        col = st.selectbox("Select Numeric Column", numeric_cols)
        plot_type = st.selectbox(
            "Select Plot Type",
            ["Histogram", "Box Plot", "Line Plot"]
        )

        fig = plot_numeric(sampled_df, col, plot_type)
        st.pyplot(fig)

        # Download numeric plot
        img_buf = io.BytesIO()
        fig.savefig(img_buf, format="png", bbox_inches="tight")
        img_buf.seek(0)

        st.download_button(
            label="Download Visualization (PNG)",
            data=img_buf,
            file_name=f"{col}_{plot_type}.png",
            mime="image/png"
        )

    # ---- CATEGORICAL PLOTS ----
    if plot_section == "Categorical" and categorical_cols:
        col = st.selectbox("Select Categorical Column", categorical_cols)

        fig = plot_categorical(sampled_df, col)
        st.pyplot(fig)

        # Download categorical plot
        img_buf = io.BytesIO()
        fig.savefig(img_buf, format="png", bbox_inches="tight")
        img_buf.seek(0)

        st.download_button(
            label="Download Visualization (PNG)",
            data=img_buf,
            file_name=f"{col}_bar_chart.png",
            mime="image/png"
        )

    # ---------------- FULL REPORT DOWNLOAD ----------------
    st.header("📥 Download Full EDA Report")

    excel_report = generate_excel_report(
        overview,
        quality,
        numeric_stats,
        categorical_stats
    )

    st.download_button(
        label="Download Full EDA Report (Excel)",
        data=excel_report,
        file_name="EDA_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )