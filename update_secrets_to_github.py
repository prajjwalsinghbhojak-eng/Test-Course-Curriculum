import os
import json
import re

base_dir = "C:/Users/lokesh.m.lv/AI_CoE_L-D/AI_CoE_Curriculum/Level_1_Beginner"

def process_notebook(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            nb = json.load(f)
        except json.JSONDecodeError:
            return False
            
    modified = False
    for cell in nb.get('cells', []):
        if cell['cell_type'] == 'markdown':
            if isinstance(cell['source'], list):
                text = "".join(cell['source'])
            else:
                text = cell['source']
                
            old_text = text
            # Replace various Colab/Authentication markdown instructions
            text = re.sub(r'To run the following cell, your API key must be stored.*?example\.', 
                          '**Authentication:** The API tokens are securely managed via GitHub Secrets and are automatically injected into your environment variables.', text, flags=re.IGNORECASE|re.DOTALL)
            text = re.sub(r'To run this notebook, your API key.*?learn more\.', 
                          '**Authentication:** The API tokens are securely managed via GitHub Secrets and are automatically injected into your environment variables.', text, flags=re.IGNORECASE|re.DOTALL)
            text = re.sub(r'In Colab, add the key to the secrets manager.*?environment variable\.',
                          'The API tokens are managed via GitHub Secrets.', text, flags=re.IGNORECASE|re.DOTALL)
            
            if text != old_text:
                modified = True
                cell['source'] = [text]
                
        elif cell['cell_type'] == 'code':
            if isinstance(cell['source'], list):
                text = "".join(cell['source'])
            else:
                text = cell['source']
                
            old_text = text
            # Remove Colab userdata imports
            text = re.sub(r'from google\.colab import userdata\n?', '', text)
            # Replace userdata.get() with os.getenv()
            text = re.sub(r'userdata\.get\([\'"]([A-Z0-9_]+)[\'"]\)', r'os.getenv("\1")', text)
            
            if text != old_text:
                modified = True
                # Ensure os is imported if we injected os.getenv
                if "os.getenv" in text and "import os" not in text:
                    text = "import os\n" + text
                cell['source'] = [text]
                
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1)
        return True
    return False

count = 0
for root, dirs, files in os.walk(base_dir):
    for filename in files:
        if filename.endswith(".ipynb"):
            if process_notebook(os.path.join(root, filename)):
                count += 1
                print(f"Updated secrets in {filename}")
                
print(f"\nTotal notebooks updated: {count}")
