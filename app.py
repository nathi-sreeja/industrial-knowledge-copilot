import streamlit as st
from groq import Groq
from retriever import retrieve
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(
    page_title="Industrial Knowledge Copilot",
    page_icon="🏭",
    layout="wide"
)

st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #0A0F1E;
        color: #FFFFFF;
    }

    /* Hide default streamlit header */
    #MainMenu, footer, header {visibility: hidden;}

    /* Custom header */
    .main-header {
        background: linear-gradient(135deg, #111B2E 0%, #0A0F1E 100%);
        border: 1px solid #00C9A7;
        border-radius: 16px;
        padding: 24px 32px;
        margin-bottom: 24px;
    }
    .main-title {
        font-size: 2.4rem;
        font-weight: 800;
        color: #FFFFFF;
        margin: 0;
    }
    .main-title span {
        color: #00C9A7;
    }
    .main-subtitle {
        color: #7A8FAD;
        font-size: 1rem;
        margin-top: 6px;
    }

    /* Stats bar */
    .stats-bar {
        display: flex;
        gap: 16px;
        margin-bottom: 24px;
    }
    .stat-card {
        background: #111B2E;
        border: 1px solid #1E2D45;
        border-radius: 12px;
        padding: 16px 24px;
        flex: 1;
        text-align: center;
    }
    .stat-number {
        font-size: 1.8rem;
        font-weight: 800;
        color: #00C9A7;
    }
    .stat-label {
        font-size: 0.8rem;
        color: #7A8FAD;
        margin-top: 4px;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #111B2E;
        border-radius: 12px;
        padding: 4px;
        gap: 4px;
        border: 1px solid #1E2D45;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #7A8FAD;
        border-radius: 8px;
        font-weight: 600;
        padding: 10px 24px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00C9A7 !important;
        color: #0A0F1E !important;
    }

    .stTabs [aria-selected="false"] {
        background-color: #1E2D45 !important;
        color: #FFFFFF !important;
    }

    /* Input styling */
    .stTextInput > div > div > input {
        background-color: #111B2E;
        border: 1px solid #1E2D45;
        border-radius: 10px;
        color: #FFFFFF;
        padding: 12px 16px;
        font-size: 1rem;
    }
    .stTextInput > div > div > input:focus {
        border-color: #00C9A7;
        box-shadow: 0 0 0 2px rgba(0, 201, 167, 0.2);
    }

    /* Force textarea dark */
    textarea {
        background-color: #111B2E !important;
        color: #FFFFFF !important;
        caret-color: #00C9A7 !important;
    }
    
    /* Force input dark */
    input {
        background-color: #111B2E !important;
        color: #FFFFFF !important;
        caret-color: #00C9A7 !important;
    }
    .stTextArea > div > div > textarea {
        background-color: #111B2E !important;
        border: 1px solid #1E2D45 !important;
        border-radius: 10px !important;
        color: #FFFFFF !important;
        font-size: 0.95rem !important;
    }
    .stTextArea > div > div > textarea:focus {
        border-color: #00C9A7;
        box-shadow: 0 0 0 2px rgba(0, 201, 167, 0.2);
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #00C9A7, #4F8EF7);
        color: #0A0F1E;
        border: none;
        border-radius: 10px;
        font-weight: 700;
        font-size: 1rem;
        padding: 12px 32px;
        width: 100%;
        transition: opacity 0.2s;
    }
    .stButton > button:hover {
        opacity: 0.9;
        color: #0A0F1E;
    }

    /* Answer card */
    .answer-card {
        background: #111B2E;
        border: 1px solid #00C9A7;
        border-radius: 14px;
        padding: 24px;
        margin-top: 20px;
    }
    .answer-label {
        color: #00C9A7;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 12px;
    }
    .answer-text {
        color: #FFFFFF;
        font-size: 1rem;
        line-height: 1.7;
    }

    /* Source card */
    .source-card {
        background: #0D1A30;
        border: 1px solid #1E2D45;
        border-radius: 10px;
        padding: 16px;
        margin-top: 8px;
    }
    .source-label {
        color: #4F8EF7;
        font-size: 0.8rem;
        font-weight: 700;
    }
    .source-text {
        color: #C8D8F0;
        font-size: 0.85rem;
        margin-top: 6px;
        line-height: 1.5;
    }

    /* Compliance card */
    .compliance-card {
        background: #111B2E;
        border: 1px solid #F7B731;
        border-radius: 14px;
        padding: 24px;
        margin-top: 20px;
    }
    .compliance-label {
        color: #F7B731;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 12px;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background-color: #111B2E;
        border-radius: 10px;
        color: #7A8FAD;
    }

    /* Labels */
    .stTextInput label, .stTextArea label {
        color: #C8D8F0 !important;
        font-weight: 600;
    }

    /* Spinner */
    .stSpinner > div {
        border-top-color: #00C9A7 !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <div class="main-title">🏭 Industrial Knowledge <span>Copilot</span></div>
    <div class="main-subtitle">AI-powered knowledge retrieval across all your industrial documents — instantly.</div>
</div>
""", unsafe_allow_html=True)

# Stats bar
st.markdown("""
<div class="stats-bar">
    <div class="stat-card">
        <div class="stat-number">7</div>
        <div class="stat-label">Documents Indexed</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">RAG</div>
        <div class="stat-label">Powered By</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">llama-3.3</div>
        <div class="stat-label">AI Model</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">&lt;2s</div>
        <div class="stat-label">Response Time</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Tabs
tabs = st.tabs(["💬  Q&A Copilot", "✅  Compliance Gap Checker"])

# --- Tab 1: Q&A ---
with tabs[0]:
    st.markdown("<br>", unsafe_allow_html=True)
    query = st.text_input(
        "Ask a question about your industrial documents:",
        placeholder="e.g. What is the maintenance interval for the pump?"
    )

    if st.button("🔍  Search Knowledge Base", key="qa_btn") and query:
        with st.spinner("Searching across all documents..."):
            chunks = retrieve(query)
            context = "\n\n".join([f"[Source: {c['source']}]\n{c['text']}" for c in chunks])
            prompt = f"""You are an industrial knowledge assistant.
Answer the question using only the context below.
Always mention which document your answer comes from.
If the answer is not in the context, say "Not found in documents."

Context:
{context}

Question: {query}
Answer:"""
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            answer = response.choices[0].message.content

            st.markdown(f"""
            <div class="answer-card">
                <div class="answer-label">🤖 AI ANSWER</div>
                <div class="answer-text">{answer}</div>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("📄 View source document chunks"):
                for c in chunks:
                    st.markdown(f"""
                    <div class="source-card">
                        <div class="source-label">📁 {c['source']}</div>
                        <div class="source-text">{c['text'][:300]}...</div>
                    </div>
                    """, unsafe_allow_html=True)

# --- Tab 2: Compliance ---
with tabs[1]:
    st.markdown("<br>", unsafe_allow_html=True)
    checklist = st.text_area(
        "Paste your regulatory checklist (one item per line):",
        height=200,
        placeholder="e.g.\n1. Fire extinguisher must be checked monthly\n2. PPE must be worn in all zones\n3. Gas levels must be monitored every 2 hours"
    )

    if st.button("✅  Run Compliance Check", key="comp_btn") and checklist:
        with st.spinner("Auditing documents against checklist..."):
            chunks = retrieve(checklist, top_k=6)
            context = "\n\n".join([f"[Source: {c['source']}]\n{c['text']}" for c in chunks])
            prompt = f"""You are an industrial compliance auditor.
Below is a regulatory checklist and excerpts from company documents.
For each checklist item, respond with:
✅ Covered — if the document clearly addresses it
⚠️ Partial — if it is mentioned but not fully addressed
❌ Missing — if there is no mention in the documents

Always state which document supports your decision.

Documents:
{context}

Checklist:
{checklist}

Compliance Report:"""
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            report = response.choices[0].message.content

            st.markdown(f"""
            <div class="compliance-card">
                <div class="compliance-label">📋 COMPLIANCE REPORT</div>
                <div class="answer-text">{report}</div>
            </div>
            """, unsafe_allow_html=True)