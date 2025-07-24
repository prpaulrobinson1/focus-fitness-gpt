
import streamlit as st
import openai

# Page config
st.set_page_config(page_title="Lauren's Virtual Coach", layout="centered")

# OpenAI client
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🏋️ Lauren’s Virtual Fitness Coach")

# Enhanced system prompt
system_prompt = """
You are Lauren’s Avatar, a no-nonsense, experienced online fitness coach.

Here are your core principles:
- If someone reports an injury, always ask specific follow-ups before giving any exercise advice (e.g., location, type of injury, diagnosis, onset).
- If someone asks about weight loss, you should gently suggest using the calorie and macro calculator — but only once.
- If someone says they are tired, give a firm yet compassionate response: distinguish between physical fatigue and mental burnout, and recommend movement or recovery strategies with purpose.
- You avoid vague advice. You respond as Lauren would: direct, warm, structured, but never fluffy.
- You do not offer detailed meal plans or medical diagnoses — but you are strong on training structure, movement advice, and long-term consistency.

You know Lauren’s background includes rehab coaching, older adult training, and practical results over quick fixes. Keep tone businesslike, friendly, and firm.
"""

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
if "last_user_input" not in st.session_state:
    st.session_state.last_user_input = ""

# Chat input
user_input = st.text_input("Ask me anything about training, nutrition, injuries, or recovery:", value="", key="chat_input")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.last_user_input = user_input

    try:
        with st.spinner("Thinking like Lauren..."):
            response = client.chat.completions.create(
                model="gpt-4",
                messages=st.session_state.messages,
                temperature=0.7
            )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

    except Exception as e:
        st.error(f"Error: {e}")
        st.stop()

# Display chat (newest at top)
if len(st.session_state.messages) > 1:
    st.markdown("### 💬 Conversation")
    for m in reversed(st.session_state.messages[1:]):  # Skip system message
        if m["role"] == "user":
            st.markdown(f"**You:** {m['content']}")
        elif m["role"] == "assistant":
            st.markdown(f"**Lauren’s Avatar:** {m['content']}")
