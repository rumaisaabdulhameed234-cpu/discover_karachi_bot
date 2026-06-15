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
        <span style="top:88%; left:20%; animation-delay:2s;">💚</span>
        <span style="top:35%; left:50%; animation-delay:3.5s;">🍓</span>
        <span style="top:55%; left:60%; animation-delay:1.8s;">💚</span>
    </div>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="main-header">
        <div class="main-title">Discover Karachi</div>
        <div class="main-subtitle">your personal guide to cafes, restaurants & places in Karachi</div>
    </div>
""", unsafe_allow_html=True)

# Fetch the API key securely from Streamlit's environment secrets
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# System prompt
system_prompt = """
You are Discover Karachi, a warm and friendly chatbot that ONLY answers questions 
about restaurants, cafes, food spots, and places to visit in Karachi, Pakistan.

Always be warm, friendly and conversational. Give specific place names, areas and price ranges when possible.

If asked anything NOT about Karachi food or places, say:
"I only know about food and places in Karachi! Ask me about cafes, restaurants or spots to visit."
"""

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display welcome message if chat is empty
if not st.session_state.messages:
    st.markdown(f"""
        <div class="bot-polaroid">
            <div class="polaroid-card tilt-left">
                Hello! I'm Discover Karachi, your go-to guide for all the best food spots and places to visit in Karachi. What kind of cuisine are you craving today? Are you looking for a cozy cafe in Clifton, a delicious desi meal in Gulshan, or maybe some mouth-watering BBQ in DHA? Let me know, and I'd be happy to help!
                <div class="polaroid-label">— discover karachi</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
            <div class="user-bubble">
                <div class="user-bubble-inner">{message["content"]}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        tilt = "tilt-left" if random.random() > 0.5 else "tilt-right"
        st.markdown(f"""
            <div class="bot-polaroid">
                <div class="polaroid-card {tilt}">
                    {message["content"]}
                    <div class="polaroid-label">— discover karachi</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("ask me about cafes and places in karachi..."):

    st.markdown(f"""
        <div class="user-bubble">
            <div class="user-bubble-inner">{prompt}</div>
        </div>
    """, unsafe_allow_html=True)

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("finding the best spots for you..."):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt}
            ] + st.session_state.messages,
            max_tokens=500
        )
        bot_reply = response.choices.message.content

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    st.rerun()
        
