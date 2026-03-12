import os
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from app.core.config import settings

# Import triggers based on provider
if settings.AI_PROVIDER == "google":
    from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
elif settings.AI_PROVIDER == "vertexai":
    from langchain_google_vertexai import VertexAIEmbeddings, ChatVertexAI
    import vertexai
    vertexai.init(project=settings.GOOGLE_CLOUD_PROJECT, location=settings.GOOGLE_CLOUD_LOCATION)

class RAGService:
    """Service to handle Retrieval Augmented Generation (RAG) logic for both Google AI and Vertex AI."""

    def __init__(self):
        self._initialize_models()
        self.vector_db = None
        self.prompt_template = self._load_prompt()

    def _initialize_models(self):
        """Initializes embeddings and LLM based on the selected provider."""
        if settings.AI_PROVIDER == "google":
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=settings.GOOGLE_API_KEY
            )
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=settings.GOOGLE_API_KEY
            )
        elif settings.AI_PROVIDER == "vertexai":
            self.embeddings = VertexAIEmbeddings(
                model_name="text-embedding-004"
            )
            self.llm = ChatVertexAI(
                model_name="gemini-1.5-flash"
            )

    def _load_prompt(self) -> PromptTemplate:
        """Loads the RAG prompt from the prompts directory."""
        prompt_path = os.path.join(os.path.dirname(__file__), "..", "core", "prompts", "rag_system_prompt.txt")
        with open(prompt_path, "r", encoding="utf-8") as f:
            template = f.read()
        return PromptTemplate(template=template, input_variables=["context", "question"])

    def initialize_db(self, texts: list):
        """Initializes the vector database from a list of texts."""
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs = text_splitter.create_documents(texts)
        
        self.vector_db = Chroma.from_documents(
            documents=docs,
            embedding=self.embeddings,
            persist_directory=settings.VECTOR_DB_PATH
        )

    def query(self, question: str):
        """Queries the RAG system."""
        if not self.vector_db:
            self.vector_db = Chroma(
                persist_directory=settings.VECTOR_DB_PATH,
                embedding_function=self.embeddings
            )
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_db.as_retriever(),
            chain_type_kwargs={"prompt": self.prompt_template}
        )
        return qa_chain.invoke(question)

# Singleton instance
rag_service = RAGService()
