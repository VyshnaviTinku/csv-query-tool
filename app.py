import streamlit as st
import pandas as pd
from core import apply_filters, compute_all_stats

st.set_page_config(page_title="CSV Tool Dashboard", layout="wide")

st.title("📊 CSV Tool Dashboard")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("Raw Data")
    st.dataframe(df)

    # Sidebar filters
    st.sidebar.header("Filters")
    filters = []

    for col in df.columns:
        unique_vals = df[col].dropna().unique()
        if len(unique_vals) < 20:
            selected = st.sidebar.selectbox(col, ["All"] + list(unique_vals))
            if selected != "All":
                filters.append(f"{col}={selected}")

    if filters:
        df = apply_filters(df, filters)

    st.subheader("Filtered Data")
    st.dataframe(df)

    # Stats
    st.subheader("Statistics")
    stats = compute_all_stats(df)
    st.json(stats)

    # Charts
    numeric_cols = df.select_dtypes(include='number').columns

    if len(numeric_cols) > 0:
        col = st.selectbox("Select column", numeric_cols)
        st.bar_chart(df[col])