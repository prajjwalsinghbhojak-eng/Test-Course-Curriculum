import os
import shutil

dest_dir = "C:/Users/lokesh.m.lv/AI_CoE_L-D/AI_CoE_Curriculum/Level_1_Beginner/Day_07_Tool_Integration"
os.makedirs(dest_dir, exist_ok=True)

src_dir = "C:/Users/lokesh.m.lv/AI_CoE_L-D/Learning Path/Day 7 & 8 Agentic AI Systems & Tool Integration"

files_to_move = {
    "Function_calling.ipynb": "Day_07_Function_calling.ipynb",
    "Agents_Function_Calling_Barista_Bot.ipynb": "Day_07_Agents_Function_Calling_Barista_Bot.ipynb",
    "agents.ipynb": "Day_07_Intro_to_smolagents.ipynb"
}

for src_name, dest_name in files_to_move.items():
    src_path = os.path.join(src_dir, src_name)
    if os.path.exists(src_path):
        shutil.move(src_path, os.path.join(dest_dir, dest_name))
