# AI Center of Excellence — Level 1 Capstone

> **Build a prototype AI application using everything you learned in Level 1.**
>
> This is a self-directed project. You will pick one of three projects, plan your architecture, and build a working prototype — using **Gemini CLI as your primary coding assistant**. A pre-configured environment with all required services, datasets, and libraries is provided.

| | |
|---|---|
| **Duration** | 4 days (self-paced) |
| **Coding Assistant** | Gemini CLI (primary) |
| **Environment** | GitHub Codespaces or local VS Code (Dev Container) |
| **UI Framework** | Streamlit |
| **Completion** | Self-assessment checklist + live demo |

---

## How to Use Gemini CLI

Gemini CLI is your primary tool for writing code in this capstone. The goal is to practice **prompting an AI to build** — the same skill that makes a professional AI engineer productive.

**Principles for effective use:**

- **Be specific about context.** Tell Gemini CLI which file you are working in, what already exists, and what you want to add next.
- **Work in small steps.** Ask it to implement one function or one feature at a time rather than the entire application at once.
- **Review before you run.** Read the generated code, understand what it does, and modify if needed. You are the architect — Gemini CLI is the implementer.
- **Iterate.** If the output isn't right, refine your prompt with more constraints or examples.
- **Use it for debugging too.** Paste error messages and ask Gemini CLI to diagnose and fix them.

**Example prompts to get you started:**

```
"I am building a RAG system using ChromaDB and Gemini.
Write a function that takes a list of text chunks and their metadata,
generates embeddings using the Gemini embedding API, and stores them in a ChromaDB collection called 'documents'."
```

```
"I have a Streamlit app with a chat interface.
Add a sidebar that shows the source documents retrieved for the last query,
with the document name, page number, and a relevance score."
```

```
"Write a LangGraph agent with two nodes: a retriever node that queries ChromaDB
and a generator node that calls Gemini. Add a conditional edge that routes
to a fallback response if retrieval returns fewer than 2 results."
```

---

## What's Pre-Provisioned in Your Environment

Your dev container comes ready with everything you need:

| Category | What's included |
|---|---|
| **API Keys** | Gemini API key pre-configured as environment variable |
| **Libraries** | `google-genai`, `langchain`, `langgraph`, `chromadb`, `streamlit`, `pandas`, `plotly`, `pypdf`, `python-docx`, `rank-bm25`, `sentence-transformers` |
| **Google Cloud SDK** | Pre-authenticated, project configured |
| **Datasets** | Project-specific datasets pre-loaded (see each project) |
| **Boilerplate** | Folder structure, Streamlit shell, ChromaDB initializer, Gemini client setup, evaluation logger |

### Boilerplate Folder Structure

```
capstone/
├── app.py                  # Streamlit entry point (shell provided)
├── config.py               # API keys, constants (pre-filled)
├── ingestion/
│   ├── loader.py           # Document/data loading utilities (provided)
│   └── chunker.py          # Basic chunking (provided)
├── retrieval/
│   └── retriever.py        # ChromaDB setup and query (shell provided)
├── agents/
│   └── agent.py            # LangGraph agent (shell provided)
├── evaluation/
│   └── evaluator.py        # Evaluation logger (shell provided)
├── data/                   # Pre-loaded project datasets
└── prompts/                # Prompt templates folder
```

---

## The Projects

Pick **one** project. All three require the same Level 1 skills and are equal in scope and difficulty.

---

## Project 1 — Customer Support Intelligence Bot

### Overview

Build an AI-powered support assistant for a real software product. Users ask support questions in natural language and receive accurate, cited answers. An agent routes queries between direct answers, product area lookups, and ticket escalation — just like a real enterprise support system.

### Dataset

Pre-loaded in `data/project1/`:

| File | Description |
|---|---|
| `support_docs/` | Support articles and FAQs from a public help center (Stripe) — ~500 articles in markdown format |
| `product_areas.json` | Product area taxonomy (Payments, Billing, APIs, etc.) |
| `sample_queries.csv` | 50 sample user queries with expected answer themes (for evaluation) |

