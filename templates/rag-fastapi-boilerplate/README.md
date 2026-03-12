# RAG-FastAPI Boilerplate

This is a production-ready, modular template for building Retrieval-Augmented Generation (RAG) applications using **FastAPI** and **Google Gemini**.

## 📁 Project Structure
```text
rag-fastapi-boilerplate/
├── app/
│   ├── api/            # API routes and controllers
│   ├── core/           
│   │   ├── config.py   # Pydantic settings and environment config
│   │   └── prompts/    # Structured prompt templates (.txt files)
│   ├── services/       # Business logic (RAG, Gemini integration)
│   └── main.py         # Application entry point
├── data/               # Persistent storage for ChromaDB
├── tests/              # Placeholder for unit and integration tests
├── .env.example        # Template for environment variables
├── requirements.txt    # Python dependencies
└── README.md           # Instructions for this template
```

## 📝 Setup Instructions

1. **Clone & Navigate:**
   ```bash
   cd templates/rag-fastapi-boilerplate
   ```

2. **Create Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   - Copy `.env.example` to `.env`.
   - Choose your provider by setting `AI_PROVIDER` to `google` or `vertexai`.
   - **For Google AI:** Add `GOOGLE_API_KEY`.
   - **For Vertex AI:** Add `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION`.

## 🚀 Running the App

Start the development server:
```bash
python app/main.py
```

## 🧠 Configuring Your AI Provider

This boilerplate allows you to switch between **Google AI (Gemini API)** and **Vertex AI (GCP)** without changing any code.

### Option 1: Using Google AI (Gemini API)
*Best for individual developers, quick prototyping, and simple API access.*

1. Set `AI_PROVIDER=google` in your `.env`.
2. Get an API key from [Google AI Studio](https://aistudio.google.com/).
3. **Example `.env`:**
   ```env
   AI_PROVIDER=google
   GOOGLE_API_KEY=AIzaSy...
   ```

### Option 2: Using Vertex AI (Google Cloud)
*Best for enterprise projects, data residency requirements, and deep GCP integration.*

1. Set `AI_PROVIDER=vertexai` in your `.env`.
2. Ensure you have the [Google Cloud CLI](https://cloud.google.com/sdk/docs/install) installed and authenticated (`gcloud auth application-default login`).
3. **Example `.env`:**
   ```env
   AI_PROVIDER=vertexai
   GOOGLE_CLOUD_PROJECT=your-project-id
   GOOGLE_CLOUD_LOCATION=us-central1
   ```

### How it works:
The application uses a **Factory Pattern** in `app/services/rag_service.py`. When the server starts, it reads the `AI_PROVIDER` flag and automatically initializes the corresponding LangChain drivers (`langchain-google-genai` vs `langchain-google-vertexai`).

## 🛠️ How to Use the API

Once the server is running, you can interact with the RAG system using these endpoints:

### 1. Ingest Data
- **Endpoint:** `POST /api/v1/ingest`
- **Body:** `["Text 1", "Text 2"]`

### 2. Query the System
- **Endpoint:** `POST /api/v1/query`
- **Body:** `{"question": "Your question?"}`

### 3. Interactive Docs
- Visit `http://localhost:8000/docs` for the full Swagger UI.

## 📝 Best Practices Implemented
- **Separation of Concerns:** Clearly defined layers for API, Logic, and Config.
- **Prompt Engineering:** Prompts are stored in `.txt` files in `app/core/prompts/` to separate content from code.
- **FastAPI Modular Routing:** Uses `APIRouter` for scalable endpoint management.
- **Environment Management:** Uses `pydantic-settings` to validate and load variables.
- **DRY Principle:** Reusable `RAGService` handled as a singleton.
