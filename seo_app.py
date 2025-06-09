import streamlit as st
import pandas as pd
import os
import re
from urllib.parse import urlparse

st.set_page_config(page_title="SEO Backlink Filter", layout="wide")

st.title("🔍 SEO Competitor Backlink Filter")

# --- CATEGORY DETECTION LOGIC ---
category_keywords = {
    "Automotive": ["car", "vehicle", "automotive", "engine", "auto"],
    "Real Estate": ["property", "estate", "housing", "real-estate", "rent"],
    "Fashion": ["style", "fashion", "clothing", "wear", "dresses", "outfit"],
    "Lifestyle": ["lifestyle", "life", "home", "interior", "living", "self-care"],
    "Photography": ["photography", "camera", "photo", "images"],
    "Software & SaaS": ["software", "tool", "platform", "app", "solution", "saas"],
    "Travel": ["travel", "trip", "vacation", "tour", "destination"],
    "Education": ["school", "education", "college", "student", "learning"],
    "Business": ["business", "startup", "entrepreneur", "b2b", "brand"],
    "Crypto": ["crypto", "bitcoin", "blockchain", "ethereum", "web3"],
    "Entertainment": ["entertainment", "movies", "shows", "celeb", "music"],
    "SEO & Digital Marketing": ["seo", "digital marketing", "rank", "serp", "ads", "optimization"],
    "E-commerce": ["shop", "store", "ecommerce", "buy", "product", "deal"],
    "Service-Based": ["service", "agency", "consulting", "solution", "freelancer"],
    "Finance": ["finance", "money", "investment", "loan", "bank", "credit"],
    "Law": ["law", "legal", "attorney", "court"],
    "Tech": ["tech", "technology", "ai", "machine learning", "gadgets", "tools"],
    "Health": ["health", "wellness", "fitness", "diet", "mental", "brain"],
    "Food": ["food", "cuisine", "recipe", "kitchen", "cook"],
    "Pets": ["pet", "dog", "cat", "animal", "wildlife"],
    "Blog / Guest Posting": ["guest post", "write for us", "submit article", "contribute"],
    "Sports": ["sports", "football", "cricket", "athlete", "match"],
}

def detect_categories(text):
    text = str(text).lower()
    matched_categories = []
    for category, keywords in category_keywords.items():
        if any(keyword in text for keyword in keywords):
            matched_categories.append(category)
    return ', '.join(set(matched_categories)) if matched_categories else 'Uncategorized'

def extract_tld(domain):
    try:
        netloc = urlparse(domain).netloc
        tld = netloc.split('.')[-1]
        return tld.lower()
    except:
        return ''

# --- SIDEBAR ---
with st.sidebar:
    st.header("📤 Upload Your File")
    uploaded_file = st.file_uploader("Upload Excel or CSV file", type=["xlsx", "csv"])
    st.markdown("---")
    st.markdown("📌 **Instructions:**")
    st.markdown("• Upload a file with a column containing domain URLs or backlinks.\n"
                "• Detected categories and TLDs will auto-populate.\n"
                "• Use filters below the table to refine your view.")

# --- MAIN LOGIC ---
if uploaded_file:
    filename = uploaded_file.name
    if filename.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
    elif filename.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        st.error("Unsupported file format.")
        st.stop()

    st.success("✅ File uploaded successfully!")

    # Detect column with URLs (auto-detect first column if unsure)
    url_column = df.columns[0]

    # Detect categories
    df['Detected Categories'] = df[url_column].apply(detect_categories)

    # Extract TLDs
    df['TLD'] = df[url_column].apply(extract_tld)

    # --- FILTERING CONTROLS ---
    st.subheader("🎛️ Filters")

    # Category filter
    unique_categories = sorted(set(cat for cats in df['Detected Categories'].dropna().str.split(', ') for cat in cats))
    selected_categories = st.multiselect("Filter by Categories", unique_categories, default=unique_categories)

    # TLD filter
    unique_tlds = sorted(df['TLD'].dropna().unique())
    selected_tlds = st.multiselect("Filter by TLDs", unique_tlds, default=unique_tlds)

    # Search bar
    search_query = st.text_input("🔍 Search URLs")

    # Apply filters
    filtered_df = df[df['Detected Categories'].apply(lambda x: any(cat in x for cat in selected_categories))]
    filtered_df = filtered_df[filtered_df['TLD'].isin(selected_tlds)]

    if search_query:
        filtered_df = filtered_df[filtered_df[url_column].str.contains(search_query, case=False, na=False)]

    # --- TABLE DISPLAY ---
    st.subheader(f"📊 Filtered Results ({len(filtered_df)} rows)")
    st.dataframe(filtered_df, use_container_width=True)

    # --- DOWNLOAD ---
    st.download_button("📥 Download Filtered Data", filtered_df.to_csv(index=False), file_name="filtered_backlinks.csv", mime="text/csv")

else:
    st.warning("⬅️ Upload a file to begin.")
