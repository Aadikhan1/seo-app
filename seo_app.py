import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt
import re
from urllib.parse import urlparse

st.set_page_config(page_title="Advanced Website Category Filter Tool", layout="wide")
st.title("\U0001F50D Advanced Website Category Filter Tool")

uploaded_file = st.file_uploader("\U0001F4C4 Upload your website data file (CSV or Excel)", type=["csv", "xlsx"])

def extract_tld(url):
    try:
        parsed_url = urlparse(url if url.startswith("http") else "http://" + url)
        domain = parsed_url.netloc or parsed_url.path
        parts = domain.split('.')
        return ".".join(parts[-2:]) if len(parts) >= 2 else domain
    except Exception:
        return "Unknown"

if uploaded_file:
    try:
        # Read file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("✅ File uploaded successfully!")

        # -- Extract TLDs from Website or Domain column --
        domain_col = 'Website' if 'Website' in df.columns else st.selectbox("Select column containing URLs/domains", df.columns)
        df['Tld'] = df[domain_col].astype(str).apply(extract_tld)

        st.markdown("### \U0001F4CA Uploaded Data Preview")
        st.dataframe(df.head())

        # -- Category setup --
        st.markdown("---")
        st.subheader("\U0001F9E0 Apply Filters")

        # Category Filter
        category_col = 'Category' if 'Category' in df.columns else st.selectbox("Select column for category filtering", df.columns)
        all_categories = sorted(df[category_col].dropna().unique().tolist())

        with st.expander("\U0001F4C2 Category Filters"):
            col1, col2 = st.columns([1, 3])
            with col1:
                select_all = st.button("✅ Select All Categories")
                clear_all = st.button("❌ Clear All Categories")

            if 'selected_categories' not in st.session_state:
                st.session_state.selected_categories = all_categories

            if select_all:
                st.session_state.selected_categories = all_categories
            if clear_all:
                st.session_state.selected_categories = []

            selected_categories = st.multiselect(
                "Choose Categories to Filter",
                all_categories,
                default=st.session_state.selected_categories
            )

        # -- Country & TLD Filters --
        with st.expander("\U0001F30F Geographic & Domain Filters"):
            col1, col2 = st.columns(2)
            with col1:
                countries = df['Country'].dropna().unique().tolist() if 'Country' in df.columns else []
                selected_countries = st.multiselect("Country Filter", countries)
            with col2:
                tlds = sorted(df['Tld'].dropna().unique().tolist())
                selected_tlds = st.multiselect("ccTLD Filter (Domain Extensions)", tlds, default=tlds)

        # -- Traffic filter --
        with st.expander("\U0001F4C8 Traffic Filters"):
            min_traffic = st.number_input("Minimum Traffic Threshold", value=0)
            max_traffic = st.number_input("Maximum Traffic Threshold", value=1000000)

        # -- Apply filters --
        filtered_df = df.copy()

        if selected_categories:
            filtered_df = filtered_df[filtered_df[category_col].isin(selected_categories)]
        if selected_countries and 'Country' in df.columns:
            filtered_df = filtered_df[filtered_df['Country'].isin(selected_countries)]
        if selected_tlds:
            filtered_df = filtered_df[filtered_df['Tld'].isin(selected_tlds)]
        if 'Traffic' in df.columns:
            filtered_df = filtered_df[(filtered_df['Traffic'] >= min_traffic) & (filtered_df['Traffic'] <= max_traffic)]

        # -- Summary count --
        st.markdown("### \U0001F4CA Website Category Summary")
        category_counts = filtered_df[category_col].value_counts().sort_values(ascending=False)

        summary_cols = st.columns(len(category_counts))
        for col, (cat, count) in zip(summary_cols, category_counts.items()):
            col.metric(cat, count)

        st.dataframe(
            category_counts.reset_index().rename(columns={'index': 'Category', category_col: 'Count'})
        )

        fig, ax = plt.subplots()
        category_counts.plot(kind='barh', ax=ax)
        ax.invert_yaxis()
        ax.set_xlabel("Number of Websites")
        ax.set_ylabel("Category")
        st.pyplot(fig)

        # -- Search functionality --
        st.markdown("### \U0001F50D Search Filter")
        search_col = st.selectbox("Select column to search", df.columns)
        search_term = st.text_input("Enter search term")

        if search_term:
            filtered_df = filtered_df[filtered_df[search_col].astype(str).str.contains(search_term, case=False)]

        # -- Show filtered data --
        st.markdown(f"### ✅ Filtered Results ({len(filtered_df)})")
        st.dataframe(filtered_df)

        # -- Download button --
        def convert_df(df):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False)
            return output.getvalue()

        st.download_button(
            "\U0001F4E5 Download Filtered Data",
            data=convert_df(filtered_df),
            file_name="filtered_websites.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        if st.button("\U0001F504 Reset All"):
            st.session_state.selected_categories = all_categories
            st.experimental_rerun()

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
else:
    st.info("\U0001F4C2 Please upload a CSV or Excel file to begin.")
