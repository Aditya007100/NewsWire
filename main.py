import streamlit as st
import feedparser
import urllib.parse
import re

# App Configuration
st.set_page_config(page_title="NewsWire Live", page_icon="📰", layout="centered")

# News Fetching Function
def fetch_news(rss_url, limit=15):
    try:
        feed = feedparser.parse(rss_url)
        news_items = []
        for entry in feed.entries[:limit]:
            # Image nikalne ki koshish
            desc = entry.get('description', '')
            img_match = re.search(r'<img[^>]+src="([^">]+)"', desc)
            img_url = img_match.group(1) if img_match else "https://images.unsplash.com/photo-1504711434969-e33886168f5c?auto=format&fit=crop&w=800&q=80"
            
            # Safe Published Date
            pub_date = entry.get('published', 'Live Update')
            
            # YouTube Link
            yt_query = urllib.parse.quote(entry.title + " news")
            yt_link = f"https://www.youtube.com/results?search_query={yt_query}"
            
            news_items.append({
                "title": entry.title,
                "link": entry.link,
                "published": pub_date,
                "image": img_url,
                "youtube": yt_link
            })
        return news_items
    except Exception as e:
        return []

# Design Function
def display_news(news_list):
    if not news_list:
        st.warning("Khabrein load nahi ho pa rahi hain. Kripya thodi der baad try karein.")
        return
    for item in news_list:
        st.markdown(f"""
        <div style="background-color: #1e1e1e; color: white; border-radius: 12px; margin-bottom: 25px; border: 1px solid #333; overflow: hidden; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
            <img src="{item['image']}" style="width: 100%; height: 220px; object-fit: cover;">
            <div style="padding: 15px;">
                <h3 style="margin-top:0; font-size: 18px; line-height: 1.4;">{item['title']}</h3>
                <p style="color: #aaaaaa; font-size: 12px;">🕒 {item['published']}</p>
                <div style="display: flex; gap: 10px; margin-top: 15px;">
                    <a href="{item['link']}" target="_blank" style="background-color: #4da6ff; color: black; padding: 10px 15px; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 13px;">Read Article</a>
                    <a href="{item['youtube']}" target="_blank" style="background-color: #ff0000; color: white; padding: 10px 15px; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 13px;">📺 YouTube Clips</a>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Main App Header
st.title("📰 NewsWire: Live Media Hub")
st.write("### Taaza Khabrein | Photos | YouTube Video Clips")

tab1, tab2, tab3 = st.tabs(["🇮🇳 National News", "🌍 Global News", "📍 Select Your State"])

with tab1:
    st.info("India ki top headlines (Live Syncing...)")
    display_news(fetch_news("https://news.google.com/rss/headlines/section/geo/IN?hl=en-IN&gl=IN&ceid=IN:en"))

with tab2:
    display_news(fetch_news("https://news.google.com/rss/headlines/section/topic/WORLD?hl=en-IN&gl=IN&ceid=IN:en"))

with tab3:
    state = st.selectbox("Apna State Chunein:", ["Jharkhand", "Bihar", "Delhi", "Maharashtra", "UP", "Rajasthan", "West Bengal"])
    if state:
        display_news(fetch_news(f"https://news.google.com/rss/search?q={state}+News&hl=en-IN&gl=IN&ceid=IN:en"))
