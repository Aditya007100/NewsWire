import streamlit as st
import feedparser
import urllib.parse
import re

# 1. App Page Configuration (Website ka Title aur Layout)
st.set_page_config(
    page_title="NewsWire | Live Media Hub", 
    page_icon="📰", 
    layout="wide"
)

# Custom CSS for better look (Dark Theme & Rounded Cards)
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    div.stButton > button:first-child {
        background-color: #ff4b4b;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. News Fetch Karne Ka Function (Smart Image & Video Logic)
def fetch_news(rss_url, limit=15):
    feed = feedparser.parse(rss_url)
    news_items = []
    
    for entry in feed.entries[:limit]:
        # Description se Image nikalne ki koshish (Regex use karke)
        desc = entry.get('description', '')
        img_match = re.search(r'<img[^>]+src="([^">]+)"', desc)
        
        if img_match:
            img_url = img_match.group(1)
        else:
            # Agar news mein image nahi hai, toh default breaking news image
            img_url = "https://images.unsplash.com/photo-1504711434969-e33886168f5c?auto=format&fit=crop&w=800&q=80"
        
        # YouTube Clips ke liye Search Link banana
        yt_query = urllib.parse.quote(entry.title + " latest news")
        yt_link = f"https://www.youtube.com/results?search_query={yt_query}"
        
        news_items.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published,
            "image": img_url,
            "youtube": yt_link
        })
    return news_items

# 3. News ko Sundar Cards mein Display karne ka Function
def display_news(news_list):
    # Har line mein 2 news cards dikhayenge
    cols = st.columns(2)
    for idx, item in enumerate(news_list):
        with cols[idx % 2]:
            st.markdown(f"""
            <div style="background-color: #1e1e1e; color: white; border-radius: 15px; margin-bottom: 25px; border: 1px solid #333; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.5);">
                <img src="{item['image']}" style="width: 100%; height: 230px; object-fit: cover; border-bottom: 2px solid #333;">
                <div style="padding: 20px;">
                    <h3 style="margin-top:0; font-size: 19px; color: #ffffff; line-height: 1.4; font-family: sans-serif;">{item['title']}</h3>
                    <p style="font-size: 12px; color: #999;">📅 {item['published']}</p>
                    <hr style="border: 0.5px solid #444; margin: 15px 0;">
                    <div style="display: flex; gap: 12px;">
                        <a href="{item['link']}" target="_blank" style="flex: 1; text-align: center; background-color: #007bff; color: white; padding: 10px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 14px;">📖 Read Full</a>
                        <a href="{item['youtube']}" target="_blank" style="flex: 1; text-align: center; background-color: #e60000; color: white; padding: 10px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 14px;">📺 Video Clips</a>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- APP INTERFACE START ---

st.title("📰 NewsWire: Live Media Hub")
st.subheader("Taaza Khabrein | Photos | YouTube Video Clips")
st.markdown("---")

# Navigation Tabs
tab1, tab2, tab3 = st.tabs(["🇮🇳 National News", "🌍 Global News", "📍 Select Your State"])

with tab1:
    st.info("India ki top headlines (Live Syncing...)")
    india_url = "https://news.google.com/rss/headlines/section/geo/IN?hl=en-IN&gl=IN&ceid=IN:en"
    display_news(fetch_news(india_url))

with tab2:
    st.info("Duniya bhar ki badi khabrein")
    world_url = "https://news.google.com/rss/headlines/section/topic/WORLD?hl=en-IN&gl=IN&ceid=IN:en"
    display_news(fetch_news(world_url))

with tab3:
    st.subheader("Apne State ki khabrein chuniye")
    # Ranchi (Jharkhand) ke hisab se default list
    state = st.selectbox("State Select Karein:", ["Jharkhand", "Bihar", "Delhi", "Maharashtra", "Uttar Pradesh", "West Bengal", "Rajasthan", "Gujarat", "Punjab"])
    
    if state:
        state_url = f"https://news.google.com/rss/search?q={state}+News&hl=en-IN&gl=IN&ceid=IN:en"
        display_news(fetch_news(state_url))

# Footer Section
st.markdown("---")
st.markdown("<p style='text-align: center; color: #666;'>© 2026 NewsWire Engine | Built with Streamlit & GitHub</p>", unsafe_allow_html=True)
