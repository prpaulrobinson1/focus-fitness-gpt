
import streamlit as st

# Set page config
st.set_page_config(page_title="Lauren's GPT Assistant", layout="centered")

# Session state for name and chat history
if 'name' not in st.session_state:
    st.session_state.name = ""
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Title and name input
st.title("👋 Welcome Lauren’s GPT Assistant!")
if not st.session_state.name:
    st.session_state.name = st.text_input("Hi, this is Lauren’s Avatar, I am here to help. Who am I speaking to today?")
    st.stop()

st.markdown(f"Nice to see you, **{st.session_state.name}**. How can I help you today?")

# Question input
question = st.text_input("Ask me anything about training, injury, nutrition, or Lauren’s approach:")

# Process and respond
if question:
    response = ""

    q = question.lower()
    if "squat" in q and "muscle" in q:
        response = (
            "A squat primarily works the quadriceps, gluteus maximus, and hamstrings. "
            "It also engages the erector spinae and core for stability. "
            "Lauren would remind you to focus on proper knee alignment and neutral spine during execution."
        )
    elif "knee injury" in q or ("injury" in q and "knee" in q):
        response = (
            "Before suggesting exercises, Lauren would want to know more. "
            "Is it a ligament, cartilage, tendon, or joint issue? When did it start? Has it been diagnosed? "
            "Once we know that, we can consider safe movement strategies."
        )
    elif "lose weight" in q or "weight loss" in q:
        response = (
            "Lauren supports sustainable fat loss through strength training, NEAT, and high-protein eating. "
            "Would you like to estimate your calorie and macro needs?"
        )
    elif "protein" in q:
        response = (
            "Lauren typically recommends 1.6–2.2g of protein per kg of body weight for most clients. "
            "This supports satiety, lean mass retention, and recovery during fat loss or strength training."
        )
    elif "hello" in q or "hi" in q:
        response = f"Hi {st.session_state.name}, how can I support your fitness journey today?"
    else:
        response = (
            "That’s a great question. Lauren would tailor the answer depending on your goals, "
            "injury history, and lifestyle. Can you tell me a bit more so we can guide you properly?"
        )

    st.session_state.chat_history.append((question, response))

# Display chat history
if st.session_state.chat_history:
    st.markdown("### 💬 Conversation")
    for i, (q, r) in enumerate(reversed(st.session_state.chat_history[-5:]), 1):
        st.markdown(f"**You:** {q}")
        st.markdown(f"**Lauren’s Avatar:** {r}")
