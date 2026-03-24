# AI Center of Excellence — Learning Curriculum

> A structured, three-level learning program that takes learners from zero AI knowledge to production-grade GenAI engineering and model fine-tuning. All hands-on work uses **Gemini models, Google Cloud services, LangChain, LangGraph, ChromaDB**, and other open-source tools.

---

## Program Structure at a Glance

| Level | Target Audience | Format | Duration | Outcome |
|-------|----------------|--------|----------|---------|
| **Level 1 — Beginner** | No prior AI knowledge | 14-day intensive (10 learning + 4 capstone) | ~14 days | Clear entry-level GenAI Engineer interviews |
| **Level 2 — Intermediate** | Level 1 graduates | Topic-based modules | Self-paced (~4 weeks) | Build & deploy production-quality AI systems |
| **Level 3 — Advanced** | Level 2 graduates | Topic-based modules | Self-paced (~3 weeks) | Fine-tune models (SFT, RLHF, DPO) |

---

---

# 🟢 Level 1 — Beginner: Foundations of Generative AI

> **Goal:** Take someone with basic Python knowledge and zero AI background to a point where they understand LLMs, can engineer prompts expertly, build RAG systems, evaluate AI outputs, work with agents, and confidently clear entry-level GenAI engineer roles.

> **Format:** Day-by-day intensive curriculum. Each day includes interactive Jupyter notebooks with pre-written code, guided walkthroughs, and **inline coding exercises** embedded directly in the notebooks. Days 1–10 cover all core topics; Days 11–14 are a hands-on capstone project built with AI-assisted coding.

---

### Day 1 — Introduction to AI & Large Language Models

**Learning Objectives**
- Understand what Generative AI is and where it fits in the AI landscape
- Learn the conceptual basics of Transformer architecture
- Understand tokens, context windows, and how LLMs generate text
- Set up the development environment (Python, Gemini API, Jupyter)

**Notebooks**
| # | Notebook | Description | Est. Time |
|---|----------|-------------|-----------|
| 1 | `01_What_is_GenAI.ipynb` | AI vs ML vs GenAI, real-world applications, landscape overview | 30 min |
| 2 | `02_How_LLMs_Work.ipynb` | Transformers (conceptual), attention, tokens, context windows | 30 min |
| 3 | `03_Your_First_LLM_Call.ipynb` | Set up Gemini API, make first API call, explore parameters (temperature, top-k, top-p) | 45 min |

**Key Concepts:** Generative AI, Transformers, tokens, context windows, API keys, model parameters

---

### Day 2 — Prompt Engineering Fundamentals

**Learning Objectives**
- Master core prompting techniques: zero-shot, few-shot, chain-of-thought
- Understand structured vs unstructured prompts
- Learn role prompting and system instructions

**Notebooks**
| # | Notebook | Description | Est. Time |
|---|----------|-------------|-----------|
| 1 | `01_Zero_Shot_Prompting.ipynb` | Direct instruction prompting without examples | 20 min |
| 2 | `02_Few_Shot_Prompting.ipynb` | Providing examples, enforcing output formats (JSON, tables) | 25 min |
| 3 | `03_Chain_of_Thought_Prompting.ipynb` | Step-by-step reasoning, math problems, logical tasks | 25 min |
| 4 | `04_Role_and_System_Prompting.ipynb` | Personas, system instructions, tone control | 20 min |
| 5 | `05_Prompt_Design_Patterns.ipynb` | Templates, delimiters, output schemas, production prompt patterns | 30 min |

**Key Concepts:** Zero-shot, few-shot, CoT, role prompting, system instructions, prompt templates

---

### Day 3 — Advanced Prompt Engineering & Structured Output

**Learning Objectives**
- Apply advanced prompting: self-consistency, tree-of-thought, ReAct pattern
- Generate structured outputs (JSON mode, function-calling schemas)
- Build a reusable prompt library for common tasks

**Notebooks**
| # | Notebook | Description | Est. Time |
|---|----------|-------------|-----------|
| 1 | `01_Advanced_Prompting_Techniques.ipynb` | Self-consistency, tree-of-thought, iterative refinement | 30 min |
| 2 | `02_Structured_Output_Generation.ipynb` | JSON mode, schema enforcement, Pydantic + Gemini | 30 min |
| 3 | `03_ReAct_Prompting_Pattern.ipynb` | Reason + Act pattern, tool-use through prompting | 25 min |
| 4 | `04_Building_a_Prompt_Library.ipynb` | Categorization, summarization, extraction, QA prompt templates | 30 min |

