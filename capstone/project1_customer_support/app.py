"""
Customer Support Intelligence Bot — Streamlit UI

Tabs:
    Chat        Multi-turn chat with source citations in the sidebar
    Evaluation  Run the evaluation pipeline and view results
"""
import streamlit as st

from config import GEMINI_API_KEY, EVAL_QUESTIONS_PATH, EVAL_LOG_PATH
from agents.agent import agent
from evaluation.evaluator import run_evaluation

# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Support Bot",
    page_icon="💬",
    layout="wide",
)

# ── API key guard ─────────────────────────────────────────────────────────────

if not GEMINI_API_KEY:
    st.error(
        "**GEMINI_API_KEY is not set.** "
        "Make sure your Codespace has the COURSE_PASSPHRASE secret configured "
        "and that setup.sh ran successfully."
    )
    st.stop()

# ── Gemini client ─────────────────────────────────────────────────────────────

# TODO: Initialise the Gemini client here and store in st.session_state.
# Hint: Prompt Gemini CLI —
#   "Show me how to initialise a google-genai client using GEMINI_API_KEY
#   and store it in st.session_state so it is only created once."

# ── Session state ─────────────────────────────────────────────────────────────

if "messages" not in st.session_state:
    st.session_state.messages = []   # {"role": "user"|"assistant", "content": str, "sources": list}

if "last_sources" not in st.session_state:
    st.session_state.last_sources = []

if "last_ticket_id" not in st.session_state:
    st.session_state.last_ticket_id = None

# ── Tabs ──────────────────────────────────────────────────────────────────────

chat_tab, eval_tab = st.tabs(["💬 Chat", "📊 Evaluation"])


# ─────────────────────────────────────────────────────────────────────────────
# Chat tab
# ─────────────────────────────────────────────────────────────────────────────

with chat_tab:
    col_chat, col_sources = st.columns([3, 1])

    with col_chat:
        st.title("Customer Support Bot")
        st.caption("Ask any question about our product. Powered by Gemini + RAG.")

        # Render conversation history
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                if msg["role"] == "assistant" and msg.get("ticket_id"):
                    st.info(f"🎫 Ticket created: **{msg['ticket_id']}**")

        # Chat input
        if prompt := st.chat_input("Ask a support question..."):
            # Show user message immediately
            st.session_state.messages.append({"role": "user", "content": prompt, "sources": [], "ticket_id": None})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Run the agent
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    # TODO: Build chat_history from st.session_state.messages and invoke the agent.
                    # Hint: Prompt Gemini CLI —
                    #   "Write the agent invocation block for a Streamlit chat app.
                    #   Convert st.session_state.messages to the chat_history format
                    #   expected by SupportState, invoke the agent, then display
                    #   the answer and store sources in session state."
                    output = agent.invoke({
                        "query":            prompt,
                        "chat_history":     [],      # TODO: pass real history
                        "product_area":     None,
                        "retrieved_chunks": [],
                        "tool_calls":       [],
                        "answer":           "",
                        "sources":          [],
                        "ticket_id":        None,
                        "route":            None,
                    })

                answer    = output.get("answer", "Sorry, I couldn't generate an answer.")
                sources   = output.get("sources", [])
                ticket_id = output.get("ticket_id")

                st.markdown(answer)
                if ticket_id:
                    st.info(f"🎫 Ticket created: **{ticket_id}**")

            st.session_state.messages.append({
                "role":      "assistant",
                "content":   answer,
                "sources":   sources,
                "ticket_id": ticket_id,
            })
            st.session_state.last_sources   = sources
            st.session_state.last_ticket_id = ticket_id
            st.rerun()

    # Sources sidebar
    with col_sources:
        st.subheader("📄 Sources")
        if st.session_state.last_sources:
            for i, src in enumerate(st.session_state.last_sources, 1):
                with st.expander(f"{i}. {src.get('title', src.get('source', 'Unknown'))}"):
                    st.caption(f"**Product area:** {src.get('product_area', '—')}")
                    st.caption(f"**File:** {src.get('source', '—')}")
                    if "rrf_score" in src:
                        st.caption(f"**Relevance score:** {src['rrf_score']:.3f}")
        else:
            st.caption("Sources will appear here after your first question.")

        if st.session_state.messages:
            if st.button("🗑 Clear conversation"):
                st.session_state.messages     = []
                st.session_state.last_sources = []
                st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# Evaluation tab
# ─────────────────────────────────────────────────────────────────────────────

with eval_tab:
    st.title("Evaluation Dashboard")
    st.caption(f"Runs the agent against all questions in `{EVAL_QUESTIONS_PATH.name}` and scores faithfulness & relevance.")

    if st.button("▶ Run Evaluation", type="primary"):
        with st.spinner("Running evaluation — this may take a few minutes..."):
            # TODO: pass the initialised Gemini client instead of None
            summary = run_evaluation(
                agent=agent,
                gemini_client=None,
                questions_path=EVAL_QUESTIONS_PATH,
                log_path=EVAL_LOG_PATH,
            )

        st.success(f"Evaluated {summary['n']} questions")

        col1, col2 = st.columns(2)
        col1.metric("Avg Faithfulness", f"{summary['avg_faithfulness']:.2f} / 1.00")
        col2.metric("Avg Relevance",    f"{summary['avg_relevance']:.2f} / 1.00")

    # Show previous results if the log file exists
    if EVAL_LOG_PATH.exists():
        import json
        import pandas as pd

        records = [json.loads(line) for line in EVAL_LOG_PATH.read_text().splitlines() if line.strip()]
        if records:
            st.subheader("Previous Results")
            df = pd.DataFrame(records)[["timestamp", "query", "faithfulness", "relevance", "route", "num_sources"]]
            st.dataframe(df, use_container_width=True)
    else:
        st.info("No evaluation results yet. Click **Run Evaluation** to generate them.")
