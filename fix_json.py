import os
import glob

for f in glob.glob('AI_CoE_Curriculum/**/*.ipynb', recursive=True):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    if '... [truncated]' in content:
        content = content.replace('... [truncated]\n', '",\n')
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Fixed formatting block in {f}")