**Key Concepts:** Self-consistency, ToT, ReAct, structured generation, JSON mode, prompt libraries

---

### Day 4 — Hallucinations, Grounding & Generation Control

**Learning Objectives**
- Understand why LLMs hallucinate and categorize hallucination types
- Apply grounding techniques to reduce hallucinations
- Control generation with temperature, top-k, top-p, and safety settings

**Notebooks**
| # | Notebook | Description | Est. Time |
|---|----------|-------------|-----------|
| 1 | `01_Understanding_Hallucinations.ipynb` | Types of hallucinations, why they happen, real examples | 25 min |
| 2 | `02_Grounding_Techniques.ipynb` | Prompt grounding, citation enforcement, fact-checking patterns | 30 min |
| 3 | `03_Generation_Control_Parameters.ipynb` | Temperature, top-k, top-p experiments, deterministic outputs | 25 min |
| 4 | `04_Safety_Settings_and_Guardrails.ipynb` | Content safety filters, input validation, output sanitization | 20 min |

**Key Concepts:** Hallucination types, grounding, temperature, sampling strategies, safety settings

---

### Day 5 — Embeddings & Semantic Search

**Learning Objectives**
- Understand what embeddings are and how they capture meaning
- Generate embeddings using Gemini embedding models
- Build a semantic search system using cosine similarity

**Notebooks**
| # | Notebook | Description | Est. Time |
|---|----------|-------------|-----------|
| 1 | `01_What_are_Embeddings.ipynb` | Vector representations of text, embedding models, dimensionality | 25 min |
| 2 | `02_Generating_Embeddings_with_Gemini.ipynb` | Gemini embedding API, batch embedding, task types | 30 min |
| 3 | `03_Similarity_Search.ipynb` | Cosine similarity, dot product, building a basic search engine | 30 min |
| 4 | `04_Semantic_Search_Application.ipynb` | End-to-end semantic search over a document corpus | 30 min |

**Key Concepts:** Embeddings, vector representations, cosine similarity, semantic search, Gemini embedding API

---

### Day 6 — Vector Databases & Document Processing

**Learning Objectives**
- Understand vector database fundamentals (indexing, ANN search)
- Set up and use ChromaDB for persistent vector storage
- Build a document processing pipeline: load → chunk → embed → store

**Notebooks**
| # | Notebook | Description | Est. Time |
|---|----------|-------------|-----------|
| 1 | `01_Vector_Database_Fundamentals.ipynb` | What are vector DBs, HNSW indexing, why they matter | 25 min |
| 2 | `02_Getting_Started_with_ChromaDB.ipynb` | Installation, collections, CRUD operations, metadata filtering | 30 min |
| 3 | `03_Document_Chunking_Strategies.ipynb` | Fixed-size, recursive, semantic chunking, overlap strategies | 30 min |
| 4 | `04_Document_Processing_Pipeline.ipynb` | PDF/text loading → chunking → embedding → ChromaDB storage | 35 min |

**Key Concepts:** Vector databases, ChromaDB, ANN search, document chunking, metadata filtering

---

### Day 7 — Retrieval Augmented Generation (RAG)

**Learning Objectives**
- Understand the RAG architecture and why it solves hallucination problems
- Build a complete RAG system from scratch using Gemini + ChromaDB
- Compare vanilla LLM answers vs RAG-grounded answers

**Notebooks**
| # | Notebook | Description | Est. Time |
|---|----------|-------------|-----------|
| 1 | `01_RAG_Architecture_Overview.ipynb` | Retriever + Generator pattern, when to use RAG, architecture diagram | 25 min |
| 2 | `02_Building_a_Basic_RAG_System.ipynb` | End-to-end RAG: query → retrieve → augment → generate | 40 min |
| 3 | `03_RAG_with_LangChain.ipynb` | LangChain document loaders, retrievers, chains for RAG | 35 min |
| 4 | `04_RAG_vs_Vanilla_LLM.ipynb` | Side-by-side comparison, grounding analysis, when RAG helps | 20 min |

**Key Concepts:** RAG architecture, retriever-generator pattern, LangChain, context augmentation

---

### Day 8 — Advanced RAG Techniques

**Learning Objectives**
- Implement hybrid retrieval (BM25 + dense embeddings)
- Apply query transformation techniques (rewriting, HyDE, multi-query)
- Use re-ranking models to improve retrieval precision

