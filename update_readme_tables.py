import re

def replace_table(path, new_table):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    content = re.sub(r'\| # \| Notebook \|.*?(?=\n##|$)', new_table, content, flags=re.DOTALL)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

t4 = """| # | Notebook | What You'll Learn | Est. Time |
|---|----------|-------------------|-----------|
| 1 | `Day_04_File_Search_Managed_RAG.ipynb` | Introduction to Google's specialized File Search API for seamless, zero-infrastructure RAG over user documents | 40 min |
| 2 | `Day_04_ChromaDB_Similarity_Search.ipynb` | Implementing local vector storage and retrieval manually using open-source ChromaDB and Gemini Embeddings without requiring API keys | 45 min |
"""
replace_table("C:/Users/lokesh.m.lv/AI_CoE_L-D/AI_CoE_Curriculum/Level_1_Beginner/Day_04_Retrieval_Augmented_Generation/README.md", t4)

t5 = """| # | Notebook | What You'll Learn | Est. Time |
|---|----------|-------------------|-----------|
| 1 | `Day_05_Advanced_RAG_with_ChromaDB.ipynb` | Implementing advanced RAG pipelines like Parent Document Retrieval and expansion locally via ChromaDB and Gemini | 60 min |
"""
replace_table("C:/Users/lokesh.m.lv/AI_CoE_L-D/AI_CoE_Curriculum/Level_1_Beginner/Day_05_Advanced_RAG/README.md", t5)

t6 = """| # | Notebook | What You'll Learn | Est. Time |
|---|----------|-------------------|-----------|
| 1 | `Day_06_Gemini_LLM_as_a_Judge.ipynb` | Using Gemini Native Structured Outputs to act as an automated, impartial judge for RAG evaluation and AI scoring | 45 min |
"""
replace_table("C:/Users/lokesh.m.lv/AI_CoE_L-D/AI_CoE_Curriculum/Level_1_Beginner/Day_06_Evaluation_Frameworks/README.md", t6)

print("Tables replaced.")
