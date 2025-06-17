import streamlit as st
import requests
import base64
from pathlib import Path

API_BASE = "http://localhost:8000"

# ---------------- Page Config with Custom Icon ----------------
st.set_page_config(page_title="📄 Gemini Document Q&A", layout="wide")

# ---------------- Background Image Setup ----------------
bg_path = Path(r"C:\Users\Nikitha\OneDrive\Desktop\ragmodel\images\3274387.jpg")

# Read image bytes and encode as base64
image_bytes = bg_path.read_bytes()
encoded_string = base64.b64encode(image_bytes).decode()

page_bg = f"""
<style>
body {{
    background-image: url("data:image/jpeg;base64,{encoded_string}");
    background-size: cover;
    background-attachment: fixed;
    background-repeat: no-repeat;
}}

.block-container {{
    background-color: rgba(0, 0, 0, 0.6);  /* transparent black glassy effect */
    border-radius: 20px;
    padding: 2rem;
    backdrop-filter: blur(6px);
    color: white;
}}

h1, h2, h3 {{
    color: #ffcc00;
}}

.stTextInput > div > input, .stTextArea > div > textarea {{
    background-color: #1e1e1e;
    color: white;
    border-radius: 8px;
    padding: 10px;
    border: 1px solid #444;
}}

.stButton > button {{
    background-color: #ff5722;
    color: white;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    padding: 0.6em 1.5em;
    transition: 0.3s;
}}

.stButton > button:hover {{
    background-color: #e64a19;
}}

.answer-box {{
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid #ffffff20;
    padding: 1em;
    border-radius: 12px;
    color: #fff;
    font-size: 1.1em;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
    margin-top: 1rem;
}}

.sidebar .sidebar-content {{
    background: rgba(0, 0, 0, 0.7);
}}
</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)

st.title("📄 Intelligent Document Q&A with Feedback")

# ---------- Session State ----------
if 'uploaded' not in st.session_state:
    st.session_state.uploaded = False
if 'last_query' not in st.session_state:
    st.session_state.last_query = None
if 'last_answer' not in st.session_state:
    st.session_state.last_answer = None

# ---------- Sidebar: Q&A History ----------
with st.sidebar:
    st.header("📜 Q&A History")
    try:
        history_res = requests.get(f"{API_BASE}/history")
        if history_res.status_code == 200:
            history = history_res.json().get("history", [])
            if history:
                for i, item in enumerate(reversed(history[-10:]), 1):
                    st.markdown(f"**{i}. {item['question']}**\n\n→ {item['answer']}")
            else:
                st.info("No Q&A history yet.")
        else:
            st.error("❌ Failed to load history.")
    except Exception as e:
        st.error(f"Error: {e}")

# ---------- Phase 1: File Upload ----------
st.header("📂 1. Upload a Document")

if not st.session_state.uploaded:
    uploaded_file = st.file_uploader("Upload PDF, DOCX, or TXT", type=["pdf", "docx", "txt"])
    if uploaded_file:
        with st.spinner("Uploading and processing..."):
            files = {'file': (uploaded_file.name, uploaded_file, uploaded_file.type)}
            res = requests.post(f"{API_BASE}/upload", files=files)
            if res.status_code == 200:
                st.success(res.json().get("message", "Upload successful!"))
                st.session_state.uploaded = True
            else:
                st.error(f"Upload failed: {res.text}")
else:
    st.success("✅ Document already uploaded.")
    if st.button("🔁 Upload New Document"):
        st.session_state.uploaded = False
        st.experimental_rerun()

# ---------- Phase 2: Ask Questions ----------
if st.session_state.uploaded:
    st.header("💬 2. Ask a Question")
    query = st.text_input("🔎 What do you want to know from this document?")

    if st.button("🧠 Ask"):
        if query:
            with st.spinner("Thinking..."):
                res = requests.post(f"{API_BASE}/ask", json={"query": query})
                if res.status_code == 200:
                    answer = res.json().get("answer", "No answer returned.")
                    st.session_state.last_query = query
                    st.session_state.last_answer = answer
                else:
                    st.error("❌ Failed to get answer.")
                    st.session_state.last_query = None
                    st.session_state.last_answer = None
        else:
            st.warning("⚠️ Please enter a question.")

    if st.session_state.last_answer:
        st.markdown("### 🧠 Answer:")
        st.markdown(f'<div class="answer-box">{st.session_state.last_answer}</div>', unsafe_allow_html=True)

        # ---------- Phase 3: Feedback ----------
        st.subheader("📝 3. Provide Feedback")
        col1, col2 = st.columns(2)
        with col1:
            rating = st.slider("⭐ Rate the answer (1 = Poor, 5 = Great)", 1, 5, 3)
        with col2:
            correction = st.text_area("💡 Suggest a better answer (optional)")

        if st.button("📤 Submit Feedback"):
            fb_payload = {
                "question": st.session_state.last_query,
                "answer": st.session_state.last_answer,
                "rating": int(rating),
                "correction": correction or ""
            }

            fb_res = requests.post(f"{API_BASE}/feedback", json=fb_payload)

            if fb_res.status_code == 200:
                st.success("✅ Feedback submitted! Thank you 🙌")
                st.session_state.last_query = None
                st.session_state.last_answer = None
            else:
                st.error(f"❌ Failed to submit feedback: {fb_res.text}")
