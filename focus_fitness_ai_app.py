
import streamlit as st

# Configure page
st.set_page_config(page_title="Lauren's GPT Assistant", layout="centered")

# Session state
if "name" not in st.session_state:
    st.session_state.name = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "show_calculator" not in st.session_state:
    st.session_state.show_calculator = False
if "last_topic" not in st.session_state:
    st.session_state.last_topic = ""

# Page Title
st.title("🤖 Lauren’s Avatar – Your Fitness Assistant")

# Greet and collect name
if not st.session_state.name:
    name_input = st.text_input("Hi, this is Lauren’s Avatar. Who am I speaking to today?", key="name_input")
    if name_input:
        st.session_state.name = name_input.strip()
        st.success(f"Welcome {st.session_state.name}! You can now start chatting below.")

# Chat interface (only shows once name is set)
if st.session_state.name:
    st.markdown(f"👋 Hi **{st.session_state.name}**, how can I support your training, nutrition, or recovery today?")

    with st.form("chat_input_form"):
        user_input = st.text_input("Your message:", key="input")
        send = st.form_submit_button("Send")

    if send and user_input:
        user_message = user_input.strip().lower()
        response = ""

        if "squat" in user_message and "muscle" in user_message:
            response = (
                "Squats work your quads, glutes, hamstrings, and core. "
                "Lauren would remind you to keep your knees tracking over your toes and maintain a neutral spine."
            )
            st.session_state.last_topic = "squat"

        elif any(word in user_message for word in ["meniscus", "knee injury", "knee problem", "knee pain", "knee"]):
            response = (
                "Lauren would want to know: Is this a tear, inflammation, or undiagnosed? "
                "When did the pain begin? Are you experiencing clicking, swelling, or locking? "
                "Once you clarify, we can explore movement strategies or modifications."
            )
            st.session_state.last_topic = "knee"

        elif "tear" in user_message and st.session_state.last_topic == "knee":
            response = (
                "That helps — if it’s a meniscus or ligament tear, Lauren would focus on restoring range of motion, "
                "avoiding twisting motions, and supporting joint stability. "
                "Has a physio given you exercises or are you waiting for imaging results?"
            )

        elif any(word in user_message for word in ["protein", "macros", "calories", "calculate", "intake"]):
            response = (
                "Sure! Let's estimate your daily calorie and macro targets. Please scroll down and fill in the calculator."
            )
            st.session_state.show_calculator = True
            st.session_state.last_topic = "nutrition"

        elif any(word in user_message for word in ["lose weight", "fat loss"]):
            response = (
                "For fat loss, Lauren focuses on strength training, NEAT (daily movement), and high-protein intake. "
                "Would you like help setting your intake targets?"
            )
            st.session_state.last_topic = "fat loss"

        elif "injury" in user_message:
            response = (
                "Can you tell me more about the injury? Lauren would want to know when it started, "
                "what aggravates it, and if a diagnosis was given before advising next steps."
            )
            st.session_state.last_topic = "injury"

        elif "hello" in user_message or "hi" in user_message:
            response = f"Hi {st.session_state.name}, I’m here to support your fitness journey. Ask me anything!"
            st.session_state.last_topic = "greeting"

        else:
            if st.session_state.last_topic == "knee" and "pain" in user_message:
                response = (
                    "Understood. With ongoing knee pain, Lauren would recommend temporarily avoiding deep flexion movements, "
                    "and might suggest quad activation work, glute bridges, or cycling if pain-free. Would you like movement suggestions?"
                )
            else:
                response = (
                    f"Thanks for your message, {st.session_state.name}. "
                    "Tell me more about your goal or situation so I can tailor Lauren’s advice for you."
                )

        st.session_state.chat_history.append(("You", user_input.strip()))
        st.session_state.chat_history.append(("Lauren’s Avatar", response))

    # Display chat history
    if st.session_state.chat_history:
        st.markdown("### 🗨️ Conversation History")
        for sender, msg in st.session_state.chat_history[-10:]:
            if sender == "You":
                st.markdown(f"**You:** {msg}")
            else:
                st.markdown(f"**Lauren’s Avatar:** {msg}")

    # Calorie Calculator
    if st.session_state.show_calculator:
        st.markdown("---")
        st.subheader("🔢 Calorie & Macro Calculator")

        sex = st.selectbox("Sex", ["Female", "Male"])
        age = st.number_input("Age", 18, 99, 40)
        height = st.number_input("Height (cm)", 140, 220, 167)
        weight = st.number_input("Current Weight (kg)", 40.0, 200.0, 64.0)
        goal_weight = st.number_input("Goal Weight (kg)", 40.0, 200.0, 59.0)
        activity = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
        timeframe = st.slider("Goal Timeframe (weeks)", 4, 52, 16)

        if st.button("Calculate"):
            if sex == 'Male':
                bmr = 10 * weight + 6.25 * height - 5 * age + 5
            else:
                bmr = 10 * weight + 6.25 * height - 5 * age - 161

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

            st.success(f"Estimated TDEE: {tdee} kcal/day")
            st.success(f"Calorie Target for Weight Loss: {target_calories} kcal/day")
            st.markdown(f"**Daily Macros:** Protein: {protein}g | Carbs: {carbs}g | Fat: {fat}g")
