import streamlit as st
import feedparser

st.set_page_config(
    page_title="投資觀念重構儀表板",
    page_icon="💡",
    layout="wide"
)

st.markdown("""
    <style>
    .post-card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #e6e9ef;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
    }
    .post-title { color: #1E88E5; font-size: 1.35rem; font-weight: 600; }
    .post-title:hover { color: #1565C0; }
    .post-meta { color: #6c757d; font-size: 0.92rem; margin-bottom: 14px; }
    </style>
    """, unsafe_allow_html=True)

st.title("💡 投資觀念重構站")
st.caption("📡 RSS 即時抓取 KOL 最新觀點")

RSS_FEEDS = {
    "臉書測試粉專": "https://rss.app/feeds/3uU9UA2r2SUPFJwA.xml",
}

with st.sidebar:
    st.header("⚙️ 控制面板")
    selected_source = st.selectbox("選擇資料來源", list(RSS_FEEDS.keys()))
    
    if st.button("🔄 重新抓取最新文章", type="primary"):
        st.cache_data.clear()
        st.rerun()

# 主內容
feed = feedparser.parse(RSS_FEEDS[selected_source])

if not feed.entries:
    st.error("無法抓取文章")
else:
    st.success(f"✅ 抓取到 {len(feed.entries)} 篇文章")
    
    for i, entry in enumerate(feed.entries):
        published = entry.get("published", "未知時間")
        
        st.markdown(f"""
            <div class="post-card">
                <div class="post-meta">🕒 {published}</div>
                <a class="post-title" href="{entry.link}" target="_blank">{entry.title}</a>
                <div style="margin-top: 16px; line-height: 1.7;">
                    {entry.get('summary', '無摘要')[:400]}...
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1.2, 5])
        with col1:
            if st.button("📌 收藏", key=f"save_{i}"):
                st.success("已加入收藏！")
        with col2:
            st.markdown(f"[🔗 閱讀原文]({entry.link})")
        
        st.divider()
