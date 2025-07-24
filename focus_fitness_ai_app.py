
import streamlit as st

def calculate_tdee(weight, height, age, sex, activity_level):
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

    tdee = bmr * activity_multipliers[activity_level]
    return round(tdee, 2)

def calculate_macros(calories):
    protein = round((0.3 * calories) / 4)
    fat = round((0.3 * calories) / 9)
    carbs = round((0.4 * calories) / 4)
    return protein, fat, carbs

st.set_page_config(page_title="Lauren's GPT Assistant", layout="centered")

st.title("👋 Welcome Lauren’s GPT Assistant!")
st.markdown("Hi, this is Lauren’s Avatar, I am here to help. Who am I speaking to today?")

menu = st.selectbox("What would you like help with?", [
    "Ask a Fitness Question",
    "Report an Injury",
    "Get Nutrition Guidance",
    "Live Calorie & Macro Calculator",
    "Learn About Lauren’s Coaching",
    "Exit"
])

if menu == "Live Calorie & Macro Calculator":
    st.subheader("🔢 Calorie & Macro Calculator")

    sex = st.selectbox("Sex", ["Female", "Male"])
    age = st.number_input("Age", 18, 99, 40)
    height = st.number_input("Height (cm)", 140, 220, 167)
    weight = st.number_input("Current Weight (kg)", 40.0, 200.0, 64.0)
    goal_weight = st.number_input("Goal Weight (kg)", 40.0, 200.0, 59.0)
    activity = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
    timeframe = st.slider("Goal Timeframe (weeks)", 4, 52, 16)

    if st.button("Calculate My Targets"):
        tdee = calculate_tdee(weight, height, age, sex, activity)
        deficit = 375
        target_calories = tdee - deficit
        protein, fat, carbs = calculate_macros(target_calories)

        st.success(f"Estimated TDEE: {tdee} kcal/day")
        st.success(f"Calorie Target for Weight Loss: {target_calories} kcal/day")
        st.markdown(f"**Daily Macros:** Protein: {protein}g, Carbs: {carbs}g, Fat: {fat}g")

if menu == "Get Nutrition Guidance":
    st.subheader("🥗 Nutrition Guidance")
    goal = st.radio("What's your main goal?", ["Lose weight", "Build muscle", "Improve energy", "Not sure yet"])
    tracking = st.checkbox("Would you like to use the calorie/macro calculator?")
    if goal == "Lose weight":
        st.markdown("Lauren focuses on realistic fat loss through strength training, NEAT, and flexible eating — not rigid calorie tracking.")
        if tracking:
            st.markdown("You can use the **Live Calorie Calculator** above to get tailored calorie and macro guidance.")
    else:
        st.markdown("Lauren encourages a high-protein foundation, adequate carbs for training, and healthy fats — tailored to lifestyle and preferences.")

elif menu == "Ask a Fitness Question":
    st.subheader("💬 Ask a Fitness Question")
    question = st.text_input("Type your question here:")
    if question:
        st.write("Thanks! Lauren would say that every good answer starts with understanding your goals. Here's a starting point:")
        st.markdown("- If your question involves weight loss, training plans, or plateaus, Lauren may gently suggest a calorie and macro check.")
        st.markdown("- For strength or rehab, Lauren emphasizes progressive overload and tailored movement.")

elif menu == "Report an Injury":
    st.subheader("🩹 Injury Reporting")
    area = st.selectbox("Which area is injured?", ["Knee", "Shoulder", "Back", "Hip", "Other"])
    details = st.text_area("Please describe the issue in detail (when it began, what makes it worse, any medical advice received, etc.)")
    if details:
        st.markdown("Thanks for explaining. Lauren would ask:")
        st.markdown("- Has it been diagnosed by a medical professional?")
        st.markdown("- Are you currently able to bear weight or move the area?")
        st.markdown("- Have you had this injury before?")

elif menu == "Learn About Lauren’s Coaching":
    st.subheader("💡 Lauren’s Coaching Philosophy")
    st.markdown("""
Lauren helps busy professionals, parents, and older adults build sustainable fitness habits. Her focus is on:
- Tailored strength training with progressive overload
- Adapting around injuries or medical history
- Weekly check-ins and structured tracking (spreadsheet-based)
- Combining movement, mindset, recovery, and nutrition without pressure

She avoids extremes and encourages long-term health over quick fixes. From post-surgery recovery to elite professionals — Lauren’s seen it all.
""")

elif menu == "Exit":
    st.write("Thanks for visiting. Lauren and I are here whenever you're ready!")
