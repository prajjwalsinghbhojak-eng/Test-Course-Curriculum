# gemini.md — AI CoE L&D Project Context

> Read before acting. This file provides the core context, goals, and directory structures for Gemini to assist in building the AI Learning Path for the CoE.

---

## 🎯 Project Goal

The goal of this project is to prepare structured learning paths for AI learners across three levels:
- **Level 1 (Beginner)**: A structured 10-day intensive curriculum.
- **Level 2 (Intermediate)**: Topic-based curriculum spanning intermediate concepts.
- **Level 3 (Advanced)**: Topic-based curriculum focused on advanced, production-grade applications.

## 🤖 Gemini's Role

Your primary task in this project is to **find, evaluate, and sort notebooks and other content** from a raw "dump" directory and place them into the structured learning path. 

---

## 📂 Key Directories

### 1. Source Directory (The "Dump")
**Path:** `Learning Path/`  
*(e.g., `C:\Users\lokesh.m.lv\AI_CoE_L-D\Learning Path\`)*

This directory contains raw notebooks, documents, and resources organized roughly by topic or day. It needs to be properly curated, evaluated, and moved into the formal curriculum structure.

### 2. Target Directory (The Structured Output)
**Path:** `AI_CoE_Curriculum/`  
*(e.g., `C:\Users\lokesh.m.lv\AI_CoE_L-D\AI_CoE_Curriculum\`)*

This is where sorted and finalized content belongs. The structure is broken down into:
- `Level_1_Beginner/`
- `Level_2_Intermediate/`
- `Level_3_Advanced/`

### 3. Authoritative Curriculum Reference
**Path:** `curriculum/10-Day Intensive AI Program_ LLM Engineering, RAG Systems & Agentic AI.docx`  

This document contains the exact syllabus and structure that must be followed.

---

## 📜 Strict Rules for Content Sorting

### Level 1 (Beginner)
1. **Strict Adherence:** The path must **strictly follow** the curriculum document (`curriculum/10-Day Intensive AI Program_ LLM Engineering, RAG Systems & Agentic AI.docx`).
2. **Reference Example:** Some work is already completed. ALWAYS check `AI_CoE_Curriculum\Level_1_Beginner\Day_01_LLM_Fundamentals_and_Prompt_Engineering` to verify the expected formatting, file structure, and quality before processing subsequent days. 
3. **Content Verification:** Ensure notebooks selected for Level 1 align perfectly with the beginner scope defined in the curriculum document.

### Level 2 & 3 (Intermediate & Advanced)
1. **Topic-Based Sorting:** These levels are to be sorted by **topic**, advancing beyond the 10-day Level 1 curriculum. 
2. **Complexity Routing:** When evaluating notebooks from the source dump, if they contain material too complex or out-of-scope for the Level 1 10-day curriculum, categorize them logically by topic into Level 2 or Level 3 appropriately.

---

## ✅ Workflow for Gemini

When asked to sort or build out a section of the curriculum:
1. **Analyze:** Read the target day/topic from the authoritative curriculum document.
2. **Search:** Look through the `Learning Path/` dump for notebooks and resources matching the objectives.
3. **Evaluate:** Determine if the content is appropriate for Level 1, 2, or 3 based on complexity.
4. **Organize:** Move and rename files into the `AI_CoE_Curriculum/` structure. Ensure you use clear, descriptive directory and file names similar to the Day 01 example.
