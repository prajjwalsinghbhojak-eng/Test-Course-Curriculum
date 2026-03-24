import os
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from app.config import settings

# Provider logic initialization
if settings.AI_PROVIDER == "google":
    from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
elif settings.AI_PROVIDER == "vertexai":
    from langchain_google_vertexai import VertexAIEmbeddings, ChatVertexAI
    import vertexai
    vertexai.init(project=settings.GOOGLE_CLOUD_PROJECT, location=settings.GOOGLE_CLOUD_LOCATION)

class RAGEngine:
    """A pure RAG engine supporting multiple Google AI providers."""

    def __init__(self):
        self._setup_models()
        self.vector_db = None
        self.prompt = self._load_prompt()

    def _setup_models(self):
        if settings.AI_PROVIDER == "google":
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001", 
                google_api_key=settings.GOOGLE_API_KEY
            )
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash", 
                google_api_key=settings.GOOGLE_API_KEY
            )
        else:
            self.embeddings = VertexAIEmbeddings(model_name="text-embedding-004")
            self.llm = ChatVertexAI(model_name="gemini-1.5-flash")

    def _load_prompt(self):
        path = os.path.join(os.path.dirname(__file__), "..", "prompts", "rag_prompt.txt")
        with open(path, "r", encoding="utf-8") as f:
            return PromptTemplate(template=f.read(), input_variables=["context", "question"])

    def ingest_texts(self, texts: list):
        """Standard ingestion logic."""
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = splitter.create_documents(texts)
        self.vector_db = Chroma.from_documents(
            documents=docs,
            embedding=self.embeddings,
            persist_directory=settings.VECTOR_DB_PATH
        )

    def ask(self, question: str):
        """Retrieve and generate."""
        if not self.vector_db:
            # Try loading existing
            self.vector_db = Chroma(
                persist_directory=settings.VECTOR_DB_PATH,
                embedding_function=self.embeddings
            )
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_db.as_retriever(),
            chain_type_kwargs={"prompt": self.prompt}
        )
        return qa_chain.invoke(question)["result"]
