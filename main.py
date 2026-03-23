import streamlit as st
import feedparser
import urllib.parse
import re

# App ka setup
st.set_page_config(page_title="NewsWire Live", page_icon="📰", layout="centered")

# News fetch karne ka function
def fetch_news(rss_url, limit=15):
    feed = feedparser.parse(rss_url)
    news_items = []
    for entry in feed.entries[:limit]:
        desc = entry.get('description', '')
        # Photo nikalne ki koshish
        img_match = re.search(r'<img[^>]+src="([^">]+)"', desc)
        img_url = img_match.group(1) if img_match else "https://images.unsplash.com/photo-1504711434969-e33886168f5c?auto=format&fit=crop&w=800&q=80"
        
        # YouTube link banana
        yt_query = urllib.parse.quote(entry.title + " news")
        yt_link = f"https://www.youtube.com/results?search_query={yt_query}"
        
        news_items.append({
            "title": entry.title, 
            "link": entry.link, 
            "published": entry.published, 
            "image": img_url, 
            "youtube": yt_link
        })
    return news_items

# News dikhane ka function
def display_news(news_list):
    for item in news_list:
        st.markdown(f"""
        <div style="background-color: #1e1e1e; color: white; border-radius: 12px; margin-bottom: 25px; border: 1px solid #333; overflow: hidden; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
            <img src="{item['image']}" style="width: 100%; height: 200px; object-fit: cover;">
            <div style="padding: 15px;">
                <h3 style="margin-top:0; font-size: 18px; color: #ffffff;">{item['title']}</h3>
                <p style="font-size: 12px; color: #aaaaaa;">🕒 {item['published']}</p>
                <div style="display: flex; gap: 10px; margin-top: 15px;">
                    <a href="{item['link']}" target="_blank" style="background-color: #4da6ff; color: black; padding: 8px 15px; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 13px;">Read Article</a>
                    <a href="{item['youtube']}" target="_blank" style="background-color: #ff0000; color: white; padding: 8px 15px; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 13px;">📺 YouTube</a>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Main App Interface
st.title("📰 NewsWire: Live Updates")
st.markdown("---")

# Tabs for categories
tab1, tab2, tab3 = st.tabs(["🇮🇳 India Top News", "🌍 World News", "📍 State Wise"])

with tab1:
    india_url = "https://news.google.com/rss/headlines/section/geo/IN?hl=en-IN&gl=IN&ceid=IN:en"
    display_news(fetch_news(india_url))

with tab2:
    world_url = "https
