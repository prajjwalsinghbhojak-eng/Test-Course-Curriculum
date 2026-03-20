import os
import shutil

base_dir = "C:/Users/lokesh.m.lv/AI_CoE_L-D/AI_CoE_Curriculum/Level_1_Beginner"

# 1. Cleanup duplicates
def merge_dirs(src, dest):
    if os.path.exists(src):
        os.makedirs(dest, exist_ok=True)
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dest, item)
            if os.path.isfile(s) and not os.path.exists(d):
                shutil.move(s, d)
        print(f"Merged {src} into {dest}")
        # Only remove if it's empty after move
        if not os.listdir(src):
            shutil.rmtree(src)
        else:
            print(f"Warning: {src} not empty after merge")

merge_dirs(os.path.join(base_dir, "Day_04_Retrieval_Augmented_Generation_RAG"), os.path.join(base_dir, "Day_04_Retrieval_Augmented_Generation"))
merge_dirs(os.path.join(base_dir, "Day_05_Advanced_RAG_and_Hybrid_Retrieval"), os.path.join(base_dir, "Day_05_Advanced_RAG"))

# 2. Inject Reading and Video
resources = {
    "Day_01": {
        "read": "- [Anthropic Prompt Engineering Tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial)\n- [Prompt Engineering Guide](https://www.promptingguide.ai/)",
        "vid": "- [Intro to Large Language Models by Andrej Karpathy (YouTube)](https://www.youtube.com/watch?v=zjkBMFhNj_g)"
    },
    "Day_02": {
        "read": "- [Google ML Crash Course: Embeddings](https://developers.google.com/machine-learning/crash-course/embeddings/video-lecture)\n- [Understanding LLM Hallucinations](https://www.ibm.com/topics/ai-hallucinations)",
        "vid": "- [Word Embeddings Explained (YouTube)](https://www.youtube.com/watch?v=5PL0TmQNN5w)"
    },
    "Day_03": {
        "read": "- [Pinecone: What is a Vector Database?](https://www.pinecone.io/learn/vector-database/)",
        "vid": "- [Vector Databases Explained - IBM Technology (YouTube)](https://www.youtube.com/watch?v=klvqMVhA9A0)"
    },
    "Day_04": {
        "read": "- [What is Retrieval-Augmented Generation (RAG)?](https://www.ibm.com/topics/retrieval-augmented-generation)",
        "vid": "- [Retrieval Augmented Generation (RAG) Explained: A Visual Guide (YouTube)](https://www.youtube.com/watch?v=T-D1OfcDW1M)"
    },
    "Day_05": {
        "read": "- [Hugging Face Blog: Matryoshka Embeddings](https://huggingface.co/blog/matryoshka)\n- [Qdrant: Hybrid Search Concepts](https://qdrant.tech/documentation/concepts/hybrid-queries/)",
        "vid": "- [Building Production-Ready RAG Applications (YouTube)](https://www.youtube.com/watch?v=1bXyG2Wv3vM)"
    },
    "Day_06": {
        "read": "- [Evaluating RAG Pipelines with Ragas](https://docs.ragas.io/)",
        "vid": "- [LLM-as-a-Judge Explained (YouTube)](https://www.youtube.com/watch?v=vjTz_XzH7nI)"
    },
    "Day_07": {
        "read": "- [Function Calling and Tool Use Introduction](https://platform.openai.com/docs/guides/function-calling)",
        "vid": "- [How to let LLMs use tools (Function Calling) (YouTube)](https://www.youtube.com/watch?v=0RSBEA9-X-M)"
    },
    "Day_08": {
        "read": "- [Intro to AI Agents (HuggingFace)](https://huggingface.co/learn/cookbook/agents)",
        "vid": "- [Agentic Design Patterns by Andrew Ng (YouTube)](https://www.youtube.com/watch?v=sal78ACtGTc)"
    },
    "Day_09": {
        "read": "- [Model Context Protocol Introduction](https://modelcontextprotocol.io/docs/getting-started/intro)\n- [FastAPI Documentation](https://fastapi.tiangolo.com/)",
        "vid": "- [Model Context Protocol (MCP) Explained (YouTube)](https://www.youtube.com/watch?v=1FMy4h68c0o)"
    },
    "Day_10": {
        "read": "- [Dockerizing FastAPI applications (FastAPI)](https://fastapi.tiangolo.com/deployment/docker/)",
        "vid": "- [Deploying AI Models to Google Cloud Run (YouTube)](https://www.youtube.com/watch?v=v_CW06Y8dYg)"
    }
}

for root, dirs, files in os.walk(base_dir):
    if "README.md" in files:
        cur_dir = os.path.basename(root)
        day_prefix = cur_dir[:6]
        if day_prefix in resources:
            readme_path = os.path.join(root, "README.md")
            with open(readme_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            if "## Required Reading" in content:
                print(f"Skipped {readme_path} (Already has reading material)")
                continue
                
            ins_text = f"\n## Required Reading\n{resources[day_prefix]['read']}\n\n## Video Lectures\n{resources[day_prefix]['vid']}\n\n"
            
            if "## Notebooks" in content:
                content = content.replace("## Notebooks", ins_text + "## Notebooks")
            elif "## Prerequisites" in content:
                content = content.replace("## Prerequisites", ins_text + "## Prerequisites")
            else:
                content += ins_text
                
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Updated {readme_path}")
