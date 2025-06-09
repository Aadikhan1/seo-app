import streamlit as st
import pandas as pd
from urllib.parse import urlparse
from collections import Counter
import base64

# Streamlit page config
st.set_page_config(page_title="Advanced Website Category Filter Tool", layout="wide")
st.markdown("""
    <style>
    .css-18e3th9 {padding-top: 2rem;}
    .stButton > button {width: 100%;}
    .block-container {padding-top: 1rem;}
    .css-1d391kg {gap: 1rem;}
    .css-1kyxreq {gap: 1rem;}
    </style>
""", unsafe_allow_html=True)

st.title("🔎 Advanced Website Category Filter Tool")

# File Upload
uploaded_file = st.file_uploader("Upload your website data file (CSV or Excel):", type=['csv', 'xlsx'])

if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Extract domain and TLD
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

    # Category detection based on keywords
    category_keywords = {
        "Automotive": ["car", "vehicle", "automotive", "engine", "auto"],
        "Real Estate": ["property", "estate", "housing", "real-estate", "rent"],
        "Fashion": ["style", "fashion", "clothing", "wear", "dresses", "outfit"],
        "Lifestyle": ["lifestyle", "life", "home", "interior", "living"],
        "Photography": ["photography", "camera", "photo", "images"],
        "Software & SaaS": ["software", "tool", "platform", "app", "solution", "SaaS"],
        "Travel": ["travel", "trip", "vacation", "tour", "destination"],
        "Education": ["school", "education", "college", "student", "learning"],
        "Business": ["business", "startup", "entrepreneur", "b2b", "brand"],
        "Crypto": ["crypto", "bitcoin", "blockchain", "ethereum", "web3"],
        "Entertainment": ["entertainment", "movies", "shows", "celeb"],
        "Digital Marketing & SEO": ["seo", "digital marketing", "rank", "SERP", "ads"],
        "E-commerce": ["shop", "store", "ecommerce", "buy", "product", "deal"],
        "Service-Based": ["service", "agency", "consulting", "solution", "freelancer"],
        "Finance": ["finance", "money", "investment", "loan", "bank", "credit"],
        "Law": ["law", "legal", "attorney", "court"],
        "Tech": ["tech", "technology", "AI", "machine learning", "gadgets"],
        "Health": ["health", "wellness", "fitness", "diet", "mental"],
        "Food": ["food", "cuisine", "recipe", "kitchen"],
        "Pets": ["pet", "dog", "cat", "animal"],
        "Blog / Guest Posting": ["guest post", "write for us", "submit article", "contribute"],
        "Sports": ["sports", "football", "cricket", "athlete"]
    }
    def detect_categories(text):
        text = str(text).lower()
        matched_categories = []
        for category, keywords in category_keywords.items():
            if any(keyword in text for keyword in keywords):
                matched_categories.append(category)
        return ', '.join(set(matched_categories)) if matched_categories else 'Uncategorized'

    # Apply category detection on URLs or title column
    df['Detected Categories'] = df.iloc[:, 0].apply(detect_categories)

    # Unique TLDs
    unique_tlds = sorted(df['Tld'].unique())

    # Category Filters
    with st.expander("🗂️ Category Filters"):
        st.markdown("**WorkGine Focus**")
        wg_focus = st.multiselect("", ["Software & SaaS"], default=["Software & SaaS"])

        st.markdown("**Key Business Areas**")
        key_areas = st.multiselect("", ["Digital Marketing & SEO", "Business & Finance", "Real Estate", "Automotive", "Home Improvement & Gardening"], default=[])

        st.markdown("**Filter by Website Purpose/Structure**")
        purposes = st.multiselect("", ["Blog / Guest Posting", "Service-Based", "E-commerce"], default=[])

        st.markdown("**General Categories**")
        general_cats = st.multiselect("", ["Business", "Tech", "Fashion", "Sports", "Travel", "Crypto", "Finance", "Education", "Health", "Law", "Lifestyle", "Music", "Pets", "Photography", "Entertainment", "Food"], default=[])

    # Geographic & Domain Filters
    with st.expander("🌍 Geographic & Domain Filters"):
        col1, col2 = st.columns(2)
        with col1:
            selected_countries = st.multiselect("Country Filter", ["USA", "UK", "India", "Australia", "Germany", "Canada", "Other"], default=[])
        with col2:
            selected_tlds = st.multiselect("ccTLD Filter (Domain Extensions):", options=unique_tlds, default=unique_tlds)

    # Traffic Filters
    with st.expander("📈 Traffic Filters"):
        col1, col2 = st.columns(2)
        with col1:
            min_traffic = st.number_input("Minimum Traffic Threshold:", value=0)
        with col2:
            max_traffic = st.number_input("Maximum Traffic Threshold:", value=500)

    # Process Button
    if st.button("⚙️ Process and Filter Websites"):
        filtered_df = df[df['Tld'].isin(selected_tlds)]

        if 'Traffic' in df.columns:
            filtered_df = filtered_df[(filtered_df['Traffic'] >= min_traffic) & (filtered_df['Traffic'] <= max_traffic)]
        else:
            filtered_df['Traffic'] = 0

        st.subheader(f"📋 Results ({len(filtered_df)})")

        # TLD Summary
        tld_counts = filtered_df['Tld'].value_counts().to_dict()
        tld_summary = ', '.join([f"{k} ({v})" for k, v in tld_counts.items()])
        st.markdown(f"**TLD Summary:** {tld_summary}")

        # Category Summary
        if 'Detected Categories' not in filtered_df.columns:
            filtered_df['Detected Categories'] = 'Uncategorized'

        category_list = filtered_df['Detected Categories'].astype(str).str.split(', ')
        flat_categories = [item for sublist in category_list for item in sublist]
        cat_counter = Counter(flat_categories)
        cat_summary = ', '.join([f"{cat} ({count})" for cat, count in cat_counter.items()])
        st.markdown(f"**Category Summary:** {cat_summary}")

        # Display filtered results
        st.dataframe(filtered_df[['Domain', 'Traffic', 'Detected Categories', 'Tld']])

        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download Results", csv_data, file_name="filtered_websites.csv", mime='text/csv')
