import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt

st.set_page_config(page_title="Advanced Website Category Filter Tool", layout="wide")
st.title("🕵️ Advanced Website Category Filter Tool")

uploaded_file = st.file_uploader("📤 Upload your website data file (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file:
    try:
        # Read file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("✅ File uploaded successfully!")
        st.markdown("### 📊 Uploaded Data Preview")
        st.dataframe(df.head(), use_container_width=True)

        # -- Category setup --
        st.markdown("---")
        st.subheader("🧠 Apply Filters")

        # Auto-detect category column or let user select
        category_col = None
        possible_category_cols = ['Category', 'category', 'Type', 'type', 'Group', 'group']
        
        for col in possible_category_cols:
            if col in df.columns:
                category_col = col
                break
                
        if category_col is None:
            category_col = st.selectbox(
                "Select column for category filtering", 
                df.columns,
                key="category_col_selector"
            )
        
        all_categories = sorted(df[category_col].dropna().unique().tolist())

        if 'selected_categories' not in st.session_state:
            st.session_state.selected_categories = all_categories

        # -- Category summary stats (as buttons above table) --
        st.markdown("### 📌 Website Category Summary")
        category_counts = df[category_col].value_counts()
        
        # Create columns for the category buttons
        num_columns = min(5, len(category_counts))  # Max 5 columns
        cols = st.columns(num_columns)
        
        # Display category buttons with counts
        for i, (cat, count) in enumerate(category_counts.items()):
            with cols[i % num_columns]:
                st.button(
                    f"{cat} ({count})",
                    key=f"cat_{i}",
                    help=f"Click to filter by {cat} category",
                    on_click=lambda c=cat: st.session_state.update({
                        'selected_categories': [c]
                    })
                )

        # -- Filter controls --
        with st.expander("📂 Category Filters", expanded=True):
            col1, col2 = st.columns([1, 3])

            with col1:
                if st.button("✅ Select All Categories"):
                    st.session_state.selected_categories = all_categories
                if st.button("❌ Clear All Categories"):
                    st.session_state.selected_categories = []
                if st.button("🔄 Reset Filters"):
                    st.session_state.selected_categories = all_categories
                    st.experimental_rerun()

            with col2:
                selected_categories = st.multiselect(
                    "Choose Categories to Filter",
                    all_categories,
                    default=st.session_state.selected_categories,
                    key="category_selector"
                )

        # Filter data based on selected categories
        if selected_categories:
            filtered_df = df[df[category_col].isin(selected_categories)]
            st.success(f"Showing {len(filtered_df)} websites from {len(selected_categories)} selected categories")
        else:
            filtered_df = df.copy()
            st.warning("No categories selected - showing all websites")

        # Show filtered data with counts per category
        st.markdown("### ✅ Filtered Data by Category")
        
        # Display category counts for filtered data
        filtered_counts = filtered_df[category_col].value_counts()
        st.markdown("**Filtered Categories Count:**")
        count_cols = st.columns(len(filtered_counts))
        for i, (cat, count) in enumerate(filtered_counts.items()):
            count_cols[i].metric(label=cat, value=count)
        
        st.dataframe(filtered_df, use_container_width=True)

        # -- Visualizations --
        st.markdown("---")
        st.subheader("📈 Data Visualization")
        
        tab1, tab2 = st.tabs(["Bar Chart", "Pie Chart"])
        
        with tab1:
            fig1, ax1 = plt.subplots()
            filtered_counts.plot(kind='barh', ax=ax1, color="skyblue")
            ax1.invert_yaxis()
            ax1.set_xlabel("Number of Websites")
            ax1.set_ylabel("Category")
            ax1.set_title("Website Categories Distribution")
            st.pyplot(fig1)
            
        with tab2:
            fig2, ax2 = plt.subplots()
            filtered_counts.plot(kind='pie', ax=ax2, autopct='%1.1f%%')
            ax2.set_ylabel("")
            ax2.set_title("Website Categories Proportion")
            st.pyplot(fig2)

        # -- Search functionality --
        st.markdown("---")
        st.subheader("🔍 Search Within Filtered Data")
        
        search_col = st.selectbox(
            "Select column to search", 
            df.columns,
            key="search_col"
        )
        search_term = st.text_input(
            "Enter search term", 
            key="search_term"
        )

        if search_term:
            search_df = filtered_df[
                filtered_df[search_col].astype(str).str.contains(search_term, case=False)
            ]
            st.success(f"Found {len(search_df)} matches for '{search_term}'")
            
            if not search_df.empty:
                st.dataframe(search_df, use_container_width=True)
            else:
                st.warning("No matches found in filtered data")

        # -- Download button --
        st.markdown("---")
        st.subheader("💾 Export Data")
        
        def convert_df(df):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False)
            return output.getvalue()

        st.download_button(
            "📥 Download Filtered Data (Excel)",
            data=convert_df(filtered_df),
            file_name="filtered_websites.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # CSV download option
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Download Filtered Data (CSV)",
            data=csv,
            file_name="filtered_websites.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
        st.error(str(e))
else:
    st.info("📂 Please upload a CSV or Excel file to begin.")
