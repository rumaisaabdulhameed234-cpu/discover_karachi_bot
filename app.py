import streamlit as st
from groq import Groq
import random

st.set_page_config(
    page_title="Discover Karachi",
    page_icon=None,
    layout="centered"
)

# Load CSS from external file
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

# Floating background decorations
st.markdown("""
    <div class="bg-decorations">
        <span style="top:5%; left:3%; animation-delay:0s;">🍓</span>
        <span style="top:12%; left:90%; animation-delay:1s;">💚</span>
        <span style="top:25%; left:8%; animation-delay:2s;">💚</span>
        <span style="top:20%; left:75%; animation-delay:0.5s;">🍓</span>
        <span style="top:40%; left:95%; animation-delay:1.5s;">🍓</span>
        <span style="top:50%; left:2%; animation-delay:3s;">💚</span>
        <span style="top:60%; left:85%; animation-delay:2.5s;">💚</span>
        <span style="top:70%; left:10%; animation-delay:1s;">🍓</span>
        <span style="top:80%; left:92%; animation-delay:0.5s;">🍓</span>
    </div>
""", unsafe_allow_html=True)

# App Navigation Sidebar
with st.sidebar:
    st.markdown("<h2 style='color: #b5476b; font-family: Playfair Display; font-style: italic; margin-top:10px;'>🌸 Discover Menu</h2>", unsafe_allow_html=True)
    page = st.radio(
        "Explore view:",
        ["💬 Live Chatbot", "✨ Trending Spots", "📌 About the Project"]
    )

system_prompt = """
You are Discover Karachi, a warm and friendly chatbot that ONLY answers questions 
about restaurants, cafes, food spots, and places to visit in Karachi, Pakistan.

Always be warm, friendly and conversational. Give specific place names, areas and price ranges when possible. Use plenty of cute food/cafe emojis.

If asked anything NOT about Karachi food or places, say:
"I only know about food and places in Karachi! Ask me about cafes, restaurants or spots to visit."
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- VIEW 1: MAIN CHATBOT ---
if page == "💬 Live Chatbot":
    st.markdown("""
        <div class="main-header">
            <div class="main-title">Discover Karachi</div>
            <div class="main-subtitle">your personal guide to cafes, restaurants & places in Karachi</div>
        </div>
    """, unsafe_allow_html=True)

    # Fixed height scrollable window container for dynamic app look
    chat_container = st.container(height=420, border=False)

    with chat_container:
        if not st.session_state.messages:
            st.markdown(f"""
                <div class="bot-polaroid">
                    <div class="polaroid-card tilt-left">
                        Hello! I'm Discover Karachi, your go-to guide for all the best food spots and places to visit in Karachi. What kind of cuisine are you craving today? Are you looking for a cozy cafe in Clifton, a delicious desi meal in Gulshan, or maybe some mouth-watering BBQ in DHA? Let me know, and I'd be happy to help!
                        <div class="polaroid-label">— discover karachi</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                    <div class="user-bubble">
                        <div class="user-bubble-inner">{message["content"]}</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                tilt = "tilt-left" if len(message["content"]) % 2 == 0 else "tilt-right"
                st.markdown(f"""
                    <div class="bot-polaroid">
                        <div class="polaroid-card {tilt}">
                            {message["content"]}
                            <div class="polaroid-label">— discover karachi</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

    if prompt := st.chat_input("ask me about cafes and places in karachi..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

# --- VIEW 2: TRENDING SPOTS GRID ---
elif page == "✨ Trending Spots":
    st.markdown("""
        <div class="main-header">
            <div class="main-title">Trending Hotspots</div>
            <div class="main-subtitle">Curated aesthetic favorites in K-town right now</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="polaroid-card" style="max-width:100%; margin-bottom:15px;">
            <h3 style="color:#b5476b; margin-top:0; font-size:1.1rem;">☕ The Coffee Pot (DHA)</h3>
            <p style="font-size:0.88rem; line-height:1.4; margin-bottom:5px;">Stunning visual lighting, cozy corners perfect for assignments, and phenomenal fresh pastries.</p>
            <span style="font-size:0.75rem; color:#5a9e7e; font-weight:bold;">📍 DHA Phase 6</span>
        </div>
        <div class="polaroid-card" style="max-width:100%; margin-bottom:15px;">
            <h3 style="color:#b5476b; margin-top:0; font-size:1.1rem;">🥐 Cafe Aylanto (Clifton)</h3>
            <p style="font-size:0.88rem; line-height:1.4; margin-bottom:5px;">High-end Mediterranean layout with an absolutely stunning courtyard. The ideal ambient dinner option.</p>
            <span style="font-size:0.75rem; color:#5a9e7e; font-weight:bold;">📍 Clifton Block 4</span>
        </div>
    """, unsafe_allow_html=True)

# --- VIEW 3: ABOUT VIEW ---
elif page == "📌 About the Project":
    st.markdown("""
        <div class="main-header">
            <div class="main-title">About the Project</div>
        </div>
        <div class="polaroid-card" style="max-width:100%; margin: 0 auto; text-align:center;">
            <p style="font-size:1rem; line-height:1.5; font-style:italic;">
                "Discover Karachi" is an AI-powered interface curated to simplify finding premium dining spots across the city. Driven by advanced LLM endpoints and styled with personal aesthetic intent.
            </p>
            <div class="polaroid-label" style="font-size:0.9rem; margin-top:15px;">🍓 Built for UX Marketing Assignment 🍓</div>
        </div>
    """, unsafe_allow_html=True)

if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.spinner("finding the best spots for you..."):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages,
            max_tokens=500
        )
        bot_reply = response.choices.message.content
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        st.rerun()
