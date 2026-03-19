# Day 1 — LLM Fundamentals & Prompt Engineering

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
