Intensive AI Program: LLM Engineering, RAG Systems & Agentic AI
Program Overview
This 10-day intensive program develops practical expertise in LLM engineering, Retrieval Augmented Generation (RAG), evaluation frameworks, and agentic AI systems.
Participants will build production-style AI systems, culminating in a multi-agent enterprise RAG assistant capable of:
Document ingestion


Hybrid retrieval


Streaming responses


Multi-agent orchestration


Evaluation pipelines


API deployment


The program combines conceptual understanding + hands-on implementation.

Day 1 — LLM Fundamentals & Prompt Engineering
Objective
Understand how Large Language Models work and how developers interact with them using prompts and APIs.
Topics Covered
LLM Fundamentals
Overview of Large Language Models


Transformer architecture (conceptual)


LLM capabilities and limitations


Tokens and context windows


Cost considerations for token usage


Prompt Engineering
Prompt design principles


Structured vs unstructured prompts


Zero-shot prompting


Few-shot prompting


Chain-of-thought prompting


Controlled Generation Concepts
Instruction tuning (conceptual)


Reinforcement Learning from Human Feedback (RLHF)


Prompt templates for production systems


Exercises
Experiment with different prompt styles


Compare structured vs unstructured prompts


Few-shot prompt design experiments


Build a simple QA bot using an LLM API



Day 2 — Hallucination Analysis & Embeddings
Objective
Understand why hallucinations occur and how embeddings enable semantic search.
Topics Covered
Hallucination Analysis
Types of hallucinations


Causes of hallucinations in LLMs


Prompt grounding techniques


Generation Control
Temperature


Top-k sampling


Top-p (nucleus sampling)


Output variability control


Embeddings & Semantic Representation
Sentence embeddings


SBERT embedding models


Vector representations


Cosine similarity


Applications of embeddings


Exercises
Run controlled generation experiments


Analyze hallucination behavior


Generate embeddings for sample text


Build a semantic similarity experiment



Day 3 — Vector Databases & Document Processing
Objective
Learn how to store and retrieve embeddings efficiently.
Topics Covered
Vector database fundamentals


FAISS architecture


Chroma database


Document chunking strategies


Metadata filtering


Embedding drift concepts


Exercises
Build pipeline:
PDF → Chunk → Embed → Vector Store
Build a semantic document search engine


Experiment with different chunk sizes



Day 4 — Retrieval Augmented Generation (RAG)
Objective
Build a basic RAG system.
Topics Covered
RAG architecture


Retriever + Generator workflow


Dense retrieval


Context window management


Prompt grounding with retrieved documents


Exercises
Build a RAG chatbot over documents


Compare LLM vs RAG answers


Improve response grounding



Day 5 — Advanced RAG & Hybrid Retrieval
Objective
Improve retrieval accuracy using advanced retrieval techniques.
Topics Covered
Hybrid retrieval (BM25 + Dense)


Query rewriting


Multi-query retrieval


Re-ranking models


Context compression techniques


Exercises
Implement hybrid retrieval pipeline


Add re-ranking model


Measure answer quality improvements



Day 6 — Evaluation Framework for LLM & RAG
Objective
Build systematic evaluation pipelines for AI applications.
Topics Covered
Offline evaluation


Golden dataset creation


Faithfulness evaluation


Answer relevance scoring


Hallucination detection


Retrieval metrics (Precision@K)


LLM-as-judge evaluation


RAGAS framework (concept)


Exercises
Create evaluation dataset


Compute retrieval metrics


Build evaluation pipeline


Compare different RAG versions



Day 7 — Agentic AI Systems & Multi-Agent RAG
Objective
Understand agent-based AI architectures.
Topics Covered
Agentic AI architecture


Planner agents


Retriever agents


Critic agents


Tool-using agents


Function calling


Exercises
Build a Multi-Agent RAG System
Agents:
1️⃣ Retriever Agent
 2️⃣ Answer Generation Agent
 3️⃣ Critic Agent

Day 8 — Production Engineering for AI Systems
Objective
Learn how to prepare AI systems for production environments.
Topics Covered
LLM APIs vs local models


Streaming responses


Latency optimization


Cost optimization


Guardrails


Prompt security


Prompt injection prevention


Logging and monitoring



Day 9 — Agent Frameworks & MCP Tool Integration
Objective
Learn how to integrate agents with external tools and systems using MCP.
Topics Covered
MCP (Model Context Protocol)
What MCP is


Why MCP is useful for AI systems


Connecting LLMs with external tools


Tool discovery and invocation


Tool-Using Agents
Integrating APIs with agents


External knowledge access


Retrieval tools


Data access tools


Google ADK
Agent development concepts


Tool integration


Agent orchestration


Exercises
Build an agent that uses external tools


Integrate MCP-based tool access


Create a tool-enabled AI assistant



Day 10 — FastAPI & REST APIs for AI Applications
Objective
Deploy the RAG system as a production-ready API service.
Topics Covered
FastAPI for AI Systems
FastAPI fundamentals


REST API design for AI services


