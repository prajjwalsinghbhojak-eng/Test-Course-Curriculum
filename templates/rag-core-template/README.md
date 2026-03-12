# Pure RAG Core Template

A clean, modular Python template for building Retrieval-Augmented Generation (RAG) applications using **Google Gemini** or **Vertex AI**, without the overhead of a web framework.

## 📁 Structure
```text
rag-core-template/
├── app/
│   ├── config.py      # Configuration logic
│   └── rag_engine.py  # Core RAG logic (Gemini/Vertex)
├── data/              # Storage for Vector DB
├── prompts/           # External prompt management
├── .env.example       # Template for keys
├── main.py            # Usage demonstration
└── requirements.txt   # Dependencies
```

## 🚀 Setup
1. **Navigate:** `cd templates/rag-core-template`
2. **Install:** `pip install -r requirements.txt`
3. **Configure:** Copy `.env.example` to `.env` and set your `AI_PROVIDER` (google or vertexai).

## 💻 Usage
Run the demonstration script:
```bash
python main.py
```

## 🧠 Why use this?
- **Lightweight:** No FastAPI or web dependencies.
- **Modular:** Easy to integrate into existing scripts, batch jobs, or CLI tools.
- **Provider Agnostic:** Swap between Standard Gemini and Enterprise Vertex AI with a single environment flag.
