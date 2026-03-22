import os
import re

def patch_notebook(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content

        # Clean up old API key variable assignments
        content = re.sub(r'GOOGLE_API_KEY\s*=\s*(?:os\.getenv|userdata\.get)\([^)]+\)(?:\\n)?', '', content)
        content = re.sub(r'GEMINI_API_KEY\s*=\s*(?:os\.getenv|userdata\.get)\([^)]+\)(?:\\n)?', '', content)
        content = re.sub(r'userdata_api_key\s*=\s*(?:os\.getenv|userdata\.get)\([^)]+\)(?:\\n)?', '', content)

        # Replace client instantiations to use get_api_key()
        content = re.sub(r'client\s*=\s*genai\.Client\(api_key=[^)]+\)', 'client = genai.Client(api_key=get_api_key())', content)
        content = re.sub(r'genai\.configure\(api_key=[^)]+\)', 'genai.configure(api_key=get_api_key())', content)

        # Inject the `helpers.auth` import and repo path injection right where `genai` is imported
        # Use single backslashes for n so that it writes as \n in the file, which JSON interprets as a newline.
        setup_injection = 'import sys, os\\nrepo_root = os.path.abspath(os.path.join(os.getcwd(), \\"../../..\\"))\\nif repo_root not in sys.path:\\n    sys.path.append(repo_root)\\nfrom helpers.auth import get_api_key\\nfrom google import genai'
        
        setup_injection_2 = setup_injection.replace('from google import genai', 'import google.generativeai as genai')
        
        if 'from helpers.auth import get_api_key' not in content:
            content = content.replace('from google import genai', setup_injection)
            content = content.replace('import google.generativeai as genai', setup_injection_2)

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Patched: {filepath}")
            
    except Exception as e:
        print(f"Failed to process {filepath}: {e}")

if __name__ == "__main__":
    curriculum_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "AI_CoE_Curriculum")
    
    for root, dirs, files in os.walk(curriculum_dir):
        for file in files:
            if file.endswith('.ipynb'):
                patch_notebook(os.path.join(root, file))
