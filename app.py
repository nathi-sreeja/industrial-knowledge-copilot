import streamlit as st
from groq import Groq
from retriever import retrieve
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="Industrial Knowledge Copilot", page_icon="🏭")
st.title("🏭 Industrial Knowledge Copilot")
st.caption("Ask anything about your equipment manuals and safety procedures.")

tabs = st.tabs(["💬 Q&A Copilot", "✅ Compliance Gap Checker"])

# --- Tab 1: Q&A ---
with tabs[0]:
    query = st.text_input("Ask a question:", placeholder="e.g. What is the maintenance interval for the pump?")
    if st.button("Ask", key="qa_btn") and query:
        with st.spinner("Searching documents..."):
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
            st.markdown("### Answer")
            st.write(answer)
            with st.expander("📄 Source chunks used"):
                for c in chunks:
                    st.markdown(f"**{c['source']}**")
                    st.write(c["text"])
                    st.divider()

# --- Tab 2: Compliance Gap Checker ---
with tabs[1]:
    st.markdown("Paste a **safety/regulatory checklist** and the tool will check your documents for gaps.")
    checklist = st.text_area("Paste checklist items (one per line):", height=200,
        placeholder="e.g.\n1. Fire extinguisher must be checked monthly\n2. PPE must be worn in Zone A\n3. Gas levels must be monitored every 2 hours")
    if st.button("Check Compliance", key="comp_btn") and checklist:
        with st.spinner("Checking documents against checklist..."):
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
            st.markdown("### Compliance Report")
            st.write(report)