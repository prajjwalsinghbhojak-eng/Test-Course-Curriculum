import os
import shutil

dest_dir = "C:/Users/lokesh.m.lv/AI_CoE_L-D/AI_CoE_Curriculum/Level_1_Beginner/Day_06_Evaluation_Frameworks"
os.makedirs(dest_dir, exist_ok=True)

src_dir = "C:/Users/lokesh.m.lv/AI_CoE_L-D/Learning Path/Day 6 - Evaluation Framework for LLM & RAG"

files_to_move = {
    "rag_evaluation.ipynb": "Day_06_RAG_Evaluation.ipynb",
    "llm_judge.ipynb": "Day_06_LLM_as_a_Judge.ipynb",
    "llm_judge_evaluating_ai_search_engines_with_judges_library.ipynb": "Day_06_Evaluating_AI_Search_Engines.ipynb"
}

for src_name, dest_name in files_to_move.items():
    src_path = os.path.join(src_dir, src_name)
    if os.path.exists(src_path):
        shutil.move(src_path, os.path.join(dest_dir, dest_name))