Request/response schema


Streaming responses


Building AI APIs
RAG API endpoint


Query handling


Response streaming


Deployment Concepts
API architecture for AI


Scalability considerations


Cost monitoring


Hands-On Exercises
Participants will:
Convert their RAG system into a REST API


Build endpoints such as:


POST /query
 POST /upload-document
 GET /health
Test APIs using Postman / curl


Implement streaming responses































Real-World Gen AI Projects
Project 1 — Single Agent Business Assistant
Objective:-
Build a single intelligent agent that can assist business users by retrieving information from internal documents and answering queries accurately.
Business Problem
Organizations often store large amounts of internal documentation such as:
Policy documents
Operational manuals
Technical documentation
Support knowledge bases
Employees spend significant time searching for relevant information. This project builds an AI assistant that can act as a knowledge support agent.
System Capabilities
The agent should be able to:
Accept natural language queries from users


Retrieve relevant information from internal documents


Generate contextual responses using retrieved information


Provide source citations for answers


Maintain conversation context


System Architecture
The system will include:
Document Ingestion Pipeline


Upload PDF / text documents


Chunk documents into smaller segments


Generate embeddings


Vector Storage


Store embeddings in a vector database


Retrieval Layer


Retrieve relevant chunks using similarity search


LLM Response Generation


Generate grounded answers using retrieved context


Example Use Case
User Query:
What is the escalation process for a power outage incident?
Agent Response:
Retrieves the relevant section from operations documentation


Generates a structured answer


Provides document references


Expected Outcome
A business-ready knowledge assistant that can help employees quickly retrieve relevant information from enterprise documentation.



Project 2 — Multi-Agent Enterprise RAG System
Objective
Design and implement a multi-agent Retrieval Augmented Generation (RAG) system where multiple specialized agents collaborate to solve complex queries.
Business Problem
Enterprise systems often require multiple reasoning steps to answer questions. For example:
Identifying relevant documents


Extracting relevant information


Validating answer accuracy


A single agent may not handle all tasks efficiently. A multi-agent architecture allows specialized agents to collaborate.
System Architecture
The system will consist of multiple agents:
1. Retriever Agent
Responsible for retrieving relevant documents from the knowledge base.
Responsibilities:
Interpret user queries


Search vector database


Retrieve top-k relevant document chunks


2. Answer Generation Agent
Responsible for generating responses using retrieved context.
Responsibilities:
Combine retrieved documents


Generate grounded answers


Provide structured responses


3. Critic Agent
Responsible for validating the generated response.
Responsibilities:
Check answer faithfulness


Detect hallucinations


Suggest corrections if needed


Workflow
User submits a query


Retriever Agent retrieves relevant documents


Answer Agent generates the response


Critic Agent evaluates and validates the response


Example Use Case
User Query:
What are the key maintenance procedures for UPS battery systems?
Workflow:
Retriever agent finds relevant technical manuals


Answer agent generates explanation


Critic agent verifies that the answer is grounded in retrieved documents


Expected Outcome
A robust enterprise-grade RAG assistant that uses multiple agents to improve answer reliability and reduce hallucinations.












Project 3 — Agentic Workflow System (Agentic Flow)
Objective
Build an agentic workflow system where AI agents coordinate tasks, execute tools, and perform multi-step reasoning.
Business Problem
Many business workflows require multiple steps such as:
Data retrieval


Analysis


Report generation


Decision support


Traditional automation systems are rigid. Agentic workflows allow dynamic reasoning and adaptive task execution.
System Architecture
The system will include several specialized agents working in a workflow.
1. Planner Agent
Responsibilities:
Analyze user requests


Break tasks into smaller subtasks


Assign tasks to other agents


2. Tool Agent
Responsibilities:
Access external tools or APIs


Retrieve data from databases or APIs


Process structured data


3. Analysis Agent
Responsibilities:
Interpret retrieved data


Generate insights


Perform reasoning


4. Report Generation Agent
Responsibilities:
Generate structured summaries


Create business reports


Provide recommendations


Example Workflow
User Request:
Generate a weekly operational summary for the data center.
Workflow Execution:
Planner Agent breaks request into tasks


Tool Agent retrieves system metrics and logs


Analysis Agent analyzes system performance


Report Agent generates a summarized operational report


Example Output
The system generates a report containing:
Key system metrics


Performance anomalies


Recommended actions


Expected Outcome
A dynamic AI workflow system capable of orchestrating multiple agents to automate complex business processes.











Requirements:- 
Participants will design and implement a production-style enterprise AI assistant.
Required Features
Data Pipeline
Document ingestion


Intelligent chunking


Embedding generation
Retrieval System
Hybrid retrieval (BM25 + Dense)


Metadata filtering


Re-ranking
AI Architecture
Multi-agent system


Retriever agent


Generator agent


Critic agent


System Capabilities
Streaming responses


Citation support


Context grounding


Basic hallucination detection
Monitoring & Evaluation
Logging and monitoring pipeline


Evaluation framework for RAG performance


Retrieval and answer quality metrics
