import os
import shutil

src_dir = "Learning Path"
dest_root = "AI_CoE_Curriculum"

# Find all notebooks
notebook_paths = {}
for root, dirs, files in os.walk(src_dir):
    for f in files:
        if f.endswith('.ipynb'):
            notebook_paths[f] = os.path.join(root, f)

structure = {
    "Level_1_Beginner": {
        "Day_01_LLM_Fundamentals_and_Prompt_Engineering": {
            "notebooks": [
                ("Prompting.ipynb", "Client init, generation, multimodal inputs", "45 min"),
                ("Zero_shot_prompting.ipynb", "Direct tasks without examples", "15 min"),
                ("Few_shot_prompting.ipynb", "Patterns and enforcing output formats (JSON)", "15 min"),
                ("Chain_of_thought_prompting.ipynb", "Forcing explicit reasoning steps", "20 min"),
                ("Role_prompting.ipynb", "Assigning personas for tone/perspective", "15 min")
            ],
            "readme": """# Day 1 — LLM Fundamentals & Prompt Engineering

## Learning Objectives
- Understand LLM overview, transformer architecture, capabilities, and context windows.
- Apply prompt design principles including zero-shot, few-shot, and chain-of-thought.
- Grasp controlled generation concepts like instruction tuning and prompt templates.

## Prerequisites
- Basic Python knowledge.

## Notebooks (Recommended Sequence)
| # | Notebook | What You'll Learn | Est. Time |
|---|----------|-------------------|-----------|
| 1 | `Prompting.ipynb` | Client init, generation, multimodal inputs | 45 min |
| 2 | `Zero_shot_prompting.ipynb` | Direct tasks without examples | 15 min |
| 3 | `Few_shot_prompting.ipynb` | Patterns and enforcing output formats (JSON) | 15 min |
| 4 | `Chain_of_thought_prompting.ipynb` | Forcing explicit reasoning steps | 20 min |
| 5 | `Role_prompting.ipynb` | Assigning personas for tone/perspective | 15 min |

## Supplementary Resources
| Resource | Type | Description |
|----------|------|-------------|
| [Prompt Engineering Interactive Tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial) | Github | Hands-on XML tagging/Claude tutorials. |
| [Prompt Engineering Guide](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/) | Blog | Technical deep-dive into zero/few-shot learning. |
| [Building the GPT Tokenizer](https://youtu.be/zduSFxRajkE) | Video | From-scratch Byte Pair Encoding (BPE). |
| [Transformers United](https://www.youtube.com/playlist?list=PLoROMvodv4rNiJRchCzutFw5ItR_Z27CM) | Video | Stanford CS25 lecture series covering Transformer architectures. |

## Notes
- `Providing_base_cases.ipynb` was excluded as it uses an outdated legacy SDK.
"""
        },
        "Day_02_Hallucination_Analysis_and_Embeddings": {
            "notebooks": [
                ("Embeddings.ipynb", "Text/image/video/audio/PDF embeddings, cosine similarity", "45 min"),
                ("Grounding.ipynb", "Grounding with Google Search, Maps, YouTube, PDFs", "45 min")
            ],
            "readme": """# Day 2 — Hallucination Analysis & Embeddings

## Learning Objectives
- Identify types and causes of hallucinations and apply prompt grounding techniques.
- Control generation using temperature, top-k, top-p.
- Understand sentence embeddings, vector representations, and cosine similarity.

## Prerequisites
- Completion of Day 1.

## Notebooks (Recommended Sequence)
| # | Notebook | What You'll Learn | Est. Time |
|---|----------|-------------------|-----------|
| 1 | `Embeddings.ipynb` | Text/image/video/audio/PDF embeddings, cosine similarity | 45 min |
| 2 | `Grounding.ipynb` | Grounding with Google Search, Maps, YouTube, PDFs | 45 min |

## Supplementary Resources
| Resource | Type | Description |
|----------|------|-------------|
| [Why Language Models Hallucinate](https://openai.com/index/why-language-models-hallucinate/) | Blog | Research explaining hallucinations. |
| [Embedding Models Rundown](https://www.pinecone.io/learn/series/rag/embedding-models-rundown/) | Blog | Comparison of popular text embedding models. |

## Notes
- None.
"""
        },
        "Day_03_Vector_Databases_and_Document_Processing": {
            "notebooks": [
                ("Vectordb_with_chroma.ipynb", "ChromaDB document Q&A without orchestration framework", "60 min")
            ],
            "readme": """# Day 3 — Vector Databases & Document Processing

## Learning Objectives
- Understand vector database fundamentals (FAISS, Chroma).
- Apply document chunking strategies and metadata filtering.
- Build a basic pipeline: PDF → Chunk → Embed → Vector Store.

## Prerequisites
- Completion of Day 2.

## Notebooks (Recommended Sequence)
| # | Notebook | What You'll Learn | Est. Time |
|---|----------|-------------------|-----------|
| 1 | `Vectordb_with_chroma.ipynb` | ChromaDB document Q&A without orchestration framework | 60 min |

## Supplementary Resources
| Resource | Type | Description |
|----------|------|-------------|
| [Chunking Strategies](https://www.pinecone.io/learn/chunking-strategies/) | Blog | Guide on breaking down large documents. |
| [Chonkie Chunking Library](https://qdrant.tech/documentation/data-management/chonkie/) | Docs | Documentation for Chonkie, an optimized text chunking library. |

## Notes
- None.
"""
        },
        "Day_04_Retrieval_Augmented_Generation_RAG": {
            "notebooks": [
                ("Talk_to_documents_with_embeddings.ipynb", "Q&A via dot product similarity", "30 min"),
                ("Gemini_LangChain_QA_Chroma_WebLoad.ipynb", "End-to-end RAG: LangChain + Chroma", "60 min")
            ],
            "readme": """# Day 4 — Retrieval Augmented Generation (RAG)

## Learning Objectives
- Understand RAG architecture and retriever + generator workflow.
- Manage context windows and prompt grounding with retrieved documents.
- Build a RAG chatbot and compare LLM vs RAG answers.

## Prerequisites
- Completion of Day 3.

## Notebooks (Recommended Sequence)
| # | Notebook | What You'll Learn | Est. Time |
|---|----------|-------------------|-----------|
| 1 | `Talk_to_documents_with_embeddings.ipynb` | Q&A via dot product similarity | 30 min |
| 2 | `Gemini_LangChain_QA_Chroma_WebLoad.ipynb` | End-to-end RAG: LangChain + Chroma | 60 min |

## Supplementary Resources
| Resource | Type | Description |
|----------|------|-------------|
| Anatomy of RAG Retriever-Generator | Blog | Core architectural breakdown. |

## Notes
- `Gemini_LangChain_QA_Pinecone_WebLoad.ipynb` was excluded as redundant; the focus is kept on Chroma for simplicity.
"""
        },
        "Day_05_Advanced_RAG_and_Hybrid_Retrieval": {
            "notebooks": [
                ("Hybrid_Search_Legal.ipynb", "Matryoshka embeddings, hybrid search, miniCOIL, RRF", "60 min"),
                ("Search_reranking_using_embeddings.ipynb", "Function calling + Wikipedia, HyDE, cosine re-ranking", "60 min")
            ],
            "readme": """# Day 5 — Advanced RAG & Hybrid Retrieval

## Learning Objectives
- Implement hybrid retrieval (BM25 + Dense), query rewriting, multi-query retrieval.
- Understand re-ranking models and context compression techniques.
- Measure quality improvements in hybrid retrieval pipelines.

## Prerequisites
- Completion of Day 4.

## Notebooks (Recommended Sequence)
| # | Notebook | What You'll Learn | Est. Time |
|---|----------|-------------------|-----------|
| 1 | `Hybrid_Search_Legal.ipynb` | Matryoshka embeddings, hybrid search, miniCOIL, RRF | 60 min |
| 2 | `Search_reranking_using_embeddings.ipynb` | Function calling + Wikipedia, HyDE, cosine re-ranking | 60 min |

## Supplementary Resources
| Resource | Type | Description |
|----------|------|-------------|
| [Hybrid Queries & SPLADE](https://qdrant.tech/documentation/concepts/hybrid-queries/) | Docs | Combining dense vectors with sparse representations. |
| [HyDE Paper](https://arxiv.org/abs/2212.10496) | Paper | Deep dive into Hypothetical Document Embeddings for zero-shot retrieval. |

## Notes
- None.
"""
        },
        "Day_06_Evaluation_Framework_for_LLM_and_RAG": {
            "notebooks": [
                ("Basic_Evaluation.ipynb", "LLM-as-grader, essay comparison, rewriting", "30 min")
            ],
            "readme": """# Day 6 — Evaluation Framework for LLM & RAG

## Learning Objectives
- Perform offline evaluation, create golden datasets, assess faithfulness and answer relevance.
- Detect hallucinations and understand Precision/Recall.
- Utilize LLM-as-judge and understand the RAGAS framework conceptually.

## Prerequisites
- Completion of Day 5.

## Notebooks (Recommended Sequence)
| # | Notebook | What You'll Learn | Est. Time |
|---|----------|-------------------|-----------|
| 1 | `Basic_Evaluation.ipynb` | LLM-as-grader, essay comparison, rewriting | 30 min |

## Supplementary Resources
| Resource | Type | Description |
|----------|------|-------------|
| [LLM Evaluation Metrics](https://wandb.ai/onlineinference/genai-research/reports/LLM-evaluation-Metrics-frameworks-and-best-practices--VmlldzoxMTMxNjQ4NA) | Blog | Guide on evaluating LLMs using statistical metrics and model-based judges. |

## Notes
- GAP FLAGGED: There are no hands-on notebooks demonstrating DeepEval, RAGAS, or LangSmith evaluation frameworks.
"""
        },
        "Day_07_Agentic_AI_Systems_and_Multi_Agent_RAG": {
            "notebooks": [
                ("Function_calling.ipynb", "Parallel/compositional function calling, schema modes", "60 min"),
                ("Agents_Function_Calling_Barista_Bot.ipynb", "Stateful agent loop, automatic function calling", "45 min")
            ],
            "readme": """# Day 7 — Agentic AI Systems & Multi-Agent RAG

## Learning Objectives
- Understand Agentic AI architecture (planner/retriever/critic agents).
- Implement tool-using agents and function calling.
- Build multi-agent interactions.

## Prerequisites
- Completion of Day 6.

## Notebooks (Recommended Sequence)
| # | Notebook | What You'll Learn | Est. Time |
|---|----------|-------------------|-----------|
| 1 | `Function_calling.ipynb` | Parallel/compositional function calling, schema modes | 60 min |
| 2 | `Agents_Function_Calling_Barista_Bot.ipynb` | Stateful agent loop, automatic function calling | 45 min |

## Supplementary Resources
| Resource | Type | Description |
|----------|------|-------------|
| [Agentic AI Architecture](https://www.ibm.com/think/topics/agentic-ai) | Blog | IBM's deep dive into agent architectures and design patterns. |

## Notes
- None.
"""
        },
        "Day_08_Production_Engineering_for_AI_Systems": {
            "notebooks": [],
            "readme": """# Day 8 — Production Engineering for AI Systems

## Learning Objectives
- Compare LLM APIs vs local models.
- Implement streaming responses and latency/cost optimization.
- Apply guardrails, prompt security, prompt injection prevention, logging and monitoring.

## Prerequisites
- Completion of Day 7.

## Notebooks (Recommended Sequence)
No hands-on notebooks for this day. This session is resource-driven — see Supplementary Resources below.

## Supplementary Resources
| Resource | Type | Description |
|----------|------|-------------|
| Instructor-led content | Lecture | APIs, guardrails, streaming, and latency optimization. |

## Notes
- GAP FLAGGED: No notebooks covering production engineering, streaming, guardrails, or prompt security.
"""
        },
        "Day_09_Agent_Frameworks_and_MCP_Tool_Integration": {
            "notebooks": [],
            "readme": """# Day 9 — Agent Frameworks & MCP Tool Integration

## Learning Objectives
- Understand MCP (Model Context Protocol) and tool discovery.
- Build tool-using agents integrating external APIs.
- Utilize Google ADK for agent development and orchestration.

## Prerequisites
- Completion of Day 8.

## Notebooks (Recommended Sequence)
No hands-on notebooks for this day. This session is resource-driven — see Supplementary Resources below.

## Supplementary Resources
| Resource | Type | Description |
|----------|------|-------------|
| [Model Context Protocol (MCP) Docs](https://modelcontextprotocol.io/docs/getting-started/intro) | Docs | Introduction to MCP for connecting AI to external tools. |
| [Agentic AI Architecture](https://www.ibm.com/think/topics/agentic-ai) | Blog | Design patterns for multi-agent systems. |

## Notes
- GAP FLAGGED: No notebooks covering MCP, Google ADK, or orchestration frameworks like LangGraph/AutoGen.
"""
        },
        "Day_10_FastAPI_and_REST_APIs": {
            "notebooks": [],
            "readme": """# Day 10 — FastAPI & REST APIs for AI Applications

## Learning Objectives
- Understand FastAPI fundamentals and REST API design for AI.
- Build RAG API endpoints (POST /query, POST /upload-document, GET /health).
- Grasp deployment concepts: API architecture, scalability, cost monitoring.

## Prerequisites
- Completion of Day 9.

## Notebooks (Recommended Sequence)
No hands-on notebooks for this day. This session is resource-driven — see Supplementary Resources below.

## Supplementary Resources
| Resource | Type | Description |
|----------|------|-------------|
| Instructor-led content | Lecture | FastAPI fundamentals, RAG API design, and deployment architecture. |

## Notes
- GAP FLAGGED: No notebooks covering FastAPI deployment or API schema implementation.
"""
        }
    },
    "Level_2_Intermediate": {
        "Topic_Applied_Prompt_Engineering_and_NLP": {
            "notebooks": [
                ("Basic_Classification.ipynb", "Text classification, zero-temperature", "15 min"),
                ("Basic_Information_Extraction.ipynb", "Entity extraction from unstructured text", "15 min"),
                ("Basic_Code_Generation.ipynb", "Code generation via system instructions", "15 min"),
                ("Basic_Reasoning.ipynb", "Step-by-step logic and math reasoning", "20 min"),
                ("Gemini_LangChain_Summarization_WebLoad.ipynb", "LangChain WebBaseLoader summarization", "30 min")
            ],
            "readme": """# Topic: Applied Prompt Engineering & NLP

## Learning Objectives
- Apply zero-temperature classification and entity extraction.
- Generate and debug code using system instructions.
- Execute complex reasoning tasks.
- Summarize web content using LangChain.

## Prerequisites
- Level 1, Day 1 (Prompt Engineering Basics).

## Notebooks (Recommended Sequence)
| # | Notebook | What You'll Learn | Est. Time |
|---|----------|-------------------|-----------|
| 1 | `Basic_Classification.ipynb` | Text classification, zero-temperature | 15 min |
| 2 | `Basic_Information_Extraction.ipynb` | Entity extraction from unstructured text | 15 min |
| 3 | `Basic_Code_Generation.ipynb` | Code generation via system instructions | 15 min |
| 4 | `Basic_Reasoning.ipynb` | Step-by-step logic and math reasoning | 20 min |
| 5 | `Gemini_LangChain_Summarization_WebLoad.ipynb` | LangChain WebBaseLoader summarization | 30 min |

## Supplementary Resources
| Resource | Type | Description |
|----------|------|-------------|
| LangChain Documentation | Docs | Refer to standard LangChain documentation for WebBaseLoader specifics. |

## Notes
- None.
"""
        },
        "Topic_Embedding_Applications": {
            "notebooks": [
                ("clustering_with_embeddings.ipynb", "t-SNE and KMeans clustering", "60 min"),
                ("anomaly_detection.ipynb", "Euclidean distance outlier detection", "60 min"),
                ("Classify_text_with_embeddings.ipynb", "Keras neural network on embeddings", "60 min")
            ],
            "readme": """# Topic: Embedding Applications

## Learning Objectives
- Perform clustering using t-SNE and KMeans.
- Detect anomalies using Euclidean distances on embeddings.
- Train a Keras neural network classifier on text embeddings.

## Prerequisites
- Level 1, Day 2 (Hallucination Analysis & Embeddings).
- Basic understanding of machine learning models (KMeans, Neural Networks).

## Notebooks (Recommended Sequence)
| # | Notebook | What You'll Learn | Est. Time |
|---|----------|-------------------|-----------|
| 1 | `clustering_with_embeddings.ipynb` | t-SNE and KMeans clustering | 60 min |
| 2 | `anomaly_detection.ipynb` | Euclidean distance outlier detection | 60 min |
| 3 | `Classify_text_with_embeddings.ipynb` | Keras neural network on embeddings | 60 min |

## Supplementary Resources
| Resource | Type | Description |
|----------|------|-------------|
| Scikit-Learn / TensorFlow Docs | Docs | For detailed mathematical definitions of t-SNE and Keras layers. |

## Notes
- None.
"""
        },
        "Topic_Multimodal_and_Structured_Data_Applications": {
            "notebooks": [
                ("Market_a_Jet_Backpack.ipynb", "Multimodal image-to-text, structured JSON (TypedDict)", "60 min"),
                ("Chat_with_SQL_using_langchain.ipynb", "SQLite + LangChain SQL query chain", "45 min")
            ],
            "readme": """# Topic: Multimodal & Structured Data Applications

## Learning Objectives
- Process multimodal inputs (image-to-text).
- Enforce structured JSON outputs using TypedDict.
- Query SQL databases using LangChain SQL chains.

## Prerequisites
- Level 1, Day 1 (Prompt Engineering).
- Basic knowledge of SQL.

## Notebooks (Recommended Sequence)
| # | Notebook | What You'll Learn | Est. Time |
|---|----------|-------------------|-----------|
| 1 | `Market_a_Jet_Backpack.ipynb` | Multimodal image-to-text, structured JSON (TypedDict) | 60 min |
| 2 | `Chat_with_SQL_using_langchain.ipynb` | SQLite + LangChain SQL query chain | 45 min |

## Supplementary Resources
| Resource | Type | Description |
|----------|------|-------------|
| Gemini Multimodal Guide | Docs | Standard Gemini documentation on processing images. |

## Notes
- None.
"""
        },
        "Topic_Native_Tools_and_Alternative_Frameworks": {
            "notebooks": [
                ("File_Search.ipynb", "Gemini File Search tool, grounding metadata", "60 min"),
                ("Gemini_LlamaIndex_QA_Chroma_WebPageReader.ipynb", "LlamaIndex + Chroma Q&A", "60 min")
            ],
            "readme": """# Topic: Native Tools & Alternative Frameworks

## Learning Objectives
- Utilize the native Gemini File Search tool and grounding metadata.
- Implement RAG using LlamaIndex as an alternative to LangChain.

## Prerequisites
- Level 1, Day 4 (RAG).

## Notebooks (Recommended Sequence)
| # | Notebook | What You'll Learn | Est. Time |
|---|----------|-------------------|-----------|
| 1 | `File_Search.ipynb` | Gemini File Search tool, grounding metadata | 60 min |
| 2 | `Gemini_LlamaIndex_QA_Chroma_WebPageReader.ipynb` | LlamaIndex + Chroma Q&A | 60 min |

## Supplementary Resources
| Resource | Type | Description |
|----------|------|-------------|
| LlamaIndex Documentation | Docs | Refer to LlamaIndex documentation for VectorStoreIndex usage. |

## Notes
- None.
"""
        }
    },
    "Level_3_Advanced": {
        "Topic_Prompt_Chaining_and_Thinking_Models": {
            "notebooks": [
                ("Self_ask_prompting.ipynb", "Model self-asks follow-up questions", "20 min"),
                ("Story_Writing_with_Prompt_Chaining.ipynb", "Large task decomposition via iterative prompts", "60 min"),
                ("Get_started_thinking.ipynb", "Gemini Thinking Mode, thinking_budget, thought summaries", "60 min")
            ],
            "readme": """# Topic: Prompt Chaining & Thinking Models

## Learning Objectives
- Guide the model to ask follow-up questions using Self-Ask prompting.
- Decompose large generation tasks using iterative prompt chaining.
- Master Gemini's Thinking Mode, including `thinking_budget` and thought summaries.

## Prerequisites
- Level 1, Day 4 (Advanced Prompting Techniques).

## Notebooks (Recommended Sequence)
| # | Notebook | What You'll Learn | Est. Time |
|---|----------|-------------------|-----------|
| 1 | `Self_ask_prompting.ipynb` | Model self-asks follow-up questions | 20 min |
| 2 | `Story_Writing_with_Prompt_Chaining.ipynb` | Large task decomposition via iterative prompts | 60 min |
| 3 | `Get_started_thinking.ipynb` | Gemini Thinking Mode, thinking_budget, thought summaries | 60 min |

## Supplementary Resources
| Resource | Type | Description |
|----------|------|-------------|
| Gemini Thinking Mode | Docs | Overview of utilizing internal reasoning loops. |

## Notes
- None.
"""
        }
    }
}

os.makedirs(dest_root, exist_ok=True)

for level, folders in structure.items():
    level_path = os.path.join(dest_root, level)
    os.makedirs(level_path, exist_ok=True)
    
    for folder_name, content in folders.items():
        folder_path = os.path.join(level_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        
        # Write README
        with open(os.path.join(folder_path, "README.md"), "w", encoding="utf-8") as f:
            f.write(content["readme"])
            
        # Copy notebooks
        for nb_info in content["notebooks"]:
            nb_name = nb_info[0]
            if nb_name in notebook_paths:
                src = notebook_paths[nb_name]
                dst = os.path.join(folder_path, nb_name)
                shutil.copy2(src, dst)
                print(f"Copied {nb_name} to {folder_path}")
            else:
                print(f"ERROR: Could not find notebook {nb_name}")

print("Curriculum built successfully.")
