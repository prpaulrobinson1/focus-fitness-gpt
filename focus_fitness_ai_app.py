
import streamlit as st
import openai
import time

# Page config
st.set_page_config(page_title="Lauren's Virtual Coach", layout="centered")

# Set up OpenAI client
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🏋️ Lauren’s Virtual Fitness Coach")

# Lauren's system prompt
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

# Input form
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Ask me anything about training, nutrition, injuries, or recovery:", key="chat_input")
    submitted = st.form_submit_button("Send")

# Process message
if submitted and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        with st.spinner("Thinking like Lauren..."):
            start = time.time()
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages[-12:],  # last 12 plus system
                temperature=0.7,
                timeout=30  # hard timeout
            )
            elapsed = time.time() - start
            if elapsed > 20:
                st.warning("⏳ That took a while — things may be slow at the moment.")

            reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": reply})

    except Exception as e:
        st.session_state.messages.append({"role": "assistant", "content": f"⚠️ Error: {str(e)}"})

# Display conversation
if len(st.session_state.messages) > 1:
    st.markdown("### 💬 Conversation")
    for m in reversed(st.session_state.messages[1:]):  # skip system
        if m["role"] == "user":
            st.markdown(f"**You:** {m['content']}")
        elif m["role"] == "assistant":
            st.markdown(f"**Lauren’s Avatar:** {m['content']}")
