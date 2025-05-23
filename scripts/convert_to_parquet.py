import pandas as pd

# Load original CSV
df = pd.read_csv("data/medium_articles.csv")
df.columns = df.columns.str.lower().str.strip()

# Rename 'text' to 'content'
if 'text' in df.columns:
    df.rename(columns={'text': 'content'}, inplace=True)

# Drop missing rows
df = df.dropna(subset=['title', 'content'])

# Save as Parquet
df.to_parquet("data/blogs.parquet")

print(f"✅ Converted to Parquet. Rows: {df.shape[0]}")
