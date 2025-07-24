
import streamlit as st

st.set_page_config(page_title="Focus Fitness AI", layout="centered")

# Title
st.title("🏋️ Focus Fitness AI Study Assistant")
st.markdown("""
Welcome to your interactive study tool! Use this app to revise key topics and receive guidance aligned with Lauren Yates' coaching philosophy.

Use the dropdown menu below to choose a topic.
""")

# Menu
topic = st.selectbox("📚 Select a topic", [
    "Anatomy & Physiology",
    "Exercise Technique & Safety",
    "Client Consultations",
    "Training Program Design",
    "Calorie & Macro Calculator",
    "Lauren’s Coaching Style",
    "About"
])

# Content
if topic == "Anatomy & Physiology":
    st.subheader("🧠 Anatomy & Physiology")
    st.markdown("""
- Identify types of bones and their functions
- Understand the muscular, skeletal, and nervous systems
- Cardiovascular and respiratory basics
- Energy systems and their role in exercise
""")

elif topic == "Exercise Technique & Safety":
    st.subheader("✅ Exercise Technique & Safety")
    st.markdown("""
- Correct posture and form for key lifts
- Spotting techniques and safety protocols
- Training modifications for injuries or special populations
""")

elif topic == "Client Consultations":
    st.subheader("🗣️ Client Consultations & Behaviour Change")
    st.markdown("""
- Pre-screening (PAR-Q, health status)
- SMART goals and habit formation
- Motivational interviewing
- Risk stratification and professional referrals
""")

elif topic == "Training Program Design":
    st.subheader("📋 Program Design")
    st.markdown("""
- FITT and progressive overload
- Periodisation for different goals
- Customising for busy professionals and parents
- Using spreadsheets and data tracking for long-term success
""")

elif topic == "Calorie & Macro Calculator":
    st.subheader("🥗 Calorie & Macro Calculator")
    st.markdown("""
Lauren supports sustainable weight loss through:
- Calorie deficit (300–500 kcal/day)
- High-protein diet (1.6–2.2g/kg BW)
- Macro balance: Protein ~30–40%, Carbs ~30–40%, Fats ~20–30%
- Portion control or optional food tracking

Includes NEAT tracking, example meal plans, and long-term dietary strategies.
""")

elif topic == "Lauren’s Coaching Style":
    st.subheader("💡 Lauren’s Coaching Approach")
    st.markdown("""
- Tailored online coaching for professionals, parents, and all ages
- Focus on consistency, accountability, and realistic progress
- Expertise in injury rehab, post-surgery recovery, and special populations
- Emphasis on sustainable training habits, sleep, stress management, and progressive overload
- Weekly check-ins and optional tracking sheets
""")

elif topic == "About":
    st.subheader("ℹ️ About Focus Fitness AI")
    st.markdown("""
This assistant is designed to support learners and clients of Lauren Yates.

It incorporates Lauren’s strengths in:
- Post-rehab programming
- Online fitness coaching
- Weight loss and body recomposition
- Holistic training with a long-term mindset

Based on Lauren's Avatar, CV, and client strategies — not ActiveIQ manuals.
""")

# Footer
st.markdown("---")
st.markdown("🧠 Powered by Focus Fitness • [Get in touch](mailto:support@focusfitness.co.uk)")
