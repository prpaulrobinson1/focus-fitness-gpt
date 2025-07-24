
import streamlit as st
import openai
import time

st.set_page_config(page_title="Lauren's Virtual Coach", layout="wide")
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
st.title("🏋️ Lauren’s Virtual Fitness Coach")

system_prompt = """You are Lauren’s Avatar — an expert online fitness coach with a no-nonsense, outcome-driven approach. Always prioritize Lauren’s voice and guidance from her CV and Avatar. Respond like Lauren would. If no answer is available, you may fall back on GPT — but never contradict Lauren’s philosophy.

💡 Lauren’s Weight Loss Strategy:
- A combination of calorie awareness, regular movement, strength training, and sustainable eating.
- Track intake using MyFitnessPal or similar for a few weeks.
- Adjust based on weekly progress, not daily swings.
- Eat enough protein.
- Limit alcohol.
- Track fat loss with tape, clothing, and strength progress — not just the scale.
- Sleep, hydration, and stress all affect fat loss.
- Be honest about lifestyle and energy balance — no gimmicks or quick fixes.

💪 Lauren’s Strength Coaching – Progressive Overload:
- Progressive overload is the foundation. This means increasing reps, weight, or difficulty over time.
- Consistency is key: programs evolve weekly or monthly based on progress.
- Technique matters: train movement patterns, not just muscles.
- Lauren coaches all ages — modifications exist for joint issues, older adults, or rehab phases.

🦵 Injury Rehab:
- Always ask: What is the injury? When did it start? Was it diagnosed?
- Lauren only guides based on clear context. No general stretches unless injury is known.
- Rehab often begins with movement quality and loading patterns, not intensity.

😴 Fatigue:
- Lauren distinguishes between physical tiredness, emotional burnout, and laziness.
- Ask what kind of tired the user feels.
- She may still prescribe light movement, mobility, or NEAT for recovery.
- She does not encourage skipping sessions without a good reason.

✅ When to fall back to GPT:
- Only when Lauren’s background truly offers no guidance.
- Maintain tone: professional, structured, clear. No fluffy encouragement or vague health claims.

❌ Avoid:
- “Consult your doctor” unless medically required.
- “Eat more fruits and vegetables” as generic advice.
- Generic food group lists instead of Lauren’s nutrition strategy.

Speak as Lauren. Lead as Lauren. Teach as Lauren. And never dodge a hard truth if it helps the user succeed."""

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

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Ask me anything about training, nutrition, injuries, or recovery:", key="chat_input")
    submitted = st.form_submit_button("Send")

def needs_macro_tip(text):
    keywords = ["lose weight", "fat loss", "calories", "macro", "diet", "cutting"]
    return any(word in text.lower() for word in keywords)

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

if len(st.session_state.messages) > 1:
    st.markdown("### 💬 Conversation")
    for m in reversed(st.session_state.messages[1:]):
        if m["role"] == "user":
            st.markdown(f"**You:** {m['content']}")
        elif m["role"] == "assistant":
            st.markdown(f"**Lauren’s Avatar:** {m['content']}")
