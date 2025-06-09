import streamlit as st
import pandas as pd
import os
from urllib.parse import urlparse

st.set_page_config(page_title="Advanced Website Category Filter Tool", layout="wide")
st.title("🔎 Advanced Website Category Filter Tool")

uploaded_file = st.file_uploader("Upload your website data file (CSV or Excel):", type=['csv', 'xlsx'])

if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Extract domain and TLD from URL
    def extract_domain(url):
        try:
            parsed = urlparse(url)
            return parsed.netloc if parsed.netloc else parsed.path
        except:
            return ""

    def extract_tld(domain):
        parts = domain.lower().split('.')
        return '.' + parts[-1] if len(parts) > 1 else ''

    df['Domain'] = df.iloc[:, 0].apply(extract_domain)
    df['Tld'] = df['Domain'].apply(extract_tld)

    # All unique TLDs
    unique_tlds = sorted(df['Tld'].unique())

    # Sidebar TLD filter
    with st.expander("🌍 Geographic & Domain Filters"):
        selected_tlds = st.multiselect("ccTLD Filter (Domain Extensions):", options=unique_tlds, default=unique_tlds)

    # Traffic Filters
    with st.expander("📈 Traffic Filters"):
        col1, col2 = st.columns(2)
        with col1:
            min_traffic = st.number_input("Minimum Traffic Threshold:", value=0)
        with col2:
            max_traffic = st.number_input("Maximum Traffic Threshold:", value=500)

    # Filter button
    if st.button("⚙️ Process and Filter Websites"):
        filtered_df = df[df['Tld'].isin(selected_tlds)]

        if 'Traffic' in df.columns:
            filtered_df = filtered_df[(filtered_df['Traffic'] >= min_traffic) & (filtered_df['Traffic'] <= max_traffic)]
        else:
            filtered_df['Traffic'] = 0

        st.subheader(f"📋 Results ({len(filtered_df)})")

        # Count of TLDs
        tld_counts = filtered_df['Tld'].value_counts().to_dict()
        tld_summary = ', '.join([f"{k} ({v})" for k, v in tld_counts.items()])
        st.markdown(f"**TLD Summary:** {tld_summary}")

        # Detect categories if available
        if 'Detected Categories' not in filtered_df.columns:
            filtered_df['Detected Categories'] = 'Unknown'

        # Count of categories
        from collections import Counter
        category_list = filtered_df['Detected Categories'].astype(str).str.split(', ')
        flat_categories = [item for sublist in category_list for item in sublist]
        cat_counter = Counter(flat_categories)
        cat_summary = ', '.join([f"{cat} ({count})" for cat, count in cat_counter.items()])
        st.markdown(f"**Category Summary:** {cat_summary}")

        st.dataframe(filtered_df[['Domain', 'Traffic', 'Detected Categories', 'Tld']])
        st.download_button("⬇️ Download Results", filtered_df.to_csv(index=False), file_name="filtered_websites.csv")
