# Day 9 — MCP, Production Engineering & REST APIs

## Learning Objectives
- Master the **Model Context Protocol (MCP)** standard to safely connect LLMs to your data securely.
- Understand how to build standardized MCP Client and Server architectures.
- Deploy Language Models and Agentic workflows as scalable **REST APIs using FastAPI**.
- Learn basic production engineering patterns for serving AI models securely.
- Get a foundational understanding of the **Google Agent Development Kit (ADK)**.

## Prerequisites
- Deep understanding of foundational LLM inference and agentic logic.
- Basic familiarity with HTTP protocols and Python APIs.


## Required Reading
- [Model Context Protocol Introduction](https://modelcontextprotocol.io/docs/getting-started/intro)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## Video Lectures
- [Model Context Protocol (MCP) Explained (YouTube)](https://www.youtube.com/watch?v=1FMy4h68c0o)

## Notebooks (Recommended Sequence)
| # | Notebook | What You'll Learn | Est. Time |
|---|----------|-------------------|-----------|
| 1 | `Day_09_Model_Context_Protocol_102.ipynb` | Comprehensive tutorial on making API requests using the Model Context Protocol, understanding server/client relationships, and providing secure context to LLMs. | 35 min |
| 2 | `Day_09_Building_an_MCP_Server.ipynb` | Hands-on walkthrough defining and structuring a custom backend MCP server to provide bespoke tools dynamically via the standard protocol. | 30 min |
| 3 | `Day_09_FastAPI_for_AI.ipynb` | Structuring an AI backend API using FastAPI and Pydantic for validation and serving Gemini endpoints. | 35 min |
| 4 | `Day_09_Google_ADK_Quickstart.ipynb` | A quickstart introduction to the Google ADK and mapping out your agent strategies. | 20 min |

## Notes
- To view an implementation of a full boilerplate template of a FastAPI RAG service, check out the repository's `templates/rag-fastapi-boilerplate` directory.
