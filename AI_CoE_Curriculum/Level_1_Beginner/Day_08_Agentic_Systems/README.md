# Day 8 — Agentic AI Systems

## Learning Objectives
- Extend simple tool-calling AI to build autonomous agents capable of complex decision-making and reasoning.
- Build "Agentic RAG" systems that don't just linearly pull data, but dynamically reformulate queries and self-query to retrieve optimal information.
- Enable agents to autonomously convert Natural Language to SQL, correcting their own errors dynamically.

## Prerequisites
- Deep understanding of function calling, basic tools, and LLM reasoning loops (Day 7).


## Required Reading
- [Intro to AI Agents (HuggingFace)](https://huggingface.co/learn/cookbook/agents)

## Video Lectures
- [Agentic Design Patterns by Andrew Ng (YouTube)](https://www.youtube.com/watch?v=sal78ACtGTc)

## Notebooks (Recommended Sequence)
| # | Notebook | What You'll Learn | Est. Time |
|---|----------|-------------------|-----------|
| 1 | `Day_08_Agent_Text_to_SQL.ipynb` | Designing an agent capable of retrieving data directly from relational databases with built-in reflection and query correction | 50 min |
| 2 | `Day_08_Agentic_RAG.ipynb` | Overcoming standard RAG boundaries by empowering an agent to iteratively formulate optimized search strategies | 55 min |

## Notes
- Topics beyond single autonomous agents, such as hierarchical multi-agent teams or heavy integrations like multimodal VLMs, are covered extensively in Level 2 & 3.
