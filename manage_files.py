import os
import shutil

dest_dir = "C:/Users/lokesh.m.lv/AI_CoE_L-D/AI_CoE_Curriculum/Level_1_Beginner/Day_04_Retrieval_Augmented_Generation"
os.makedirs(dest_dir, exist_ok=True)

src1 = "C:/Users/lokesh.m.lv/AI_CoE_L-D/Learning Path/Day 4 & 5 - Retrieval Augmented Generation (RAG) & Advanced RAG/File_Search.ipynb"
src2 = "C:/Users/lokesh.m.lv/AI_CoE_L-D/Learning Path/Day 4 & 5 - Retrieval Augmented Generation (RAG) & Advanced RAG/Qdrant_similarity_search.ipynb"

if os.path.exists(src1):
    shutil.move(src1, os.path.join(dest_dir, "Day_04_File_Search_Managed_RAG.ipynb"))
if os.path.exists(src2):
    shutil.move(src2, os.path.join(dest_dir, "Day_04_Qdrant_Similarity_Search.ipynb"))
