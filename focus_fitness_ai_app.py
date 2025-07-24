
import streamlit as st
import openai
import time

# Page config
st.set_page_config(page_title="Lauren's Virtual Coach", layout="wide")

# OpenAI client
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🏋️ Lauren’s Virtual Fitness Coach")

# Updated system prompt
system_prompt = """
You are Lauren’s Avatar, representing an experienced, no-nonsense fitness coach.

Before you answer any question, ask yourself: "What would Lauren say?" Use these references:

1. **Lauren’s CV** – she’s highly experienced in rehab, older adults, progressive strength, and sustainable fitness.
2. **Lauren’s Avatar brief** – her coaching voice is warm but direct, and she avoids fluff or sugar-coating.
   - If someone is injured, always ask about the nature, onset, and diagnosis before advising.
   - If someone wants to lose weight, suggest the calorie & macro calculator (only once), then advise based on Lauren’s belief in strength training, NEAT, and consistency.
   - If someone says they’re tired, Lauren would distinguish between excuses and genuine fatigue. Be firm, realistic, and supportive.

Only if Lauren’s coaching background and character offer no guidance may you consult general GPT knowledge.

Avoid vague responses like “consult a professional” or generic advice. You are the coach now.
"""

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
if "macro_tip_given" not in st.session_state:
    st.session_state.macro_tip_given = False

# Sidebar: Calorie Calculator
st.sidebar.title("🔢 Calorie & Macro Calculator")

with st.sidebar:
    sex = st.selectbox("Sex", ["Female", "Male"])
    age = st.number_input("Age", 18, 99, 40)
    height = st.number_input("Height (cm)", 140, 220, 167)
    weight = st.number_input("Current Weight (kg)", 40.0, 200.0, 64.0)
    goal_weight = st.number_input("Goal Weight (kg)", 40.0, 200.0, 59.0)
    activity = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
    timeframe = st.slider("Goal Timeframe (weeks)", 4, 52, 16)
    if st.button("Calculate"):
        bmr = 10 * weight + 6.25 * height - 5 * age + (5 if sex == 'Male' else -161)
        activity_multipliers = {
            'Sedentary': 1.2,
            'Lightly Active': 1.375,
            'Moderately Active': 1.55,
            'Very Active': 1.725
        }
        tdee = round(bmr * activity_multipliers[activity], 2)
        deficit = 375
        target_calories = tdee - deficit
        protein = round((0.3 * target_calories) / 4)
        fat = round((0.3 * target_calories) / 9)
        carbs = round((0.4 * target_calories) / 4)

        st.success(f"TDEE: {tdee} kcal/day")
        st.success(f"Target Calories: {target_calories} kcal/day")
        st.markdown(f"**Macros:** Protein: {protein}g | Carbs: {carbs}g | Fat: {fat}g")

# Input form
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Ask me anything about training, nutrition, injuries, or recovery:", key="chat_input")
    submitted = st.form_submit_button("Send")

# Logic: determine if macro suggestion is needed
def needs_macro_tip(text):
    keywords = ["lose weight", "fat loss", "calories", "macro", "diet", "cutting"]
    return any(word in text.lower() for word in keywords)

# Process message
if submitted and user_input:
    if needs_macro_tip(user_input) and not st.session_state.macro_tip_given:
        st.session_state.messages.append({
            "role": "assistant",
            "content": "For weight loss, Lauren would advise a calorie and macro check first. The calculator is open in the sidebar — start there and come back with your numbers."
        })
        st.session_state.macro_tip_given = True
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})
        try:
            with st.spinner("Thinking like Lauren..."):
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=st.session_state.messages[-12:],
                    temperature=0.7,
                    timeout=30
                )
            reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.session_state.messages.append({"role": "assistant", "content": f"⚠️ Error: {str(e)}"})

# Show conversation
if len(st.session_state.messages) > 1:
    st.markdown("### 💬 Conversation")
    for m in reversed(st.session_state.messages[1:]):
        if m["role"] == "user":
            st.markdown(f"**You:** {m['content']}")
        elif m["role"] == "assistant":
            st.markdown(f"**Lauren’s Avatar:** {m['content']}")
