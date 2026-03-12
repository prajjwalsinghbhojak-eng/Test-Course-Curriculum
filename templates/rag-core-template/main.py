from app.rag_engine import RAGEngine

def main():
    # 1. Initialize the Engine
    print("Initializing RAG Engine...")
    engine = RAGEngine()

    # 2. Ingest some sample data
    print("Ingesting data...")
    sample_data = [
        "The AI Center of Excellence (CoE) was established to foster AI innovation.",
        "Generative AI focuses on creating new content like text, images, and code.",
        "RAG stands for Retrieval-Augmented Generation, a technique to ground LLMs in external data."
    ]
    engine.ingest_texts(sample_data)

    # 3. Ask a question
    question = "What does RAG stand for and what is its purpose?"
    print(f"\nQuestion: {question}")
    
    try:
        answer = engine.ask(question)
        print(f"Answer: {answer}")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
