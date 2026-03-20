import os
import shutil

dest_dir = "C:/Users/lokesh.m.lv/AI_CoE_L-D/AI_CoE_Curriculum/Level_1_Beginner/Day_08_Agentic_Systems"
os.makedirs(dest_dir, exist_ok=True)

src_dir = "C:/Users/lokesh.m.lv/AI_CoE_L-D/Learning Path/Day 7 & 8 Agentic AI Systems & Tool Integration"

files_to_move = {
    "agent_text_to_sql.ipynb": "Day_08_Agent_Text_to_SQL.ipynb",
    "agent_rag.ipynb": "Day_08_Agentic_RAG.ipynb"
}

for src_name, dest_name in files_to_move.items():
    src_path = os.path.join(src_dir, src_name)
    if os.path.exists(src_path):
        shutil.move(src_path, os.path.join(dest_dir, dest_name))
