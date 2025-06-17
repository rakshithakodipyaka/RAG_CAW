# Intelligent Document Q&A System - CAW Studios Project

An end-to-end LangChain-based system for intelligent Q&A over documents using:

## 🔧 Technologies Used

- 🔍 Google Gemini (via Generative AI)
- 📚 LangChain for RAG & Memory
- 📦 FastAPI backend
- 🌐 Streamlit frontend
- 🧠 ChromaDB vector store
- 📝 Feedback & Evaluation dashboard

## 🚀 Features

- Upload PDF, DOCX, or TXT files
- Ask questions with conversational memory
- Store Q&A history
- Rate & suggest improved answers
- Real-time analytics (average rating, feedback count)
- Clean UI via Streamlit sidebar and rating system

## 🛠️ Technologies Stack

- Python
- FastAPI
- Streamlit
- LangChain
- Google Generative AI (Gemini)
- ChromaDB
- PyMuPDF / python-docx / unstructured

## ⚙️ Setup Instructions

1️⃣ Clone the repo
git clone https://github.com/YOUR_USERNAME/langchain-doc-qa.git
cd langchain-doc-qa
2️⃣ Install dependencies
pip install -r requirements.txt
3️⃣ Add .env file
Create a .env file in the root directory and add your Google API key:
GOOGLE_API_KEY=your_google_generative_ai_api_key
4️⃣ Start FastAPI backend
uvicorn yourfilename:app --reload
5️⃣ Start Streamlit frontend
streamlit run your_streamlit_file.py
