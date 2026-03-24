# AI Center of Excellence — Level 2 Curriculum

> **Level 2 — Intermediate: Production-Quality AI Systems**
>
> Builds on Level 1 foundations to enable learners to design, deploy, and maintain production-grade AI applications. Covers engineering best practices, scalability, observability, security, and real-world deployment patterns using **Gemini models, Google Cloud, LangChain, LangGraph, FastAPI, and Google ADK**.

| | |
|---|---|
| **Target Audience** | Level 1 graduates or learners with equivalent foundational knowledge |
| **Format** | Topic-based modules (self-paced) |
| **Duration** | ~4 weeks |
| **Outcome** | Build, deploy, and maintain production-grade AI systems on Google Cloud |

---

## Module Overview

| # | Module | Focus Area |
|---|--------|------------|
| 1 | Production LLM Application Architecture | FastAPI, streaming, API design |
| 2 | LangChain & LangGraph Deep Dive | Orchestration, memory, state management |
| 3 | Advanced Document Processing & Ingestion | Multi-format parsing, chunking, indexing |
| 4 | Advanced Retrieval & Search Systems | Hybrid search, multi-index, vector DB tuning |
| 5 | Prompt Security & Guardrails | Injection defense, content moderation, compliance |
| 6 | Caching, Cost Optimization & Model Routing | Semantic caching, model tiering, token economics |
| 7 | Async Processing & Background Jobs | Queuing, long-running pipelines, Cloud Tasks |
| 8 | Multi-modal AI Applications | Images, documents with visuals, Gemini vision |
| 9 | Observability, Logging & Monitoring | Tracing, cost dashboards, quality alerting |
| 10 | Deployment & Scaling on Google Cloud | Docker, Cloud Run, Vertex AI, CI/CD |
| 11 | Agentic Systems with Google ADK & MCP | ADK orchestration, MCP integrations |
| 12 | Testing & Quality Assurance | Unit, integration, regression, A/B testing |
| 13 | Capstone: Enterprise AI System | End-to-end production build |

---

## Modules

---

### Module 1 — Production LLM Application Architecture

**Learning Objectives**
- Design robust API layers for AI services
- Build production-ready AI endpoints with FastAPI
- Implement streaming responses and handle errors gracefully
- Apply resilience patterns: retries, fallbacks, circuit breakers

**Topics**
- API design patterns for AI services (REST, gRPC, streaming)
- FastAPI for AI applications: request/response schemas, input validation
- Streaming responses with Server-Sent Events (SSE)
- Error handling: LLM API errors, timeouts, partial responses
- Resilience patterns: exponential backoff, fallback models, circuit breakers
- Rate limit handling and quota management

**Mini-Project:** Production RAG API with FastAPI — streaming responses, input validation, retry logic, and graceful fallback to a secondary model

---

### Module 2 — LangChain & LangGraph Deep Dive

**Learning Objectives**
- Compose complex chains using LangChain Expression Language (LCEL)
- Build stateful, cyclic agent workflows with LangGraph
- Implement production-grade memory systems for multi-turn conversations

**Topics**
- LangChain Expression Language (LCEL): chains, runnables, composition patterns
- Advanced LangGraph: cycles, persistence, breakpoints, human-in-the-loop
- Memory systems: conversation buffers, summary memory, entity memory
- Persistent memory: user-level vs session-level state
- Building complex conversational AI with state management

**Mini-Project:** Multi-turn conversational RAG agent with LangGraph — persistent memory, human-in-the-loop approval step, and session management

---

### Module 3 — Advanced Document Processing & Ingestion

**Learning Objectives**
- Parse diverse document formats including tables and embedded images
- Apply advanced chunking strategies for production pipelines
- Build incremental, versioned ingestion pipelines

**Topics**
- Multi-format document parsing: PDF, DOCX, HTML, images with OCR
- Advanced chunking: semantic chunking, agentic chunking, parent-child hierarchies
- Document metadata extraction and enrichment
- Handling tables, images, and structured data embedded in documents
- Incremental indexing and document versioning
- Context window management: strategies for documents exceeding context limits, map-reduce patterns

**Mini-Project:** Production document ingestion pipeline supporting PDF, DOCX, and HTML with incremental re-indexing and metadata-aware retrieval

---

### Module 4 — Advanced Retrieval & Search Systems

**Learning Objectives**
- Select and benchmark embedding models for specific domains
- Tune vector database performance for production workloads
- Build multi-index retrieval strategies for diverse data sources

