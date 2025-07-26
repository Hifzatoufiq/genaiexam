import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64

# --- PAGE CONFIG ---
st.set_page_config(page_title="🧠 GenAI Final Exam", layout="wide")

# --- BACKGROUND IMAGE FROM LOCAL FILE ---
def set_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    css = f"""
    <style>
    body {{
       
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
        background-position: center;
    }}
    .main {{
        background-color: rgba(255,255,255,0.85);
        padding: 2rem;
        border-radius: 15px;
    }}
    .title {{
        font-size: 2.5rem;
        color: #333;
        text-align: center;
        margin-bottom: 1rem;
    }}
    .subtitle {{
        font-size: 1.2rem;
        color: #222;
    }}
    .question {{
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }}
    .result-box {{
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 10px;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# --- QUESTIONS ---
questions = [
    {"question": "What is ChatGPT primarily used for?", "options": ["A. Cooking", "B. Writing and Chatting", "C. Video Editing", "D. Drawing"], "answer": "B"},
    {"question": "Gemini is developed by which company?", "options": ["A. Meta", "B. Microsoft", "C. Google", "D. Apple"], "answer": "C"},
    {"question": "Blackbox AI is mainly used to?", "options": ["A. Play Games", "B. Copy code from videos", "C. Make music", "D. Generate images"], "answer": "B"},
    {"question": "What can Canva help you create?", "options": ["A. Python Code", "B. Graphic Designs", "C. Games", "D. Chatbots"], "answer": "B"},
    {"question": "Looka is used for?", "options": ["A. Logo Design", "B. Shopping", "C. Code Debugging", "D. Video Captions"], "answer": "A"},
    {"question": "PresentationAI helps to?", "options": ["A. Write Essays", "B. Make Slides", "C. Record Audio", "D. Learn HTML"], "answer": "B"},
    {"question": "Durable AI builds?", "options": ["A. Websites", "B. TikToks", "C. Music", "D. eBooks"], "answer": "A"},
    {"question": "What type of app is Gamma?", "options": ["A. Presentation Tool", "B. AI Detector", "C. PDF Maker", "D. None"], "answer": "A"},
    {"question": "Pictory is best for?", "options": ["A. PDF Editing", "B. Resume Making", "C. Video Creation", "D. Coding"], "answer": "C"},
    {"question": "Lumen5 turns text into?", "options": ["A. Games", "B. Videos", "C. Slides", "D. Emails"], "answer": "B"},
    {"question": "Writesonic generates?", "options": ["A. Code", "B. Art", "C. Content", "D. Graphs"], "answer": "C"},
    {"question": "CheckerAI is used for?", "options": ["A. Grammar & Plagiarism", "B. Music Composition", "C. Drawing", "D. Email Spamming"], "answer": "A"},
    {"question": "Runway is best for?", "options": ["A. 3D Design", "B. AI Video Editing", "C. PDF Viewing", "D. Surveys"], "answer": "B"},
    {"question": "ChatGPT can help in?", "options": ["A. Drawing", "B. Solving MCQs", "C. Washing Dishes", "D. Sleeping"], "answer": "B"},
    {"question": "Gemini works with which products?", "options": ["A. Adobe", "B. Google", "C. Firefox", "D. Zoom"], "answer": "B"},
    {"question": "Blackbox can be used inside?", "options": ["A. Google Meet", "B. VS Code", "C. TikTok", "D. YouTube"], "answer": "B"},
    {"question": "Canva provides?", "options": ["A. Image Templates", "B. Database", "C. Python Libraries", "D. Hosting"], "answer": "A"},
    {"question": "Which tool is like ChatGPT?", "options": ["A. Gemini", "B. Canva", "C. Pictory", "D. Looka"], "answer": "A"},
    {"question": "PresentationAI saves time by?", "options": ["A. Writing code", "B. Auto-making slides", "C. Reading books", "D. Writing novels"], "answer": "B"},
    {"question": "Durable builds websites in?", "options": ["A. Minutes", "B. Hours", "C. Days", "D. Months"], "answer": "A"},
    {"question": "Gamma is best for?", "options": ["A. Presentations", "B. Music", "C. Maps", "D. Drawing"], "answer": "A"},
    {"question": "Pictory is known for?", "options": ["A. Writing blogs", "B. Creating videos from text", "C. Making resumes", "D. Uploading PDFs"], "answer": "B"},
    {"question": "Lumen5 is an AI-based?", "options": ["A. Coding Platform", "B. Video Maker", "C. Chat App", "D. Social Network"], "answer": "B"},
    {"question": "Writesonic is used to write?", "options": ["A. Shopping Lists", "B. AI Content", "C. Medical Reports", "D. Invoices"], "answer": "B"},
    {"question": "CheckerAI detects?", "options": ["A. Fake profiles", "B. Spelling & Plagiarism", "C. AI bots", "D. Phone numbers"], "answer": "B"},
    {"question": "Runway can remove?", "options": ["A. AI", "B. Objects in videos", "C. Passwords", "D. Audio"], "answer": "B"},
    {"question": "ChatGPT can generate?", "options": ["A. Weather reports", "B. Videos", "C. Text-based answers", "D. Movies"], "answer": "C"},
    {"question": "Gemini gives answers using?", "options": ["A. Wikipedia only", "B. Google + AI", "C. TikTok", "D. Files"], "answer": "B"},
    {"question": "Durable is helpful for?", "options": ["A. Students", "B. Business websites", "C. Doctors", "D. Actors"], "answer": "B"},
    {"question": "Runway helps with?", "options": ["A. Code Testing", "B. AI-based Video Creation", "C. SEO Ranking", "D. PowerPoint"], "answer": "B"},
]

# --- DATA STORAGE FILE ---
RESULTS_FILE = "student_results.csv"

def save_result(name, course, start_date, score, total):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.DataFrame([{
        "Name": name,
        "Course": course,
        "Start Date": start_date,
        "Score": score,
        "Total": total,
        "Percentage": (score / total) * 100,
        "Submitted": now
    }])
    df.to_csv(RESULTS_FILE, mode='a', header=not os.path.exists(RESULTS_FILE), index=False)

# --- UI FORM ---
st.markdown('<div class="title">🧠 GenAI Short Course Final Exam</div>', unsafe_allow_html=True)
name = st.text_input("👤 Enter Student Name")
course = st.text_input("📘 Course Title", value="GenAI Short Course")
start_exam = st.button("🚀 Start Exam")

if start_exam:
    st.session_state.start_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.start_exam = True

if "start_exam" in st.session_state and st.session_state.start_exam:
    selected_answers = []
    st.markdown('<div class="subtitle">📝 Answer the following questions:</div>', unsafe_allow_html=True)

    for i, q in enumerate(questions):
        with st.container():
            st.markdown(f"<div class='question'><strong>Q{i+1}:</strong> {q['question']}</div>", unsafe_allow_html=True)
            selected = st.radio("", options=q['options'], key=f"q{i}")
            selected_answers.append(selected.split(".")[0])  # Store only A/B/C/D

    if st.button("✅ Submit Exam"):
        score = 0
        for i, q in enumerate(questions):
            if selected_answers[i] == q["answer"]:
                score += 1

        total = len(questions)
        percentage = (score / total) * 100

        st.success(f"🎉 {name}, you scored {score}/{total} ({percentage:.2f}%)")
        save_result(name, course, st.session_state.start_date, score, total)

        st.markdown(f"""
        <div class='result-box'>
        <strong>🧾 Result Receipt</strong><br>
        Name: {name}<br>
        Course: {course}<br>
        Start Date: {st.session_state.start_date}<br>
        Score: {score} / {total}<br>
        Percentage: {percentage:.2f}%<br>
        Grade: {"A" if score >= 24 else "B" if score >= 18 else "C"}<br>
        Status: {"✅ Passed" if score >= 15 else "❌ Failed"}
        </div>
        """, unsafe_allow_html=True)

# View All Results
if st.button("📊 View All Results"):
    if os.path.exists(RESULTS_FILE):
        df = pd.read_csv(RESULTS_FILE)
        st.dataframe(df)
    else:
        st.info("No results available yet.")
