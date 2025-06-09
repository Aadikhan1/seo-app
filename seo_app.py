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
        "Automotive": ["car", "vehicle", "automotive", "engine", "auto", "garage", "dealership", "tires"],
        "Real Estate": ["property", "estate", "housing", "real-estate", "rent", "apartment", "mortgage", "realtor"],
        "Fashion": ["style", "fashion", "clothing", "wear", "dresses", "outfit", "runway", "couture", "accessories"],
        "Lifestyle": ["lifestyle", "life", "home", "interior", "living", "decor", "inspiration", "habits"],
        "Photography": ["photography", "camera", "photo", "image", "lens", "dslr", "portfolio", "editor"],
        "Software & SaaS": ["software", "tool", "platform", "app", "solution", "SaaS", "API", "integration"],
        "Travel": ["travel", "trip", "vacation", "tour", "destination", "journey", "holiday", "flight", "hotel"],
        "Education": ["school", "education", "college", "student", "learning", "university", "degree", "tutor"],
        "Business": ["business", "startup", "entrepreneur", "b2b", "brand", "management", "leadership", "operations"],
        "Crypto": ["crypto", "bitcoin", "blockchain", "ethereum", "web3", "nft", "defi", "altcoin", "token"],
        "Entertainment": ["entertainment", "movies", "shows", "celeb", "music", "tv", "trailer", "stream"],
        "Digital Marketing & SEO": ["seo", "digital marketing", "rank", "SERP", "ads", "backlink", "traffic", "campaign"],
        "E-commerce": ["shop", "store", "ecommerce", "buy", "product", "deal", "checkout", "cart"],
        "Service-Based": ["service", "agency", "consulting", "solution", "freelancer", "expert", "support"],
        "Finance": ["finance", "money", "investment", "loan", "bank", "credit", "stocks", "trading", "budget"],
        "Law": ["law", "legal", "attorney", "court", "case", "justice", "compliance", "regulation"],
        "Tech": ["tech", "technology", "AI", "machine learning", "gadgets", "coding", "development", "innovation"],
        "Health": ["health", "wellness", "fitness", "diet", "mental", "exercise", "med", "clinic"],
        "Food": ["food", "cuisine", "recipe", "kitchen", "cook", "dish", "restaurant", "meal"],
        "Pets": ["pet", "dog", "cat", "animal", "vet", "puppy", "grooming", "adoption"],
        "Blog / Guest Posting": ["guest post", "write for us", "submit article", "contribute", "blogging", "editorial"],
        "Sports": ["sports", "football", "cricket", "athlete", "tournament", "league", "match", "score"],
        "Home Improvement & Gardening": ["renovation", "garden", "DIY", "landscape", "furniture", "tools"],
        "Beauty & Personal Care": ["skincare", "makeup", "cosmetics", "beauty", "hair", "salon", "spa"],
        "Parenting & Family": ["parent", "mom", "dad", "child", "baby", "family", "kids", "parenting"],
        "Jobs & Career": ["career", "job", "resume", "interview", "recruitment", "hiring", "vacancy"],
        "News & Media": ["news", "breaking", "media", "report", "journal", "headline"],
        "Religion & Spirituality": ["religion", "spiritual", "faith", "god", "church", "temple", "belief", "bible"],
        "Science & Research": ["science", "research", "experiment", "study", "data", "lab"],
        "Games & Gaming": ["games", "gaming", "esports", "console", "pc game", "mobile game", "stream"],
        "Art & Design": ["art", "design", "painting", "illustration", "graphic", "gallery"],
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
    tld_list = [
        ".com", ".net", ".org", ".info", ".biz", ".co", ".us", ".uk", ".ca", ".au", ".in", ".de", ".fr", ".cn",
        ".jp", ".br", ".ru", ".it", ".es", ".nl", ".se", ".no", ".fi", ".za", ".mx", ".ar", ".pl", ".tr", ".id", ".ir",
        ".ae", ".kr", ".sg", ".nz", ".my", ".hk", ".ch", ".at", ".be", ".cz", ".gr", ".pt", ".ro", ".hu", ".sk", ".bg",
        ".lt", ".lv", ".ee", ".ph", ".th", ".vn", ".sa", ".ng", ".pk", ".bd", ".lk", ".eg", ".il", ".ua", ".by", ".kz",
        ".tv", ".me", ".cc", ".xyz", ".site", ".online", ".store", ".tech", ".app", ".io", ".dev", ".ai", ".cloud",
        ".space", ".website", ".fun", ".news", ".live", ".media", ".blog", ".shop", ".design", ".pro", ".jobs",
        ".name", ".travel", ".mobi", ".tel", ".museum", ".coop", ".int", ".gov", ".edu", ".mil"
    ]
    unique_tlds = sorted(tld_list)

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

        # Apply General Categories filter
        if general_cats:
            def filter_by_categories(row):
                categories = str(row['Detected Categories']).split(', ')
                return any(cat.strip() in general_cats for cat in categories)
            filtered_df = filtered_df[filtered_df.apply(filter_by_categories, axis=1)]

        st.subheader(f"📋 Results ({len(filtered_df)})")

        # TLD Summary
        tld_counts = filtered_df['Tld'].value_counts().to_dict()
        tld_summary = ', '.join([f"{k} ({v})" for k, v in tld_counts.items()])
        st.markdown(f"**TLD Summary:** {tld_summary}")

        # Category Summary
        if 'Detected Categories' not in filtered_df.columns:
            filtered_df['Detected Categories'] = 'Uncategorized'

        category_list = filtered_df['Detected Categories'].dropna().str.split(', ').explode().tolist()
        cat_counter = Counter(category_list)
        cat_summary = ', '.join([f"{cat} ({count})" for cat, count in cat_counter.items() if cat])
        st.markdown(f"**Category Summary:** {cat_summary}")

        # Display filtered results
        st.dataframe(filtered_df[['Domain', 'Traffic', 'Detected Categories', 'Tld']])

        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download Results", csv_data, file_name="filtered_websites.csv", mime='text/csv')
