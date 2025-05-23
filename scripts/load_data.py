# scripts/load_data.py

import pandas as pd
import streamlit as st

@st.cache_resource
def load_blog_data(parquet_path='data/blogs.parquet'):
    """Load preprocessed blog data from Parquet file."""
    df = pd.read_parquet(parquet_path)
    df.columns = df.columns.str.lower().str.strip()

    # Ensure required columns exist
    if 'title' not in df.columns or 'content' not in df.columns:
        raise ValueError("Missing required columns: 'title' and/or 'content'")

    # Drop rows with missing content
    df = df.dropna(subset=['title', 'content'])

    # Return relevant columns only
    return df[['title', 'content', 'tags']] if 'tags' in df.columns else df[['title', 'content']]
