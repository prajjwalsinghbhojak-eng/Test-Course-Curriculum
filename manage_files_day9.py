import os
import urllib.request
import json

dest_dir = "C:/Users/lokesh.m.lv/AI_CoE_L-D/AI_CoE_Curriculum/Level_1_Beginner/Day_09_MCP_and_REST_APIs"
os.makedirs(dest_dir, exist_ok=True)

# Download MCP notebook
mcp_url = "https://raw.githubusercontent.com/itprodirect/Model-Context-Protocol-102/main/Model-Context-Protocol-102.ipynb"
mcp_path = os.path.join(dest_dir, "Day_09_Model_Context_Protocol_102.ipynb")
req = urllib.request.Request(mcp_url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        with open(mcp_path, 'wb') as f:
            f.write(response.read())
except Exception as e:
    print(f"Error downloading MCP notebook: {e}")

# Generate FastAPI notebook
fastapi_notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Day 9: Production Engineering with FastAPI\n",
    "In this notebook, we'll learn how to expose our Language Models and Agentic workflows as REST APIs using FastAPI."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "!pip install fastapi uvicorn google-genai"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "from fastapi import FastAPI\n",
    "from pydantic import BaseModel\n",
    "from google import genai\n",
    "import os\n",
    "\n",
    "# Note: In a real environment, you'd run this via `uvicorn main:app --reload`\n",
    "# We're defining the structure here for conceptual understanding.\n",
    "\n",
    "app = FastAPI(title=\"AI Agent API\")\n",
    "client = genai.Client(api_key=os.environ.get(\"GEMINI_API_KEY\"))\n",
    "\n",
    "class QueryRequest(BaseModel):\n",
    "    prompt: str\n",
    "\n",
    "@app.post(\"/generate\")\n",
    "def generate_response(request: QueryRequest):\n",
    "    response = client.models.generate_content(\n",
    "        model=\"gemini-2.5-flash\",\n",
    "        contents=request.prompt\n",
    "    )\n",
    "    return {\"response\": response.text}\n",
    "\n",
    "print(\"FastAPI app defined!\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
fastapi_path = os.path.join(dest_dir, "Day_09_FastAPI_for_AI.ipynb")
with open(fastapi_path, "w") as f:
    json.dump(fastapi_notebook, f, indent=1)
