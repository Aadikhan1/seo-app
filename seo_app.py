def detect_categories(text):
    text = str(text).lower()
    matched_categories = []
    for category, keywords in category_keywords.items():
        if any(keyword in text for keyword in keywords):
            matched_categories.append(category)
    return ', '.join(set(matched_categories)) if matched_categories else 'Uncategorized'

# Apply category detection on URLs or title column
df['Detected Categories'] = df.iloc[:, 0].apply(detect_categories)
