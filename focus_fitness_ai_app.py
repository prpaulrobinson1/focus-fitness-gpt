
import streamlit as st
import openai

# Page config
st.set_page_config(page_title="Lauren's Virtual Coach", layout="centered")

# Use capitalized key to match existing Streamlit secret
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("🏋️ Lauren’s Virtual Fitness Coach")

# Session history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Lauren's Avatar, a professional online fitness coach who specializes in injury rehab, strength training, nutrition, and sustainable fat loss for all ages. Always ask follow-up questions if the user mentions an injury. Gently offer the calorie calculator if they ask about weight loss. Use a warm but no-nonsense tone, just like Lauren would."}
    ]

# Chat input
user_input = st.text_input("Ask me anything about training, nutrition, injuries, or recovery:")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        with st.spinner("Thinking like Lauren..."):
            completion = openai.ChatCompletion.create(
                model="gpt-4",
                messages=st.session_state.messages,
                temperature=0.7
            )
        reply = completion.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})

    except Exception as e:
        st.error(f"Error: {e}")
        st.stop()

# Display chat
if len(st.session_state.messages) > 1:
    st.markdown("### 💬 Conversation")
    for m in st.session_state.messages[1:]:
        if m["role"] == "user":
            st.markdown(f"**You:** {m['content']}")
        elif m["role"] == "assistant":
            st.markdown(f"**Lauren’s Avatar:** {m['content']}")