**Notebooks**
| # | Notebook | Description | Est. Time |
|---|----------|-------------|-----------|
| 1 | `01_Hybrid_Retrieval.ipynb` | BM25 + dense retrieval, reciprocal rank fusion | 35 min |
| 2 | `02_Query_Transformation.ipynb` | Query rewriting, HyDE (Hypothetical Document Embeddings), multi-query | 30 min |
| 3 | `03_Reranking_Models.ipynb` | Cross-encoder reranking, Cohere Rerank, improving precision | 30 min |
| 4 | `04_Context_Compression_and_Filtering.ipynb` | LLM-based compression, relevant context extraction | 25 min |

**Key Concepts:** Hybrid retrieval, BM25, query rewriting, HyDE, re-ranking, context compression

---

### Day 9 — Evaluation Frameworks for LLM & RAG

**Learning Objectives**
- Build evaluation pipelines for both LLM outputs and RAG systems
- Create golden datasets for systematic testing
- Use LLM-as-judge and RAGAS-style evaluation metrics

**Notebooks**
| # | Notebook | Description | Est. Time |
|---|----------|-------------|-----------|
| 1 | `01_Why_Evaluation_Matters.ipynb` | Evaluation mindset, offline vs online eval, golden datasets | 20 min |
| 2 | `02_LLM_Output_Evaluation.ipynb` | Faithfulness, relevance, coherence scoring with LLM-as-judge | 30 min |
| 3 | `03_RAG_Retrieval_Metrics.ipynb` | Precision@K, Recall@K, MRR, retrieval quality measurement | 30 min |
| 4 | `04_Building_an_Evaluation_Pipeline.ipynb` | End-to-end eval: dataset creation → metrics → comparison dashboard | 35 min |

**Key Concepts:** Golden datasets, LLM-as-judge, faithfulness, relevance, RAGAS metrics, Precision@K

---

### Day 10 — Agents, Function Calling & Tool Integration

**Learning Objectives**
- Understand function calling in Gemini models
- Build tools that LLMs can invoke (search, calculator, database lookup)
- Understand agentic AI architecture: planning, reasoning, acting
- Build a ReAct agent with LangGraph and tool use

**Notebooks**
| # | Notebook | Description | Est. Time |
|---|----------|-------------|-----------|
| 1 | `01_Function_Calling_Basics.ipynb` | Gemini function calling, declaring tools, handling responses | 30 min |
| 2 | `02_Building_Custom_Tools.ipynb` | Web search, calculator, DB lookup, API wrapper tools | 30 min |
| 3 | `03_Introduction_to_Agents.ipynb` | Agent loop (perceive → reason → act), agent types, ReAct pattern | 30 min |
| 4 | `04_Building_Agents_with_LangGraph.ipynb` | LangGraph basics: nodes, edges, state, conditional routing | 40 min |
| 5 | `05_Multi_Agent_RAG_System.ipynb` | Retriever agent + Generator agent + Critic agent collaboration | 35 min |

**Key Concepts:** Function calling, tool declaration, agentic AI, LangGraph, ReAct, multi-agent systems

---

---

### Days 11–14 — Capstone Project: Build a Real AI Application

> **Goal:** Apply everything from Days 1–10 to build a complete, working AI application from scratch. Learners will use **AI-assisted coding** (e.g., Gemini in IDE, Copilot) to plan, implement, test, and present their project.

**Project: AI-Powered Knowledge Assistant**

Build an end-to-end AI knowledge assistant for a domain of your choice (e.g., company docs, legal corpus, technical manuals). The application should demonstrate mastery of prompt engineering, RAG, evaluation, and agentic patterns.

---

#### Day 11 — Planning & Architecture

- Define project scope and choose a document corpus
- Design system architecture (draw a diagram with AI assistance)
- Set up project structure, dependencies, and configuration
- Plan the document ingestion pipeline
- **Deliverable:** Architecture document + project skeleton

#### Day 12 — Core Implementation

- Build document processing pipeline (load → chunk → embed → ChromaDB)
- Implement RAG-powered Q&A with source citations
- Add advanced retrieval (hybrid search, reranking, or query rewriting)
- Integrate at least one tool via function calling
- **Deliverable:** Working RAG system with tool integration

#### Day 13 — Agents, Evaluation & Polish

- Add an agentic layer (e.g., Critic agent for hallucination detection, Router agent for query classification)
- Build an evaluation pipeline (golden dataset + metrics)
- Add conversation memory and multi-turn support
- Polish the user interface (Gradio, Streamlit, or CLI)
- **Deliverable:** Multi-agent system with evaluation dashboard

#### Day 14 — Demo Day

