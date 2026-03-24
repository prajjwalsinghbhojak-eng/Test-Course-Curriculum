"""
LangGraph agent for the Customer Support Intelligence Bot.

Graph topology:
    classify_query → direct_answer  → END
                   → product_lookup → END
                   → escalation     → END

Nodes:
    classify_query  Decides how to route the query (structured output from Gemini).
    direct_answer   Hybrid retrieval + cited answer generation.
    product_lookup  Filters retrieval to a product area, then generates answer.
    escalation      Creates a support ticket and returns an empathetic response.

Each node is provided as a stub with a clear TODO and a Gemini CLI hint.
Use `gemini` in the terminal to implement each node one at a time.
"""
from typing import TypedDict, Literal, Optional
from langgraph.graph import StateGraph, END


# ── Agent state ───────────────────────────────────────────────────────────────

class SupportState(TypedDict):
    query: str
    chat_history: list          # list of {"role": "user"|"assistant", "content": str}
    product_area: Optional[str] # set by classify_query if detected
    retrieved_chunks: list      # set by retrieval nodes
    tool_calls: list            # log of tool calls made
    answer: str                 # final generated answer
    sources: list               # source metadata shown in UI sidebar
    ticket_id: Optional[str]    # set by escalation node
    route: Optional[Literal["direct_answer", "product_lookup", "escalation"]]


# ── Tools (function calling) ──────────────────────────────────────────────────

def search_by_product_area(area: str, query: str) -> list:
    """
    Retrieve chunks filtered to a specific product area.

    TODO: Call dense_retrieve() from retrieval/retriever.py with a product_area filter.
    Hint: Prompt Gemini CLI —
        "Implement search_by_product_area. It should generate a query embedding using
        the Gemini embedding API, then call dense_retrieve with the product_area filter."
    """
    return []


def create_support_ticket(issue_summary: str, severity: str = "medium") -> str:
    """
    Simulate ticket creation. Returns a mock ticket ID.

    TODO: Generate a realistic-looking ticket ID and log the ticket details.
    Hint: Use uuid or a formatted string like "TKT-{timestamp}-{random}".
    """
    return "TKT-TODO"


def get_related_articles(source_filename: str) -> list:
    """
    Return articles with the same product_area as the given source file.

    TODO: Query ChromaDB metadata to find articles in the same product area.
    Hint: Prompt Gemini CLI —
        "Implement get_related_articles. Query ChromaDB for chunks where
        product_area matches the product_area of source_filename, excluding
        chunks from that file itself."
    """
    return []


# ── Nodes ─────────────────────────────────────────────────────────────────────

def classify_query(state: SupportState) -> SupportState:
    """
    Analyse the query and decide how to route it.

    Sets:
        state["route"]        → "direct_answer" | "product_lookup" | "escalation"
        state["product_area"] → detected product area string, or None

    Routing rules:
        - "escalation"     if the user explicitly asks to raise a ticket, or if
                           the query is a complaint with no clear factual answer
        - "product_lookup" if a specific product area is clearly mentioned
        - "direct_answer"  for all other factual support questions

    TODO: Call Gemini with structured output (Pydantic model) to classify the query.
    Hint: Prompt Gemini CLI —
        "Write classify_query for a LangGraph support agent. Use Gemini structured
        output with a Pydantic model that has fields: route (enum) and product_area
        (str | None). Pass the query and chat_history as context."
    """
    # Placeholder routing — replace this with Gemini-based classification
    state["route"] = "direct_answer"
    state["product_area"] = None
    return state


def direct_answer(state: SupportState) -> SupportState:
    """
    Run hybrid retrieval and generate a cited answer.

    Steps:
        1. Embed the query with the Gemini embedding API
        2. Run dense_retrieve() and bm25_retrieve()
        3. Fuse results with reciprocal_rank_fusion()
        4. Build a prompt from the top chunks and the chat history
        5. Call Gemini to generate an answer
        6. Populate state["answer"], state["sources"], state["retrieved_chunks"]

    TODO: Implement steps 1–6.
    Hint: Prompt Gemini CLI —
        "Implement the direct_answer node. It should embed the query, run hybrid
        retrieval using the retriever module, then call Gemini to generate an answer
        grounded in the retrieved chunks. Load the prompt template from
        prompts/direct_answer_prompt.txt."
    """
    state["answer"] = "TODO: implement direct_answer node"
    state["sources"] = []
    state["retrieved_chunks"] = []
    return state


def product_lookup(state: SupportState) -> SupportState:
    """
    Filter retrieval to state["product_area"], then generate a cited answer.

    Steps:
        1. Call search_by_product_area() with the detected product area
        2. Fall back to direct_answer logic if no results found
        3. Generate and return a cited answer

    TODO: Implement with product-area-filtered retrieval.
    Hint: Prompt Gemini CLI —
        "Implement product_lookup. It should call search_by_product_area, then
        follow the same generation logic as direct_answer. If search returns
        fewer than 2 results, fall back to unfiltered retrieval."
    """
    state["answer"] = "TODO: implement product_lookup node"
    state["sources"] = []
    state["retrieved_chunks"] = []
    return state


def escalation(state: SupportState) -> SupportState:
    """
    Create a support ticket and return an empathetic escalation message.

    Steps:
        1. Call create_support_ticket() with a summary of the issue
        2. Generate an empathetic message acknowledging the issue
        3. Populate state["answer"] and state["ticket_id"]

    TODO: Implement with create_support_ticket tool.
    Hint: Prompt Gemini CLI —
        "Implement the escalation node. It should summarise the user's issue
        using Gemini, call create_support_ticket, then generate an empathetic
        response that includes the ticket ID and sets expectations for follow-up."
    """
    state["answer"] = "TODO: implement escalation node"
    state["ticket_id"] = None
    state["tool_calls"].append("create_support_ticket")
    return state


# ── Routing logic ─────────────────────────────────────────────────────────────

def route_query(state: SupportState) -> Literal["direct_answer", "product_lookup", "escalation"]:
    return state.get("route", "direct_answer")


# ── Graph assembly ────────────────────────────────────────────────────────────

def build_agent():
    graph = StateGraph(SupportState)

    graph.add_node("classify_query",  classify_query)
    graph.add_node("direct_answer",   direct_answer)
    graph.add_node("product_lookup",  product_lookup)
    graph.add_node("escalation",      escalation)

    graph.set_entry_point("classify_query")

    graph.add_conditional_edges(
        "classify_query",
        route_query,
        {
            "direct_answer":  "direct_answer",
            "product_lookup": "product_lookup",
            "escalation":     "escalation",
        },
    )

    graph.add_edge("direct_answer",  END)
    graph.add_edge("product_lookup", END)
    graph.add_edge("escalation",     END)

    return graph.compile()


agent = build_agent()