**Topics**
- Embedding model selection and benchmarking (MTEB leaderboard, domain-specific evaluation)
- Advanced ChromaDB and vector DB features: HNSW tuning, filtering, hybrid indexes
- Multi-index retrieval strategies (separate indexes per document type or domain)
- Knowledge graphs as a complement to vector search (conceptual + integration patterns)
- Embedding cache invalidation and re-indexing strategies

**Mini-Project:** Multi-index hybrid search engine with metadata-aware retrieval, embedding model benchmarking report, and automated re-indexing trigger

---

### Module 5 — Prompt Security, Guardrails & Data Privacy

**Learning Objectives**
- Identify and defend against prompt injection and jailbreak attacks
- Build multi-layer guardrail pipelines for production LLM endpoints
- Implement PII detection, redaction, and compliance controls

**Topics**
- Prompt injection attacks: direct, indirect, jailbreaks — examples and taxonomy
- Defense strategies: input sanitization, output filtering, constitutional AI
- Building guardrail pipelines: input → LLM → output validation
- Content moderation and safety classifiers
- PII detection and redaction before sending data to external LLMs
- Data residency and compliance considerations (GDPR, enterprise policies)
- Rate limiting and abuse prevention
- Audit logging for compliance

**Mini-Project:** Hardened LLM endpoint with multi-layer guardrails — prompt injection detection, PII redaction, output safety filtering, and audit log

---

### Module 6 — Caching, Cost Optimization & Model Routing

**Learning Objectives**
- Implement semantic caching to reduce redundant LLM calls at scale
- Apply model tiering to optimize cost vs quality trade-offs
- Track and control token spend across features and users

**Topics**
- Semantic caching: serving cached responses for similar queries (Redis + embedding similarity)
- Prompt caching: using Gemini's native prompt caching for repeated context
- Model tiering: routing simple queries to smaller/cheaper models (e.g., Flash vs Pro)
- LLM router design: rules-based and classifier-based query routing
- Token budgeting: per-request limits, per-user quotas, per-feature cost tracking
- Cost dashboards and spend alerting
- Measuring and improving cost-per-query at scale

**Mini-Project:** Cost-optimized RAG service with semantic caching, Gemini Flash/Pro routing based on query complexity, and a real-time cost tracking dashboard

---

### Module 7 — Async Processing & Background Jobs

**Learning Objectives**
- Design async AI pipelines for long-running tasks
- Use Google Cloud queuing primitives to decouple ingestion from serving
- Build reliable background workers with observability

**Topics**
- Why synchronous APIs aren't enough: long-running ingestion, batch evaluation, bulk generation
- Task queue patterns: Cloud Tasks and Pub/Sub for AI pipelines
- Async FastAPI endpoints: accepting jobs, returning job IDs, polling for results
- Background workers: document ingestion workers, batch embedding jobs
- Webhook patterns for async AI workflows
- Dead letter queues, retries, and failure handling
- Monitoring background job health and throughput

**Mini-Project:** Async document ingestion service — REST endpoint accepts upload, queues processing via Cloud Tasks, background worker chunks/embeds/indexes, status polling API

---

### Module 8 — Multi-modal AI Applications

**Learning Objectives**
- Process and reason over images, diagrams, and visually-rich documents
- Build pipelines that handle mixed text and visual content
- Leverage Gemini's native multi-modal capabilities in production

**Topics**
- Gemini's multi-modal capabilities: text + image + audio inputs
- Extracting structured data from images and scanned documents
- Processing PDFs with embedded images, charts, and tables (vision-based extraction)
- Multi-modal RAG: indexing and retrieving from documents with visual content
- Image grounding: referencing specific visual elements in generated responses
- Handling audio inputs: transcription and reasoning over spoken content
- Production considerations: latency, storage, and cost for multi-modal workloads

**Mini-Project:** Multi-modal knowledge assistant — ingests PDFs with charts and images, answers questions referencing both text and visual content, with source attribution

---

### Module 9 — Observability, Logging & Monitoring

**Learning Objectives**
- Instrument AI applications with end-to-end tracing
- Build dashboards for latency, cost, and quality monitoring
- Set up alerts for production quality degradation

**Topics**
- LLM observability concepts: traces, spans, token usage per request
- LangSmith for LangChain/LangGraph tracing
- Google Cloud Logging and Cloud Monitoring integration
- Latency profiling: identifying bottlenecks (retrieval vs LLM vs postprocessing)
- Cost monitoring: per-model, per-feature, per-user breakdowns
- Quality metrics monitoring: tracking faithfulness/relevance scores over time
- Alerting on quality degradation and cost anomalies
- Structured logging best practices for AI systems

**Mini-Project:** Fully instrumented RAG system with LangSmith tracing, Cloud Monitoring dashboard (latency + cost + quality), and quality degradation alert

