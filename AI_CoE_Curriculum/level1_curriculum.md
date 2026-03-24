# AI Center of Excellence — Level 1 Curriculum

> **Level 1 — Beginner: Foundations of Generative AI**
>
> A structured 14-day intensive program that takes learners from zero AI knowledge to a solid foundation in GenAI engineering. All hands-on work uses **Gemini models, Google Cloud services, LangChain, LangGraph, ChromaDB**, and other open-source tools.

| | |
|---|---|
| **Target Audience** | No prior AI knowledge; basic Python required |
| **Format** | 14-day intensive (10 learning days + 4 capstone days) |
| **Duration** | ~14 days |
| **Outcome** | Clear entry-level GenAI Engineer interviews; ready for Level 2 |

---

## Overview

Days 1–10 cover all core concepts through interactive Jupyter notebooks with pre-written code, guided walkthroughs, and **inline coding exercises** embedded directly in the notebooks. Days 11–14 are a hands-on capstone project built with AI-assisted coding.

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

## Tech Stack

| Category | Tools |
|----------|-------|
| **LLM Provider** | Google Gemini (via `google-genai` SDK) |
| **Cloud Platform** | Google Cloud (Vertex AI) |
| **Orchestration** | LangChain, LangGraph |
| **Vector Database** | ChromaDB |
| **Evaluation** | Custom pipelines, LLM-as-judge |
| **IDE Integration** | Gemini in IDE, GitHub Copilot |