### What to Build

**Core application:**
- Ingest support articles into ChromaDB with metadata (product area, article title, URL)
- RAG pipeline that retrieves relevant articles and generates cited answers
- Hybrid retrieval: dense embeddings + BM25 keyword search with reciprocal rank fusion
- Streamlit chat interface with source citations in the sidebar

**Agent:**
A LangGraph agent with the following routing logic:
- **Direct answer node** — handles clear, factual questions answered by the docs
- **Product lookup node** — routes ambiguous queries to a specific product area first, then retrieves
- **Escalation node** — triggers when confidence is low or the user explicitly asks to raise a ticket; returns a simulated ticket reference number

**Function calling tools:**
| Tool | What it does |
|---|---|
| `search_by_product_area(area, query)` | Filters ChromaDB retrieval to a specific product area |
| `create_support_ticket(issue_summary, severity)` | Simulates ticket creation, returns a mock ticket ID |
| `get_related_articles(article_id)` | Returns articles linked to a given article by metadata |

**Evaluation:**
- Faithfulness score: does the answer stay grounded in retrieved docs?
- Answer relevance score: does the answer address what was asked?
- Run evaluation on all 50 sample queries; log results for the monitoring app

### Streamlit UI Requirements

- Chat interface (multi-turn, conversation history preserved)
- Sidebar: source articles retrieved, with title, product area, and relevance score
- Escalation button visible when agent routes to escalation node
- Evaluation summary tab: shows average faithfulness and relevance scores

### Suggested Build Phases

**Phase 1 — Ingest & Retrieve**
Prompt Gemini CLI to build the ingestion pipeline (load markdown → chunk → embed → ChromaDB), then a basic retrieval function. Test it with 5 manual queries.

**Phase 2 — RAG + Hybrid Search**
Add BM25 retrieval alongside dense retrieval. Implement reciprocal rank fusion. Verify that hybrid outperforms dense-only on at least 3 test queries.

**Phase 3 — Agent & Tools**
Build the LangGraph agent with the three nodes and routing logic. Implement the three function calling tools. Test the full agent loop end-to-end.

**Phase 4 — UI + Evaluation**
Wire everything into the Streamlit app. Add the evaluation pipeline and run it against the 50 sample queries. Fix the top 3 failure cases you observe.

---

## Project 2 — Financial Document Analyst

### Overview

Build an AI research assistant that answers questions across multiple corporate annual reports. Users can ask factual questions, request comparisons across companies or years, and extract specific financial figures — all grounded in the actual documents with citations.

### Dataset

Pre-loaded in `data/project2/`:

| File | Description |
|---|---|
| `annual_reports/` | 10-K annual reports (PDF) for Apple, Google, Microsoft, Amazon, Meta — 2022 and 2023 |
| `company_metadata.json` | Company names, ticker symbols, fiscal year dates, report sections index |
| `eval_questions.csv` | 50 evaluation questions with known correct answers extracted from the documents |

### What to Build

**Core application:**
- Ingest all 10 PDFs into ChromaDB with rich metadata: company name, year, document section (Business Overview, Risk Factors, Financial Statements, etc.)
- RAG pipeline with metadata filtering — queries can be scoped to a company, year, or section
- Query rewriting: expand ambiguous queries (e.g., "how did Apple do last year?" → "Apple revenue and profit FY2023")
- Streamlit interface for Q&A with source citations

**Agent:**
A LangGraph research agent that handles multi-hop questions:
- **Planner node** — decomposes complex questions into sub-questions (e.g., "Compare Microsoft and Google cloud revenue in 2023" → two sub-queries)
- **Retriever node** — executes each sub-query with appropriate metadata filters
- **Synthesizer node** — combines sub-answers into a coherent, cited response
- **Extractor node** — activated for structured extraction requests (tables, specific numbers)

