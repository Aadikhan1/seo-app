import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Advanced Website Category Filter Tool", layout="wide")
st.title("\U0001F50D Advanced Website Category Filter Tool - NEW")

uploaded_file = st.file_uploader("Upload your website data file (CSV or Excel):", type=["csv", "xlsx"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success(f"Uploaded: {uploaded_file.name}")

        st.markdown("---")
        st.subheader("\U0001F4C2 Category Filters")

        # WorkGine Focus
        with st.container():
            st.markdown("**Focus**")
            workgine_focus = st.multiselect("", ["Software & SaaS"], default=["Software & SaaS"])

        # Key Business Areas
        with st.container():
            st.markdown("**Key Business Areas**")
            key_business = st.multiselect("", [
                "Digital Marketing & SEO", "Business & Finance", "Real Estate",
                "Automotive", "Home Improvement & Gardening"
            ], default=[
                "Digital Marketing & SEO", "Business & Finance", "Real Estate"
            ])

        # Website Purpose/Structure
        with st.container():
            st.markdown("**Filter by Website Purpose/Structure**")
            structure = st.multiselect("", ["Blog / Guest Posting", "Service-Based", "E-commerce"], default=["Blog / Guest Posting"])

        # General Categories
        with st.container():
            st.markdown("**General Categories**")
            general_categories = st.multiselect("", [
                "Business", "Tech", "Fashion", "Sports", "Travel", "Crypto", "Finance", "Education",
                "Health", "Pets", "Law", "Lifestyle", "News", "Photography", "Entertainment", "Food"
            ], default=["Business", "Tech", "Lifestyle"])

        st.markdown("---")
        st.subheader("\U0001F310 Geographic & Domain Filters")

        # Country Filter
        countries = sorted(["Argentina", "Australia", "Austria", "Belgium", "Brazil", "Canada", "Denmark", "France", "Germany",
                    "India", "Ireland", "Italy", "Japan", "Mexico", "Netherlands", "New Zealand", "Norway", "Pakistan",
                    "Philippines", "Russia", "Singapore", "South Africa", "Spain", "Sweden", "Switzerland", "UAE",
                    "UK", "USA", "Other"])
        selected_countries = st.multiselect("Country Filter", countries, default=countries)

        # ccTLD Filter
        cctlds = sorted([".ae", ".ai", ".app", ".at", ".au", ".be", ".ca", ".ch", ".co", ".co.in", ".co.uk", ".com",
                         ".com.ar", ".com.au", ".com.br", ".com.mx", ".com.pk", ".com.sg", ".de", ".dk", ".es", ".eu",
                         ".fr", ".ie", ".in", ".io", ".it", ".jp", ".mx", ".net", ".nl", ".nz", ".online", ".org", ".ph",
                         ".pk", ".pt", ".se", ".sg", ".site", ".store", ".tech", ".uk", ".us", ".xyz"])
        selected_cctlds = st.multiselect("ccTLD Filter (Domain Extensions)", cctlds, default=cctlds)

        st.markdown("---")
        st.subheader("\U0001F4CA Traffic Filters")
        col1, col2 = st.columns(2)
        min_traffic = col1.number_input("Minimum Traffic Threshold:", min_value=0, value=0)
        max_traffic = col2.number_input("Maximum Traffic Threshold:", min_value=0, value=500)

        if st.button("\U0001F527 Process and Filter Websites"):
            filtered_df = df.copy()

            # Dummy filtering logic (should match your real columns)
            filtered_df = filtered_df[
                (filtered_df['Organic Traffic'] >= min_traffic) &
                (filtered_df['Organic Traffic'] <= max_traffic) &
                (filtered_df['Domain'].isin(selected_cctlds))
            ]

            st.markdown("---")
            st.subheader(f"\U0001F4CB Results ({len(filtered_df)})")

            # Category Summary
            st.markdown("**Category Summary:**")
            detected_cat_col = 'Detected Categories' if 'Detected Categories' in filtered_df.columns else df.columns[2]
            category_summary = filtered_df[detected_cat_col].explode().value_counts()
            st.write(category_summary)

            # Download
            def convert_df(df):
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False)
                return output.getvalue()

            st.download_button("\U0001F4E5 Download Results", data=convert_df(filtered_df), file_name="filtered_websites.xlsx")

            st.dataframe(filtered_df, use_container_width=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Please upload a CSV or Excel file to begin.")
