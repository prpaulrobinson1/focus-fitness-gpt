
import streamlit as st
import os
from openai import OpenAI
import PyPDF2
from pathlib import Path

# --- CONFIG ---
st.set_page_config(page_title="Focus Fusion GPT Assistant", layout="wide")

# --- LOAD API KEY ---
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- FILE PATHS ---
data_dir = Path("data")
document_files = {
    "Level 2 Manual": data_dir / "Q2CGI MANUAL AIQ005803 EMAIL - Copy.pdf",
    "Level 3 Manual": data_dir / "Q3EXPT MANUAL AIQ005667 EMAIL - Copy.pdf",
    "Lauren Avatar": data_dir / "Lauren Avatar.pdf",
    "Lauren CV": data_dir / "Lauren Yates CV 2025 pdf.pdf",
    "Calorie Macro": data_dir / "Calorie and Macro Calculator.pdf"
}

# --- TEXT EXTRACTION ---
def extract_text_from_pdf(file_path):
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
    except Exception as e:
        return f"[Error reading {file_path.name}: {e}]"

# --- GPT CALL ---
def ask_openai(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are Lauren, a highly experienced personal trainer and rehab coach. Use the manuals provided to answer user questions in a friendly, expert tone."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error contacting OpenAI: {str(e)}"

# --- APP TITLE ---
st.title("🏋️ Welcome to your Focus Fusion GPT assistant!")
st.markdown("Hi, this is Lauren's Avatar, I am here to help. Who am I speaking to today?")

# --- TABS ---
tabs = st.tabs(["Lauren Avatar Advice", "Manual Q&A", "Calorie & Macro Calculator", "About Lauren"])

# --- TAB 1: Lauren Avatar Advice ---
with tabs[0]:
    st.header("🧘 Lauren's Personal Advice")
    question = st.text_area("Ask about injury, rehab, behaviour change, motivation, or lifestyle coaching:")
    if st.button("Get Advice", key="avatar") and question:
        context = extract_text_from_pdf(document_files["Lauren Avatar"]) + "\n" + extract_text_from_pdf(document_files["Lauren CV"])
        prompt = f"Use the following documents to answer the question:\n{context}\n\nQuestion: {question}"
        response = ask_openai(prompt)
        st.markdown(response)

# --- TAB 2: Manual Q&A ---
with tabs[1]:
    st.header("📖 Level 2 & 3 Manual Support")
    manual_q = st.text_input("Ask a technical or exam-style question:")
    if st.button("Search Manuals", key="manual") and manual_q:
        context = extract_text_from_pdf(document_files["Level 2 Manual"]) + "\n" + extract_text_from_pdf(document_files["Level 3 Manual"])
        prompt = f"Based on the L2 and L3 fitness manuals, answer this question clearly:\n{context}\n\nQuestion: {manual_q}"
        response = ask_openai(prompt)
        st.markdown(response)

# --- TAB 3: Calorie & Macro Calculator ---
with tabs[2]:
    st.header("🥗 Calorie & Macro Estimator")
    weight = st.number_input("Current Weight (kg)", 30.0, 200.0, 70.0)
    goal_weight = st.number_input("Goal Weight (kg)", 30.0, 200.0, 65.0)
    weeks = st.slider("Weeks to reach goal", 4, 52, 16)
    activity = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active"])

    tdee_values = {"Sedentary": 1600, "Lightly Active": 1850, "Moderately Active": 2050}
    tdee = tdee_values.get(activity, 1850)
    deficit = 375
    intake = tdee - deficit

    p = round(0.3 * intake / 4)
    c = round(0.4 * intake / 4)
    f = round(0.3 * intake / 9)

    st.markdown(f"**Daily Calories:** {int(intake)} kcal")
    st.markdown(f"**Protein:** {p} g")
    st.markdown(f"**Carbohydrates:** {c} g")
    st.markdown(f"**Fats:** {f} g")

# --- TAB 4: About Lauren ---
with tabs[3]:
    st.header("📋 About Lauren Yates")
    st.markdown(extract_text_from_pdf(document_files["Lauren Avatar"])[:3000])
    st.markdown("---")
    st.markdown("Want to become a PT like Lauren? Ask about our training pathways and mentorships.")

# --- FOOTER ---
st.markdown("---")
st.markdown("🧠 Powered by Focus Fitness • Contact: support@focusfitness.co.uk")
