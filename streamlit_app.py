# streamlit_app.py

import streamlit as st
from scripts.load_data import load_blog_data
from scripts.recommender import recommend_top_blogs
from scripts.kafka_producer import send_summary_request
from scripts.elastic_utils import search_similar_blogs
from scripts.auth import login_ui, log_user_action
import redis

st.set_page_config(page_title="🧠 InsightSwitch", layout="wide")
st.title("🧠 InsightSwitch — Smart Blog & Media Explorer")

# Redis connection
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# --- Authentication ---
authenticated, user_email = login_ui()
if not authenticated:
    st.warning("🔐 Please login to use the app.")
    st.stop()

# --- Content Type Toggle ---
content_type = st.radio("Select content type:", ["📝 Blogs", "🖼️ Photos"])

if content_type == "📝 Blogs":
    df = load_blog_data()
    st.success(f"✅ Loaded {len(df)} blogs")

    query = st.text_input("🔍 Search blogs by keyword:", "")

    if query:
        log_user_action(user_email, "search", query)
        results = recommend_top_blogs(query, top_n=10)

        st.markdown(f"**{len(results)} result(s) found for '{query}'**")
        for row in results:
            title = row.get("title", "Untitled").strip()
            content = row.get("content", "").strip()
            url = row.get("url", "")
            tags = row.get("tags", [])

            if not title or not content:
                continue

            st.subheader(f"📰 {title}")
            st.caption(f"🏷️ Tags: {tags}")
            if url:
                st.markdown(f"[🔗 Read Full Blog]({url})")

            redis_key = title.lower().replace(" ", "_")
            summary = redis_client.get(redis_key)

            if summary:
                st.success("🧠 Summary:")
                st.markdown(summary.decode("utf-8"))
            else:
                if st.session_state.get(f"summary_requested_{redis_key}"):
                    st.info("⏳ Summary is being generated... Please check back in a moment.")
                else:
                    if st.button(f"🧠 Summarize this blog", key=title):
                        send_summary_request(title, content)
                        st.session_state[f"summary_requested_{redis_key}"] = True
                        st.success("✅ Request sent to summarizer. Please wait a few seconds then refresh.")
                        log_user_action(user_email, "summarize_request", title)

            # Elastic-based recommendations
            if st.button(f"🧭 Recommend more like this", key=f"rec_{title}"):
                st.info("🔎 Finding similar blogs...")
                recs = search_similar_blogs(content)
                st.subheader("🔁 Similar Blogs")
                for rec in recs:
                    st.markdown(f"**{rec['title']}**")
                    st.caption(f"🏷️ Tags: {rec.get('tags', [])}")
                    if rec.get('url'):
                        st.markdown(f"[🔗 Read Full Blog]({rec['url']})")
                    st.markdown("---")

            st.markdown("---")

else:
    st.info("📷 Photo search will be added soon. Stay tuned!")