---

### Module 10 — Deployment & Scaling on Google Cloud

**Learning Objectives**
- Containerize and deploy AI applications to Google Cloud Run
- Use Vertex AI for managed model serving
- Build CI/CD pipelines that include evaluation gates

**Topics**
- Containerization with Docker: building lean AI application images
- Deploying to Google Cloud Run: configuration, secrets, environment variables
- Vertex AI for managed Gemini model serving and custom model endpoints
- Auto-scaling, load balancing, and connection pooling for AI services
- Caching at the infrastructure layer (Cloud CDN, Memorystore)
- CI/CD pipelines for AI applications: linting, testing, evaluation gates, canary deploys
- Blue-green deployments and rollback strategies for model/prompt changes

**Mini-Project:** Deploy a RAG application to Cloud Run with a full CI/CD pipeline — automated testing, evaluation gate (minimum quality threshold), and canary deployment

---

### Module 11 — Agentic Systems with Google ADK & MCP

**Learning Objectives**
- Orchestrate multi-agent systems using Google Agent Development Kit (ADK)
- Connect agents to enterprise tools via Model Context Protocol (MCP)
- Build reliable, observable agentic pipelines for production

**Topics**
- Google ADK fundamentals: agents, tools, sessions, runners
- Agent orchestration patterns with ADK: sequential, parallel, and loop agents
- Model Context Protocol (MCP): architecture, servers, clients, tool discovery
- Building MCP servers to expose custom enterprise tools to agents
- Connecting agents to databases, internal APIs, and SaaS systems via MCP
- Agent reliability: error recovery, retry logic, human escalation patterns
- Observability for agentic systems: tracing multi-step agent workflows

**Mini-Project:** Tool-rich enterprise agent built with ADK — integrates 3+ enterprise tools via MCP (e.g., internal knowledge base, ticketing system, calendar), with full tracing and human escalation

---

### Module 12 — Testing & Quality Assurance for AI Systems

**Learning Objectives**
- Build a comprehensive test suite for LLM applications
- Run regression and A/B tests to safely ship model and prompt changes
- Integrate continuous evaluation into CI/CD pipelines

**Topics**
- Unit testing LLM applications: mocking LLM responses, testing deterministic logic
- Integration testing for RAG pipelines: testing retrieval quality end-to-end
- Regression testing with golden datasets: catching quality regressions before deploy
- Property-based testing for prompt robustness
- A/B testing and canary deployments for LLM and prompt changes
- Continuous evaluation pipelines: running eval on every PR
- Evaluation-as-a-gate in CI/CD: blocking deploys that regress quality metrics

**Mini-Project:** Full test suite for a RAG application — unit tests, integration tests, golden dataset regression suite, CI integration with evaluation gate

---

---

### Module 13 — Capstone: Enterprise AI System

> **Goal:** Integrate everything from Modules 1–12 into a production-grade, enterprise-ready AI system.

**Build a production-grade multi-agent enterprise assistant with:**

- Multi-format document ingestion pipeline (PDF, DOCX, HTML, images) with async processing
- Hybrid retrieval with reranking and context window management
- Multi-agent orchestration with LangGraph or Google ADK
- FastAPI deployment with streaming responses and resilience patterns
- Semantic caching and model routing for cost optimization
- Observability: LangSmith tracing + Cloud Monitoring dashboards
- Guardrails: prompt injection defense, PII redaction, output safety filtering
- Full test suite with CI/CD pipeline and evaluation gate
- Deployed on Google Cloud Run (or Vertex AI)

**Deliverables:**
- [ ] Architecture design document
- [ ] Working production application deployed to Google Cloud
- [ ] Observability dashboard (latency, cost, quality)
- [ ] Test suite with CI integration
- [ ] Cost and performance benchmarking report
- [ ] 15-minute live demo

---

## Tech Stack

| Category | Tools |
|----------|-------|
| **LLM Provider** | Google Gemini (Flash + Pro, via `google-genai` SDK) |
| **Cloud Platform** | Google Cloud (Vertex AI, Cloud Run, Cloud Tasks, Pub/Sub, Cloud Logging, Memorystore) |
| **Orchestration** | LangChain, LangGraph |
| **Agent Framework** | Google ADK |
| **Protocols** | MCP (Model Context Protocol) |
| **Vector Database** | ChromaDB |
| **Caching** | Redis / Cloud Memorystore (semantic cache) |
| **API Framework** | FastAPI |
| **Observability** | LangSmith, Google Cloud Monitoring |
| **Containerization** | Docker |
| **CI/CD** | GitHub Actions / Cloud Build |
