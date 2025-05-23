def search_blogs(df, query):
    """Search blogs by keyword across title, content, and tags."""
    query = query.lower().strip()

    # Clean fields (just in case)
    df['title'] = df['title'].fillna('').astype(str)
    df['content'] = df['content'].fillna('').astype(str)
    df['tags'] = df['tags'].fillna('').astype(str)

    mask = (
        df['title'].str.lower().str.contains(query, na=False) |
        df['content'].str.lower().str.contains(query, na=False) |
        df['tags'].str.lower().str.contains(query, na=False)
    )

    return df[mask]
