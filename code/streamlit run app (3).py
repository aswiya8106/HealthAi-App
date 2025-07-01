import streamlit as st
import google.generativeai as genai

# Set your Gemini API Key
GOOGLE_API_KEY = "AIzaSyALFLzUNAAH9TxHjCLAXqx4IwERbWuLO5c"  # <-- Replace this
genai.configure(api_key=GOOGLE_API_KEY)

# Load Gemini model
model = genai.GenerativeModel("models/gemini-1.5-flash")

# Function to call Gemini AI
def ask_ai(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Error: {e}"

# Streamlit Setup
st.set_page_config(page_title="HealthAI", layout="centered")
st.title("🧠 HealthAI Assistant")

# Tabs
predict_tab, treatment_tab, ask_tab, analytics_tab = st.tabs([
    "🩺 Predict Disease",
    "💊 Treatment Plans",
    "💬 Chat",
    "📊 Health Analytics"
])

# Shared variable for storing predicted disease
if "predicted_disease" not in st.session_state:
    st.session_state.predicted_disease = ""

# --- 1. Predict Disease Tab ---
with predict_tab:
    st.header("Enter Symptoms")
    symptoms = st.text_input("Symptoms (comma-separated)", placeholder="e.g., fever, cold, headache")

    if st.button("Predict Disease"):
        if symptoms.strip():
            with st.spinner("Predicting disease..."):
                prompt = f"I have symptoms: {symptoms}. What is the most likely disease? Reply with the disease name only."
                disease = ask_ai(prompt)
                st.session_state.predicted_disease = disease
                st.success(f"Predicted Disease: {disease}")
        else:
            st.warning("Please enter symptoms to predict the disease.")

# --- 2. Treatment Plans Tab ---
with treatment_tab:
    st.header("Treatment Plans")

    if st.session_state.predicted_disease:
        disease = st.session_state.predicted_disease

        with st.spinner("Getting treatment plan..."):
            treatment_prompt = f"What is the treatment plan for {disease}? Include natural home remedies and common medicines (if any)."
            treatment_plan = ask_ai(treatment_prompt)

        st.success(f"Treatment Plan for {disease}")
        st.write(treatment_plan)
    else:
        st.info("🔍 Please predict a disease first in the 'Predict Disease' tab.")

# --- 3. Ask AI Tab ---
with ask_tab:
    st.header("Ask Health-Related Questions")
    question = st.text_input("Ask something...", placeholder="e.g., What are the symptoms of dengue?")

    if st.button("Ask AI"):
        if question.strip():
            with st.spinner("Thinking..."):
                answer = ask_ai(question)
            st.success("AI Response:")
            st.write(answer)
        else:
            st.warning("Please enter a question.")

# --- 4. Health Analytics Tab ---
with analytics_tab:
    st.header("📊 Health Analytics ")
    st.markdown("""
    - **🧬 Most common reported symptoms this week:**  
      - Fever, Cold, Headache, Cough

    - **📈 Trending diseases:**  
      - Flu, Typhoid, COVID-19 Variant X

    - **💊 Top medicines prescribed:**  
      - Paracetamol, Azithromycin, ORS

    - **🌱 Most asked natural remedies:**  
      - Ginger tea, Turmeric milk, Steam inhalation

    - **⚕️ Health Tip of the Day:**  
      > "Stay hydrated, sleep 7–8 hours daily, and avoid processed foods."
    """)
