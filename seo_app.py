import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt

st.set_page_config(page_title=Advanced Website Category Filter Tool, layout=wide)
st.title("🕵️ Advanced Website Category Filter Tool")

uploaded_file = st.file_uploader(📤 Upload your website data file (CSV or Excel), type=[csv, xlsx])

if uploaded_file
    try
        if uploaded_file.name.endswith('.csv')
            df = pd.read_csv(uploaded_file)
        else
            df = pd.read_excel(uploaded_file)

        st.success(✅ File uploaded successfully!)
        st.markdown(### 📊 Uploaded Data Preview)
        st.dataframe(df.head())

        # -- Category setup --
        st.markdown(---)
        st.subheader(🧠 Apply Filters)

        category_col = 'Category' if 'Category' in df.columns else st.selectbox(
            Select column for category filtering, df.columns)

        all_categories = sorted(df[category_col].dropna().unique().tolist())

        with st.expander(📂 Category Filters)
            col1, col2 = st.columns([1, 3])
            with col1
                select_all = st.button(✅ Select All Categories)
                clear_all = st.button(❌ Clear All Categories)
            if 'selected_categories' not in st.session_state
                st.session_state.selected_categories = all_categories

            if select_all
                st.session_state.selected_categories = all_categories
            if clear_all
                st.session_state.selected_categories = []

            selected_categories = st.multiselect(Choose Categories to Filter,
                                                 all_categories,
                                                 default=st.session_state.selected_categories)

        # -- Filter data --
        filtered_df = df[df[category_col].isin(selected_categories)] if selected_categories else df

        # -- Summary count --
        st.markdown(### 📊 Website Category Summary)
        category_counts = filtered_df[category_col].value_counts().sort_values(ascending=False)
        st.dataframe(category_counts.reset_index().rename(columns={'index' 'Category', category_col 'Count'}))

        fig, ax = plt.subplots()
        category_counts.plot(kind='barh', ax=ax)
        ax.invert_yaxis()
        ax.set_xlabel(Number of Websites)
        ax.set_ylabel(Category)
        st.pyplot(fig)

        # -- Search functionality --
        st.markdown(### 🔍 Search Filter)
        search_col = st.selectbox(Select column to search, df.columns)
        search_term = st.text_input(Enter search term)
        if search_term
            filtered_df = filtered_df[filtered_df[search_col].astype(str).str.contains(search_term, case=False)]

        # -- Show filtered data --
        st.markdown(### ✅ Filtered Data)
        st.dataframe(filtered_df)

        # -- Download button --
        def convert_df(df)
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer
                df.to_excel(writer, index=False)
            return output.getvalue()

        st.download_button(
            📥 Download Filtered Data,
            data=convert_df(filtered_df),
            file_name=filtered_websites.xlsx,
            mime=applicationvnd.openxmlformats-officedocument.spreadsheetml.sheet
        )

        if st.button(🔄 Reset All)
            st.session_state.selected_categories = all_categories
            st.experimental_rerun()

    except Exception as e
        st.error(f❌ Error processing file {e})

else
    st.info(📂 Please upload a CSV or Excel file to begin.)
