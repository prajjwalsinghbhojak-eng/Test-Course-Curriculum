# Day 10 — Agents, Function Calling & Tool Integration

## Learning Objectives
- Understand function calling in Gemini models
- Build tools that LLMs can invoke (search, calculator, database lookup)
- Understand agentic AI architecture: planning, reasoning, acting
- Build a ReAct agent with tool use
- Orchestrate multiple specialised agents to solve complex tasks

## Prerequisites
- Completion of Day 9 (Evaluation Frameworks)

## Required Reading
- [Function Calling — Gemini API](https://ai.google.dev/gemini-api/docs/function-calling)
- [A Practical Guide to Building Agents — Anthropic](https://www.anthropic.com/research/building-effective-agents)

## Notebooks (Recommended Sequence)
| # | Notebook | What You'll Learn | Est. Time |
|---|----------|-------------------|-----------|
| 1 | `01_Function_Calling_Basics.ipynb` | Gemini function calling, declaring tools, handling responses | 30 min |
| 2 | `02_Building_Custom_Tools.ipynb` | Web search, calculator, DB lookup, API wrapper tools | 30 min |
| 3 | `03_Introduction_to_Agents.ipynb` | Agent loop (perceive → reason → act), agent types, ReAct pattern | 30 min |
| 4 | `04_Building_a_ReAct_Agent.ipynb` | Implement a full ReAct agent with tool use and memory | 40 min |
| 5 | `05_Multi_Agent_RAG_System.ipynb` | Retriever agent + Generator agent + Critic agent collaboration | 35 min |

## Supplementary Resources
| Resource | Type | Description |
|----------|------|-------------|
| [Gemini Function Calling Guide](https://ai.google.dev/gemini-api/docs/function-calling) | Docs | Official function calling reference |
| [LangGraph](https://langchain-ai.github.io/langgraph/) | Docs | Framework for stateful multi-agent workflows |
| [ReAct Paper](https://arxiv.org/abs/2210.03629) | Paper | Original ReAct (Reason + Act) paper |