**Function calling tools:**
| Tool | What it does |
|---|---|
| `retrieve_section(company, year, section)` | Retrieves chunks from a specific section of a specific report |
| `extract_metric(company, year, metric_name)` | Extracts a specific financial figure using structured output |
| `compare_companies(companies, year, topic)` | Runs parallel retrieval across multiple companies and returns a comparison |

**Evaluation:**
- Faithfulness score: is the answer supported by the source document?
- Citation precision: does the cited passage actually contain the answer?
- Run evaluation on all 50 questions; log results for the monitoring app

### Streamlit UI Requirements

- Q&A interface with multi-turn conversation
- Sidebar: source document, company, year, section, and page reference for each retrieved chunk
- Structured extraction view: when a metric is extracted, show it in a formatted card with the source passage
- Comparison view: side-by-side table when comparing multiple companies
- Evaluation summary tab: faithfulness and citation precision scores

### Suggested Build Phases

**Phase 1 — Ingest & Retrieve**
Prompt Gemini CLI to build a PDF ingestion pipeline that preserves company/year/section metadata. Test metadata-filtered retrieval with 5 manual queries.

**Phase 2 — Query Rewriting + Advanced Retrieval**
Add a query rewriting step using Gemini. Test that rewritten queries outperform raw queries on at least 3 ambiguous examples.

**Phase 3 — Agent & Tools**
Build the planner → retriever → synthesizer agent. Implement the three tools. Test multi-hop questions end-to-end (e.g., "Which company had higher operating margin in 2023, Apple or Microsoft?").

**Phase 4 — UI + Evaluation**
Wire into Streamlit with comparison and extraction views. Run the evaluation pipeline on the 50 questions. Identify and fix the most common failure pattern.

---

## Project 3 — Business Insights Analyst

### Overview

Build a natural language analytics assistant over structured business data. Users ask plain-English business questions and receive data-backed answers with auto-generated charts and summary tables — no SQL or Python required from the user's side.

### Dataset

Pre-loaded in `data/project3/`:

| File | Description |
|---|---|
| `global_superstore.csv` | 51,000 retail orders across regions, categories, sub-categories, and time (2019–2022) — includes sales, profit, quantity, discount, shipping details |
| `data_dictionary.md` | Column definitions, data types, valid values |
| `business_questions.csv` | 50 sample business questions with expected answer themes (for evaluation) |

**Key columns:** `Order Date`, `Region`, `Country`, `Category`, `Sub-Category`, `Sales`, `Profit`, `Quantity`, `Discount`, `Ship Mode`, `Customer Segment`

### What to Build

**Core application:**
- Ingest `data_dictionary.md` into ChromaDB so the agent understands the schema
- RAG pipeline for schema/metadata questions ("what regions are available?", "what does discount mean?")
- Data query engine: agent translates natural language → pandas operations → results
- Streamlit dashboard with natural language Q&A and auto-rendered charts

**Agent:**
A LangGraph analyst agent:
- **Planner node** — interprets the business question and decides what data operations are needed
- **Query node** — calls data tools to execute operations
- **Visualizer node** — determines the right chart type and generates it (bar, line, pie, scatter)
- **Narrator node** — generates a plain-English summary of the findings with key numbers highlighted

**Function calling tools:**
| Tool | What it does |
|---|---|
| `filter_data(filters: dict)` | Filters the dataset by region, category, date range, segment, etc. |
| `aggregate(group_by, metric, agg_func)` | Groups data and computes sum/mean/count/max on a metric |
| `calculate_growth(metric, period_col, period_a, period_b)` | Calculates period-over-period growth for a metric |
| `top_n(group_by, metric, n, ascending)` | Returns top or bottom N items ranked by a metric |
| `generate_chart(data, chart_type, x, y, title)` | Generates a Plotly chart and returns it for Streamlit rendering |

