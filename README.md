# AI Center of Excellence (CoE) - L&D 🚀

Welcome to the **AI Center of Excellence Learning & Development** repository. This is the central engineering hub designed to standardize, train, and accelerate the adoption of Generative AI across the organization.

---

## 📖 Overview
This repository serves as a curated environment for team members to transition from AI fundamentals to building production-grade **Generative AI** systems. We focus on modularity, scalability, and the latest industry standards in **LLM Engineering**, **RAG**, and **Agentic Workflows**.

## 🎯 Strategic Objectives
*   **Skill Transformation:** Upskill engineering teams in AI/ML fundamentals and advanced GenAI.
*   **Production Readiness:** Provide "Gold Standard" templates for FastAPI and Core RAG integration.
*   **Standardization:** Enforce Python 3.12+ best practices and modular architecture across all AI projects.

---

## 📁 Repository Architecture
```text
AI_CoE_L-D/
├── curriculum/                 # 📚 Structured training paths & materials
│   └── 10-Day Intensive...     # 10-Day AI Program Document
├── templates/                  # 🛠️ Production-ready starters
│   ├── rag-fastapi-boilerplate # Enterprise Web API with RAG
│   └── rag-core-template       # Lightweight logic-first RAG engine
├── .gitignore                  # Development environment protection
└── README.md                   # Central documentation hub
```

---

## 🔑 Prerequisites & Environment
To ensure compatibility across all templates and learning modules:

### 1. Development Requirements
- **Python:** 3.12+ (Strictly enforced for type hinting and performance).
- **Package Manager:** `pip` or `poetry`.

### 2. AI Infrastructure & Permissions
Our ecosystem supports both developer-friendly and enterprise-grade Google AI backends:
- **Google AI (Gemini API):** Quick access via [Google AI Studio](https://aistudio.google.com/).
- **Vertex AI (GCP):** Enterprise deployment with IAM roles (requires `Vertex AI User` role).
- **Auth:** Ensure `gcloud auth application-default login` is configured for Vertex AI usage.

---

## 🎓 Learning Curriculum
Discover our structured paths for mastering Generative AI:

- 📑 **[10-Day Intensive AI Program: LLM Engineering, RAG Systems & Agentic AI](curriculum/10-Day%20Intensive%20AI%20Program_%20LLM%20Engineering,%20RAG%20Systems%20&%20Agentic%20AI.docx)**
  *A comprehensive deep-dive covering everything from Prompt Engineering to multi-agent systems.*

---

## 🚀 Acceleration Templates
We provide modular boilerplates to jumpstart development with best practices baked in.

### 1. [RAG-FastAPI Boilerplate](templates/rag-fastapi-boilerplate/README.md)
*The "Enterprise Starter"*
- **Best For:** Building scalable web applications and AI-powered microservices.
- **Stack:** FastAPI, Pydantic (Settings), LangChain, ChromaDB.
- **Features:** Production directory structure, Swagger logs, and environment-driven provider switching.

### 2. [RAG-Core Template](templates/rag-core-template/README.md)
*The "Logic-First Modular Template"*
- **Best For:** Scripting, batch jobs, CLI tools, or integration into existing Python apps.
- **Stack:** Pure Python, LangChain, ChromaDB.
- **Features:** Minimal overhead, prompt decoupling, and direct provider access (Gemini/Vertex).

---

## 🛠️ Tech Stack & Standards
- **Core:** Python 3.12+
- **Frameworks:** FastAPI, LangChain, Pydantic
- **AI Models:** Google Gemini (1.5 Flash/Pro), Vertex AI Model Model Garden
- **Vector Search:** ChromaDB
- **Standards:**
  - **Modular Design:** Clear separation between API, Services, and Config.
  - **Prompt Decoupling:** All prompts are stored in `.txt` files in `app/core/prompts/`.
  - **DRY Logic:** Centralized service managers and singleton patterns.
  - **Type Safety:** Full Pydantic validation for all configuration and inputs.

---

## 🤝 Contribution & Support
For queries regarding the CoE or requests for new templates, please reach out to the **AI Center of Excellence Leads**.

*"Building the future of AI, one module at a time."*
