
import streamlit as st

st.set_page_config(page_title="Focus Fitness AI", layout="centered")

# Title
st.title("🏋️ Focus Fitness AI Study Assistant")
st.markdown("""
Welcome to your interactive study tool! Use this app to revise key topics for your Level 2 and Level 3 qualifications.

Use the dropdown menu below to choose a topic.
""")

# Menu
topic = st.selectbox("📚 Select a study topic", [
    "Anatomy & Physiology",
    "Exercise Technique & Safety",
    "Client Consultations",
    "Training Program Design",
    "About"
])

# Content
if topic == "Anatomy & Physiology":
    st.subheader("🧠 Anatomy & Physiology")
    st.markdown("""
- Identify long, short, flat, irregular, and sesamoid bones  
- Describe the skeletal and muscular systems  
- Explain the nervous, respiratory, and cardiovascular systems  
- Understand energy systems (ATP-PC, glycolytic, aerobic)  
""")

elif topic == "Exercise Technique & Safety":
    st.subheader("✅ Exercise Technique & Safety")
    st.markdown("""
- Five points of posture for lifting  
- Safety cues for major compound movements  
- Spotting protocols and gym etiquette  
- Contraindications in special populations  
""")

elif topic == "Client Consultations":
    st.subheader("🗣️ Client Consultations & Behaviour Change")
    st.markdown("""
- Pre-screening protocols (PAR-Q, health checks)  
- SMART goals and motivational interviewing  
- Behaviour change models (e.g., TTM)  
- Risk stratification and referral guidance  
""")

elif topic == "Training Program Design":
    st.subheader("📋 Program Design")
    st.markdown("""
- FITT principles and progressive overload  
- Training adaptations and periodisation  
- Modifications for special populations  
- Designing for individual and group clients  
""")

elif topic == "About":
    st.subheader("ℹ️ About Focus Fitness AI")
    st.markdown("""
This tool supports learners studying:

- Level 2 Certificate in Gym Instructing  
- Level 3 Extended Diploma in Personal Training  

Created to enhance learning using AI and interactive revision.
""")

# Footer
st.markdown("---")
st.markdown("🧠 Powered by Focus Fitness • [Get in touch](mailto:support@focusfitness.co.uk)")