**Evaluation:**
- Answer accuracy: does the numeric answer match the ground truth calculated directly from the data?
- Faithfulness: is the narrative grounded in the actual query results?
- Run evaluation on all 50 business questions; log results for the monitoring app

### Streamlit UI Requirements

- Natural language input with multi-turn conversation history
- Auto-rendered charts below each answer (Plotly)
- Data table view: show the underlying aggregated data that produced the answer
- Question suggestions: 5 pre-built example questions to help users get started
- Evaluation summary tab: accuracy and faithfulness scores across all 50 test questions

### Suggested Build Phases

**Phase 1 — Data Exploration & Schema RAG**
Load the dataset, ingest the data dictionary into ChromaDB. Prompt Gemini CLI to build simple filter and aggregate tools. Test with 5 basic questions manually.

**Phase 2 — Query Engine**
Implement all 5 tools. Build the planner → query → narrator agent flow (skip visualizer for now). Test end-to-end with 10 business questions.

**Phase 3 — Visualizer + Agent Polish**
Add the visualizer node. Test that the agent picks the right chart type for different question patterns (trends → line, comparisons → bar, proportions → pie). Handle edge cases (no data returned, ambiguous filters).

**Phase 4 — UI + Evaluation**
Build the full Streamlit dashboard. Run the evaluation pipeline on all 50 questions. Identify the most common query failure type and fix it.

---

## Required Features Checklist

Use this to self-assess before your demo. All items are required.

### Ingestion & Retrieval
- [ ] Data/documents ingested into ChromaDB with metadata
- [ ] Basic dense retrieval working (semantic search)
- [ ] At least one advanced retrieval technique applied (hybrid search, query rewriting, or metadata filtering)

### Agent & Tools
- [ ] LangGraph agent with at least 2 nodes and conditional routing
- [ ] At least 2 function calling tools implemented and used by the agent
- [ ] Agent handles at least one edge case gracefully (low confidence, no results, ambiguous query)

### Evaluation
- [ ] Evaluation pipeline runs against the provided sample questions
- [ ] At least 2 evaluation metrics computed and logged
- [ ] Results visible in the Streamlit UI evaluation tab

### Application
- [ ] Streamlit UI is functional and demonstrates the core use case
- [ ] Multi-turn conversation history preserved
- [ ] Source citations or data provenance shown for every answer
- [ ] Application runs end-to-end without crashing on the sample queries

### Code Quality
- [ ] Prompts are in the `prompts/` folder as reusable templates (not hardcoded strings)
- [ ] No API keys hardcoded in source files
- [ ] Code is readable — Gemini CLI used to add docstrings to key functions

---

## Demo Guide

Your demo should be **10 minutes** and cover:

1. **Show the running app** (2 min) — walk through the UI, explain what it does and why
2. **Live queries** (5 min) — run 3–4 queries that show off different capabilities:
   - One simple factual question
   - One that triggers the agent's routing/planning logic
   - One that shows a function calling tool in action
   - One that shows a failure or edge case you handled
3. **Evaluation results** (2 min) — show the evaluation tab, explain what the scores mean
4. **What you'd improve** (1 min) — one thing you'd build next if you had more time

**Tip:** Rehearse your 3–4 demo queries in advance so they produce clean outputs during the demo.

---

## Tips for Working with Gemini CLI

| Situation | What to do |
|---|---|
| Gemini CLI generates code that doesn't run | Paste the full error message back and ask it to fix |
| Generated code works but produces wrong output | Show it an example input and the wrong vs expected output |
| Unsure how to structure a feature | Ask Gemini CLI to propose 2–3 approaches and explain trade-offs |
| Stuck on LangGraph wiring | Ask it to draw the graph as a comment/diagram first, then implement |
| Evaluation scores are low | Ask Gemini CLI to analyze 3 failure cases and suggest prompt improvements |
| Streamlit layout looks cluttered | Ask it to redesign the layout with a specific UX goal in mind |
