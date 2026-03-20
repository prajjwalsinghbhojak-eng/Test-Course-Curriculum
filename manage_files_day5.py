import os
import shutil

dest_dir = "C:/Users/lokesh.m.lv/AI_CoE_L-D/AI_CoE_Curriculum/Level_1_Beginner/Day_05_Advanced_RAG"
os.makedirs(dest_dir, exist_ok=True)

src = "C:/Users/lokesh.m.lv/AI_CoE_L-D/Learning Path/Day 4 & 5 - Retrieval Augmented Generation (RAG) & Advanced RAG/Hybrid_Search_Legal.ipynb"

if os.path.exists(src):
    shutil.move(src, os.path.join(dest_dir, "Day_05_Hybrid_Search_Legal_Advanced_RAG.ipynb"))