- Final testing and bug fixes
- Prepare a 10-minute demo presentation
- Present to peers and facilitators
- Peer review and feedback session
- **Deliverable:** Live demo + presentation + code walkthrough

---

**Required Features Checklist:**
- [ ] Document ingestion pipeline (PDF/text → ChromaDB)
- [ ] RAG-powered Q&A with source citations
- [ ] At least one advanced retrieval technique
- [ ] Function calling / tool integration
- [ ] At least one agent (retriever, critic, or router)
- [ ] Evaluation metrics (faithfulness, relevance, or retrieval precision)
- [ ] Clean, documented code
- [ ] Working demo

---

---

# 🟡 Level 2 — Intermediate: Production-Quality AI Systems

> **Goal:** Enable learners to confidently build, deploy, and maintain production-grade AI applications. Covers engineering best practices, scalability, observability, security, and real-world deployment patterns.

> **Prerequisite:** Completion of Level 1 or equivalent knowledge.

> **Format:** Topic-based modules (self-paced). Each module has reading material, notebooks, and a mini-project.

---

### Module 1 — Production LLM Application Architecture

- API design patterns for AI services (REST, gRPC, streaming)
- FastAPI for AI applications
- Request/response schemas, input validation, error handling
- Streaming responses with Server-Sent Events (SSE)
- **Mini-Project:** Build a production RAG API with FastAPI

---

### Module 2 — LangChain & LangGraph Deep Dive

- LangChain Expression Language (LCEL) — chains, runnables, composition
- Advanced LangGraph: cycles, persistence, human-in-the-loop, breakpoints
- Memory systems: conversation buffers, summary memory, entity memory
- Building complex conversational AI with state management
- **Mini-Project:** Multi-turn conversational RAG agent with LangGraph

---

### Module 3 — Advanced Document Processing & Ingestion

- Multi-format document parsing (PDF, DOCX, HTML, images with OCR)
- Advanced chunking: semantic chunking, agentic chunking, parent-child
- Document metadata extraction and enrichment
- Handling tables, images, and structured data in documents
- Incremental indexing and document versioning
- **Mini-Project:** Production document ingestion pipeline with multi-format support

---

### Module 4 — Advanced Retrieval & Search Systems

- Embedding model selection and benchmarking
- Advanced vector database features (HNSW tuning, filtering, hybrid indexes)
- Knowledge graphs + vector search hybrid approaches
- Multi-index retrieval strategies
- Embedding drift detection and re-indexing strategies
- **Mini-Project:** Multi-index hybrid search engine with metadata-aware retrieval

---

### Module 5 — Prompt Security & Guardrails

- Prompt injection attacks: direct, indirect, jailbreaks
- Defense strategies: input sanitization, output filtering, constitutional AI
- Building guardrail pipelines (input → LLM → output validation)
- Content moderation and safety classifiers
- Rate limiting and abuse prevention
- **Mini-Project:** Hardened LLM endpoint with multi-layer guardrails

---

### Module 6 — Observability, Logging & Monitoring

- LLM observability: traces, spans, token usage tracking
- Tools: LangSmith, Google Cloud Logging, custom dashboards
- Latency profiling and bottleneck identification
- Cost monitoring and optimization strategies
- Alerting on quality degradation
- **Mini-Project:** Instrumented RAG system with LangSmith tracing and cost dashboard

---

### Module 7 — Deployment & Scaling on Google Cloud

- Containerization with Docker
- Deploying to Google Cloud Run
- Vertex AI for managed model serving
- Auto-scaling, load balancing, and caching strategies
- CI/CD pipelines for AI applications
- **Mini-Project:** Deploy a RAG application to Cloud Run with CI/CD

---

### Module 8 — MCP (Model Context Protocol) & Google ADK

- MCP architecture: servers, clients, tool discovery
- Building MCP servers for custom tools
- Google Agent Development Kit (ADK) fundamentals
- Agent orchestration with ADK: sequential, parallel, loop agents
- Connecting agents to enterprise systems via MCP
- **Mini-Project:** Build a tool-rich agent using ADK with MCP-based integrations

---

### Module 9 — Testing & Quality Assurance for AI Systems

- Unit testing LLM applications (mocking, deterministic tests)
- Integration testing for RAG pipelines
- Regression testing with golden datasets
- A/B testing and canary deployments for LLM changes
- Continuous evaluation pipelines
- **Mini-Project:** Full test suite for a RAG application with CI integration

---

### Module 10 — Capstone: Enterprise AI System

