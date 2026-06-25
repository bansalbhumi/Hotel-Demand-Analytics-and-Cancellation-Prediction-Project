import streamlit as st
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from src.agent import AIAnalystAgent

EXAMPLE_QUESTIONS = [
    "Which market segment has the highest cancellation rate?",
    "What is the average ADR for Resort vs City Hotels?",
    "How does cancellation rate change with lead time?",
    "Give me the top 5 countries by total bookings.",
    "What percentage of bookings have non-refundable deposits?",
    "Show monthly booking trend for both hotel types.",
    "Which customer type cancels the most?",
    "What are 3 revenue improvement recommendations?",
]

@st.cache_resource
def get_agent():
    return AIAnalystAgent()


def render_ai_analyst_page():
    # ── Header ────────────────────────────────────────────────────────────────
    st.header("🤖 AI Data Analyst")
    st.markdown(
        "Ask any natural-language question about the hotel booking dataset. "
        "The AI Analyst converts your question into a safe, read-only SQL query, "
        "executes it against the live data, and explains the result in plain English."
    )

    agent = get_agent()

    # ── API key guard ─────────────────────────────────────────────────────────
    if not agent.llm:
        st.info(
            "**Running in Demo Mode.** The AI Analyst is currently providing simulated responses. "
            "To unlock full dynamic SQL querying, please enter a free Google Gemini API Key below.",
            icon="ℹ️"
        )
        api_key_input = st.text_input("Gemini API Key", type="password", placeholder="AIzaSy...")
        if api_key_input:
            os.environ["GOOGLE_API_KEY"] = api_key_input
            get_agent.clear()
            st.rerun()
        st.markdown("---")
        st.caption("Don't have an API key? Get one [here](https://aistudio.google.com/app/apikey).")

    # ── Example question chips ─────────────────────────────────────────────────
    st.markdown("#### 💡 Example Questions — click to ask instantly")
    
    # Render chips in a 4-column grid
    cols = st.columns(4)
    clicked_question = None
    for i, q in enumerate(EXAMPLE_QUESTIONS):
        if cols[i % 4].button(q, key=f"chip_{i}", use_container_width=True):
            clicked_question = q

    st.markdown("---")

    # ── Chat history ──────────────────────────────────────────────────────────
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Render existing messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ── Handle chip click or free-text input ──────────────────────────────────
    prompt = clicked_question or st.chat_input(
        "Ask a question (e.g. 'What is the cancellation rate for Online TA segment?')"
    )

    if prompt:
        # Display the user's message
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Query the agent
        with st.spinner("🔍 Analysing data and generating SQL…"):
            response = agent.ask(prompt)

        # Display the response
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

    # ── Clear history button ──────────────────────────────────────────────────
    if st.session_state.get("messages"):
        if st.button("🗑️ Clear conversation", key="clear_chat"):
            st.session_state.messages = []
            st.rerun()
