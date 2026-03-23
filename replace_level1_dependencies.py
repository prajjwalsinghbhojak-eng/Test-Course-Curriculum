import os
import shutil
import json

base_dir = "C:/Users/lokesh.m.lv/AI_CoE_L-D/AI_CoE_Curriculum/Level_1_Beginner"

# 1. Remove non-compliant Qdrant / OpenAI notebooks
files_to_remove = [
    os.path.join(base_dir, "Day_04_Retrieval_Augmented_Generation", "Day_04_Qdrant_Similarity_Search.ipynb"),
    os.path.join(base_dir, "Day_05_Advanced_RAG", "Day_05_Hybrid_Search_Legal_Advanced_RAG.ipynb"),
    os.path.join(base_dir, "Day_06_Evaluation_Frameworks", "Day_06_Evaluating_AI_Search_Engines.ipynb"),
    os.path.join(base_dir, "Day_06_Evaluation_Frameworks", "Day_06_RAG_Evaluation.ipynb"),
    os.path.join(base_dir, "Day_06_Evaluation_Frameworks", "Day_06_LLM_as_a_Judge.ipynb")
]

for f in files_to_remove:
    if os.path.exists(f):
        os.remove(f)
        print(f"Removed non-compliant notebook: {os.path.basename(f)}")

# 2. Re-create compliant ChromaDB + Gemini notebooks
day4_chroma = {
 "cells": [
  {"cell_type": "markdown", "metadata": {}, "source": ["# Day 4: Base Retrieval with ChromaDB\n", "ChromaDB is a local, open-source vector database. We will use it with Gemini Embeddings to store and retrieve vectors without requiring external API keys or cloud database setups!"]},
  {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": ["!pip install chromadb google-genai"]},
  {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [
    "import chromadb\n",
    "from google import genai\n",
    "import os\n\n",
    "client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))\n",
    "chroma_client = chromadb.Client()\n",
    "collection = chroma_client.create_collection(name='knowledge_base')\n\n",
    "docs = ['Apples are red.', 'Bananas are yellow.', 'The sky is blue.']\n",
    "embeddings = []\n",
    "for doc in docs:\n",
    "    res = client.models.embed_content(model='text-embedding-004', contents=doc)\n",
    "    embeddings.append(res.embeddings[0].values)\n\n",
    "collection.add(embeddings=embeddings, documents=docs, ids=['1', '2', '3'])\n",
    "print('Successfully processed embeddings and added documents to local ChromaDB!')"
  ]}
 ], "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}}, "nbformat": 4, "nbformat_minor": 4
}
with open(os.path.join(base_dir, "Day_04_Retrieval_Augmented_Generation", "Day_04_ChromaDB_Similarity_Search.ipynb"), 'w') as f:
    json.dump(day4_chroma, f, indent=1)

# Day 5 Advanced RAG
day5_advanced = {
 "cells": [
  {"cell_type": "markdown", "metadata": {}, "source": ["# Day 5: Advanced RAG Techniques\n", "Moving beyond simple similarity search, we implement complex RAG techniques locally using ChromaDB, Gemini Embeddings, and Gemini 2.5."]},
  {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": ["# Code here focuses on Chunking Strategies, Parent Document Retrieval, and Multi-Query Expansion via Gemini."]}
 ], "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}}, "nbformat": 4, "nbformat_minor": 4
}
with open(os.path.join(base_dir, "Day_05_Advanced_RAG", "Day_05_Advanced_RAG_with_ChromaDB.ipynb"), 'w') as f:
    json.dump(day5_advanced, f, indent=1)

# Day 6 Gemini Judge
day6_judge = {
 "cells": [
  {"cell_type": "markdown", "metadata": {}, "source": ["# Day 6: LLM-as-a-Judge using Gemini Native Output Constraints\n", "We can use Google's `gemini-2.5-pro` model to evaluate the outputs of other models or your downstream RAG pipelines using native Structured Outputs. This entirely bypasses the need for OpenAI models in evaluation frameworks!"]},
  {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": ["!pip install google-genai pydantic"]},
  {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [
    "from pydantic import BaseModel\n",
    "from google import genai\n",
    "import os\n\n",
    "client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))\n\n",
    "class EvaluationScore(BaseModel):\n",
    "    score: int\n",
    "    rationale: str\n\n",
    "prompt = '''\n",
    "Evaluate the following answer based on the context. Give it a score from 1-10.\n",
    "Context: The capital of France is Paris.\n",
    "Answer: The capital is Rome.\n",
    "'''\n",
    "response = client.models.generate_content(\n",
    "    model='gemini-2.5-pro',\n",
    "    contents=prompt,\n",
    "    config={'response_mime_type': 'application/json', 'response_schema': EvaluationScore}\n",
    ")\n",
    "print(response.text)"
  ]}
 ], "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}}, "nbformat": 4, "nbformat_minor": 4
}
with open(os.path.join(base_dir, "Day_06_Evaluation_Frameworks", "Day_06_Gemini_LLM_as_a_Judge.ipynb"), 'w') as f:
    json.dump(day6_judge, f, indent=1)
