import os
import glob

target = 'import sys, os\\nrepo_root ='
replacement = 'import sys, os\\nos.environ[\\"COURSE_PASSPHRASE\\"] = \\"actionable insights accurate decisions\\"\\nrepo_root ='

for f in glob.glob('AI_CoE_Curriculum/**/*.ipynb', recursive=True):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    if target in content and replacement not in content:
        content = content.replace(target, replacement)
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Added passphrase to {f}")