**Build a production-grade multi-agent enterprise assistant:**
- Multi-format document ingestion pipeline
- Hybrid retrieval with reranking
- Multi-agent orchestration (LangGraph)
- FastAPI deployment with streaming
- Observability, guardrails, and evaluation dashboard
- Deployed on Google Cloud

---

---

# 🔴 Level 3 — Advanced: Model Fine-Tuning & Customization

> **Goal:** Master model customization techniques — from supervised fine-tuning to RLHF — enabling learners to adapt foundation models for domain-specific applications.

> **Prerequisite:** Completion of Level 2 or equivalent production AI experience.

> **Format:** Topic-based modules (self-paced). Each module combines theory, code, and experimentation.

---

### Module 1 — Foundations of Fine-Tuning

- Why fine-tune: when prompting isn't enough
- Transfer learning concepts for LLMs
- Fine-tuning vs prompt engineering vs RAG: decision framework
- Data requirements, formats, and quality considerations
- Gemini model fine-tuning on Vertex AI (overview)

---

### Module 2 — Data Preparation for Fine-Tuning

- Dataset curation: sourcing, cleaning, deduplication
- Instruction-response dataset formats (Alpaca, ShareGPT, JSONL)
- Data quality filtering and toxicity removal
- Synthetic data generation using LLMs
- Train/validation/test split strategies for LLMs
- **Mini-Project:** Build a high-quality instruction dataset for a domain-specific task

---

### Module 3 — Supervised Fine-Tuning (SFT)

- Full fine-tuning vs parameter-efficient methods
- LoRA (Low-Rank Adaptation) — theory and practice
- QLoRA — quantized fine-tuning for resource efficiency
- Fine-tuning Gemini models on Vertex AI
- Fine-tuning open-source models (Hugging Face Transformers + PEFT)
- Hyperparameter tuning: learning rate, epochs, batch size, rank
- **Mini-Project:** Fine-tune a model for domain-specific Q&A

---

### Module 4 — Reinforcement Learning from Human Feedback (RLHF)

- RLHF pipeline: SFT → Reward Model → PPO
- Reward model training and human preference data
- Proximal Policy Optimization (PPO) for LLMs
- Practical challenges: reward hacking, mode collapse
- Tools: TRL (Transformer Reinforcement Learning) library

---

### Module 5 — Direct Preference Optimization (DPO) & Alternatives

- DPO: theory and why it simplifies RLHF
- ORPO, SimPO, KTO — other alignment techniques
- Comparing RLHF vs DPO in practice
- When to use which alignment method
- **Mini-Project:** Align a model using DPO on preference data

---

### Module 6 — Evaluation of Fine-Tuned Models

- Benchmarking fine-tuned models (perplexity, task-specific metrics)
- Human evaluation protocols
- Automated evaluation with LLM judges
- Overfitting detection and catastrophic forgetting
- A/B testing fine-tuned vs base models in production

---

### Module 7 — Model Merging, Quantization & Deployment

- Model quantization: GPTQ, AWQ, GGUF for efficient inference
- Model merging techniques (task arithmetic, TIES, DARE)
- Serving fine-tuned models: vLLM, TGI, Vertex AI endpoints
- Cost-performance trade-offs in production

---

### Module 8 — Capstone: Domain-Specific Fine-Tuned Model

**End-to-end fine-tuning project:**
- Curate a domain-specific dataset
- Fine-tune using SFT + LoRA
- Align with DPO on preference data
- Evaluate against base model on domain benchmarks
- Deploy the fine-tuned model to a serving endpoint

---

---

# Appendix

## Tech Stack Summary

| Category | Tools |
|----------|-------|
| **LLM Provider** | Google Gemini (via `google-genai` SDK) |
| **Cloud Platform** | Google Cloud (Vertex AI, Cloud Run, Cloud Logging) |
| **Orchestration** | LangChain, LangGraph |
| **Vector Database** | ChromaDB |
| **Agent Framework** | Google ADK, LangGraph |
| **Evaluation** | Custom pipelines, LLM-as-judge |
| **API Framework** | FastAPI |
| **Fine-Tuning** | Vertex AI, Hugging Face (Transformers, PEFT, TRL) |
| **Protocols** | MCP (Model Context Protocol) |

## Progression Path

```
Level 1 (Beginner)                Level 2 (Intermediate)         Level 3 (Advanced)
──────────────────────           ──────────────────────         ─────────────────────
10 learning days          ───►   10 self-paced modules   ───►  8 self-paced modules
+ 4-day capstone project         + Enterprise Capstone          + Fine-Tuning Capstone
```
