import os
import json

dest_dir = "C:/Users/lokesh.m.lv/AI_CoE_L-D/AI_CoE_Curriculum/Level_1_Beginner/Day_09_MCP_and_REST_APIs"
os.makedirs(dest_dir, exist_ok=True)

# Generate MCP Server notebook
mcp_server_notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Day 9: Building an MCP Server from Scratch\n",
    "In this notebook, we'll learn the core concepts of creating your own Model Context Protocol (MCP) server."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "!pip install mcp"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import asyncio\n",
    "from mcp.server import Server\n",
    "from mcp.server.stdio import stdio_server\n",
    "from mcp.types import Tool, TextContent, CallToolResult\n",
    "\n",
    "# Create the server instance\n",
    "app = Server(\"echo-server\")\n",
    "\n",
    "@app.list_tools()\n",
    "async def list_tools() -> list[Tool]:\n",
    "    return [\n",
    "        Tool(\n",
    "            name=\"echo\",\n",
    "            description=\"Echoes back whatever message is provided.\",\n",
    "            inputSchema={\n",
    "                \"type\": \"object\",\n",
    "                \"properties\": {\n",
    "                    \"message\": {\"type\": \"string\"}\n",
    "                },\n",
    "                \"required\": [\"message\"]\n",
    "            }\n",
    "        )\n",
    "    ]\n",
    "\n",
    "@app.call_tool()\n",
    "async def call_tool(name: str, arguments: dict) -> CallToolResult:\n",
    "    if name == \"echo\":\n",
    "        message = arguments.get(\"message\", \"No message provided\")\n",
    "        return CallToolResult(\n",
    "            content=[TextContent(type=\"text\", text=f\"Echo: {message}\")]\n",
    "        )\n",
    "    raise ValueError(f\"Unknown tool: {name}\")\n",
    "\n",
    "print(\"MCP Server defined! You could run this via stdio_server() in a real application.\")"
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
mcp_server_path = os.path.join(dest_dir, "Day_09_Building_an_MCP_Server.ipynb")
with open(mcp_server_path, "w") as f:
    json.dump(mcp_server_notebook, f, indent=1)

# Generate ADK Quickstart notebook
adk_notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Day 9: Google Agent Development Kit (ADK) Quickstart\n",
    "In this notebook, we explore how the Google ADK simplifies building intelligent agents on Google Cloud infrastructure."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### What is the Google ADK?\n",
    "The Agent Development Kit helps developers orchestrate reasoning loops, tool-calling, and interactions with Vertex AI models efficiently. \n",
    "\n",
    "- Uses a declarative model to define Agents.\n",
    "- Easily maps Python functions as tools.\n",
    "- Manages memory and context lengths effortlessly.\n",
    "\n",
    "[Reference Official Google instructions here](https://codelabs.developers.google.com/onramp/instructions#0)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Placeholder for ADK Client Logic\n",
    "print(\"Review the ADK Concepts in the markdown cells above.\")"
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
adk_path = os.path.join(dest_dir, "Day_09_Google_ADK_Quickstart.ipynb")
with open(adk_path, "w") as f:
    json.dump(adk_notebook, f, indent=1)
