#!/usr/bin/env python3
"""
Update all specified Jupyter notebooks to replace the bare client initialization
with a proper error-handling block.

This script processes each notebook's cells looking for:
    client = genai.Client(api_key=get_api_key())

And replaces it with:
    from google.genai import errors

    try:
        client = genai.Client(api_key=get_api_key())
    except errors.APIError as e:
        print(f"Gemini API Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    else:
        MODEL_ID = "gemini-2.5-flash"
        print("✅ Ready!")

After the replacement, removes any standalone lines that are now superseded:
    - MODEL_ID = "gemini-2.5-flash"
    - print("✅ Ready!")
    - print("✅ Gemini client initialized successfully!")

(Other model variables like GEN_MODEL, EMBEDDING_MODEL, MODEL are preserved.)
"""

import json
import os

BASE = "/mnt/c/Users/lokesh.m.lv/AI_CoE_L-D"

FILES = [
    "AI_CoE_Curriculum/Level_1_Beginner/Day_10_Agents_Function_Calling_and_Tool_Integration/05_Multi_Agent_RAG_System.ipynb",
    "AI_CoE_Curriculum/Level_1_Beginner/Day_10_Agents_Function_Calling_and_Tool_Integration/04_Building_a_ReAct_Agent.ipynb",
    "AI_CoE_Curriculum/Level_1_Beginner/Day_10_Agents_Function_Calling_and_Tool_Integration/03_Introduction_to_Agents.ipynb",
    "AI_CoE_Curriculum/Level_1_Beginner/Day_10_Agents_Function_Calling_and_Tool_Integration/02_Building_Custom_Tools.ipynb",
    "AI_CoE_Curriculum/Level_1_Beginner/Day_10_Agents_Function_Calling_and_Tool_Integration/01_Function_Calling_Basics.ipynb",
    "AI_CoE_Curriculum/Level_1_Beginner/Day_09_Evaluation_Frameworks/04_Building_an_Evaluation_Pipeline.ipynb",
    "AI_CoE_Curriculum/Level_1_Beginner/Day_09_Evaluation_Frameworks/03_RAG_Retrieval_Metrics.ipynb",
    "AI_CoE_Curriculum/Level_1_Beginner/Day_09_Evaluation_Frameworks/02_LLM_Output_Evaluation.ipynb",
    "AI_CoE_Curriculum/Level_1_Beginner/Day_09_Evaluation_Frameworks/01_Why_Evaluation_Matters.ipynb",
    "AI_CoE_Curriculum/Level_1_Beginner/Day_08_Advanced_RAG/04_Context_Compression_and_Filtering.ipynb",
    "AI_CoE_Curriculum/Level_1_Beginner/Day_08_Advanced_RAG/03_Reranking_Models.ipynb",
    "AI_CoE_Curriculum/Level_1_Beginner/Day_08_Advanced_RAG/02_Query_Transformation.ipynb",
    "AI_CoE_Curriculum/Level_1_Beginner/Day_08_Advanced_RAG/01_Hybrid_Retrieval.ipynb",
    "AI_CoE_Curriculum/Level_1_Beginner/Day_07_Retrieval_Augmented_Generation/04_RAG_vs_Vanilla_LLM.ipynb",
    "AI_CoE_Curriculum/Level_1_Beginner/Day_07_Retrieval_Augmented_Generation/02_Building_a_Basic_RAG_System.ipynb",
    "AI_CoE_Curriculum/Level_1_Beginner/Day_07_Retrieval_Augmented_Generation/01_RAG_Architecture_Overview.ipynb",
    "AI_CoE_Curriculum/Level_1_Beginner/Day_06_Vector_Databases_and_Document_Processing/04_Document_Processing_Pipeline.ipynb",
    "AI_CoE_Curriculum/Level_1_Beginner/Day_06_Vector_Databases_and_Document_Processing/03_Document_Chunking_Strategies.ipynb",
    "AI_CoE_Curriculum/Level_1_Beginner/Day_06_Vector_Databases_and_Document_Processing/02_Getting_Started_with_ChromaDB.ipynb",
    "AI_CoE_Curriculum/Level_1_Beginner/Day_06_Vector_Databases_and_Document_Processing/01_Vector_Database_Fundamentals.ipynb",
    "AI_CoE_Curriculum/Level_1_Beginner/Day_05_Embeddings_and_Semantic_Search/04_Semantic_Search_Application.ipynb",
    "AI_CoE_Curriculum/Level_1_Beginner/Day_05_Embeddings_and_Semantic_Search/03_Similarity_Search.ipynb",
    "AI_CoE_Curriculum/Level_1_Beginner/Day_05_Embeddings_and_Semantic_Search/02_Generating_Embeddings_with_Gemini.ipynb",
    "AI_CoE_Curriculum/Level_1_Beginner/Day_05_Embeddings_and_Semantic_Search/01_What_are_Embeddings.ipynb",
    "AI_CoE_Curriculum/Level_1_Beginner/Day_04_Hallucinations_and_Grounding/04_Safety_Settings_and_Guardrails.ipynb",
    "AI_CoE_Curriculum/Level_1_Beginner/Day_04_Hallucinations_and_Grounding/03_Generation_Control_Parameters.ipynb",
    "AI_CoE_Curriculum/Level_1_Beginner/Day_04_Hallucinations_and_Grounding/02_Grounding_Techniques.ipynb",
    "AI_CoE_Curriculum/Level_1_Beginner/Day_04_Hallucinations_and_Grounding/01_Understanding_Hallucinations.ipynb",
    "AI_CoE_Curriculum/Level_1_Beginner/Day_03_Advanced_Prompt_Engineering/04_Building_a_Prompt_Library.ipynb",
    "AI_CoE_Curriculum/Level_1_Beginner/Day_03_Advanced_Prompt_Engineering/03_ReAct_Prompting_Pattern.ipynb",
    "AI_CoE_Curriculum/Level_1_Beginner/Day_03_Advanced_Prompt_Engineering/02_Structured_Output_Generation.ipynb",
    "AI_CoE_Curriculum/Level_1_Beginner/Day_03_Advanced_Prompt_Engineering/01_Advanced_Prompting_Techniques.ipynb",
    "AI_CoE_Curriculum/Level_1_Beginner/Day_02_Prompt_Engineering_Fundamentals/05_Prompt_Design_Patterns.ipynb",
    "AI_CoE_Curriculum/Level_1_Beginner/Day_02_Prompt_Engineering_Fundamentals/04_Role_and_System_Prompting.ipynb",
    "AI_CoE_Curriculum/Level_1_Beginner/Day_02_Prompt_Engineering_Fundamentals/03_Chain_of_Thought_Prompting.ipynb",
    "AI_CoE_Curriculum/Level_1_Beginner/Day_02_Prompt_Engineering_Fundamentals/02_Few_Shot_Prompting.ipynb",
    "AI_CoE_Curriculum/Level_1_Beginner/Day_02_Prompt_Engineering_Fundamentals/01_Zero_Shot_Prompting.ipynb",
    "AI_CoE_Curriculum/Level_1_Beginner/Day_01_Introduction_to_AI_and_LLMs/03_Your_First_LLM_Call.ipynb",
]

TARGET = 'client = genai.Client(api_key=get_api_key())'

# Lines (stripped of leading/trailing whitespace) to remove after the target
# because they are superseded by the else block
SUPERSEDED = {
    'MODEL_ID = "gemini-2.5-flash"',
    'print("\u2705 Ready!")',
    'print("\u2705 Gemini client initialized successfully!")',
}

# The replacement block as a list of (content, has_newline) tuples
# where content is the line without indentation prefix or trailing newline
BLOCK = [
    ('from google.genai import errors', True),
    ('', True),  # blank line
    ('try:', True),
    ('    client = genai.Client(api_key=get_api_key())', True),
    ('except errors.APIError as e:', True),
    ('    print(f"Gemini API Error: {e}")', True),
    ('except Exception as e:', True),
    ('    print(f"An unexpected error occurred: {e}")', True),
    ('else:', True),
    ('    MODEL_ID = "gemini-2.5-flash"', True),
    ('    print("\u2705 Ready!")', False),  # last line - no newline by default
]


def transform_cell_source(source):
    """
    Transform the source list of a single code cell.
    Returns (new_source, changed).

    Algorithm:
    1. Find the line containing TARGET
    2. Build the replacement block with matching indentation
    3. Skip the errors import header if already present in the cell
    4. Insert replacement in place of the TARGET line
    5. After replacement, skip any lines whose stripped content is in SUPERSEDED
    """
    full_text = ''.join(source)

    if TARGET not in full_text:
        return source, False

    if 'except errors.APIError' in full_text:
        # Already transformed - skip
        return source, False

    has_errors_import = 'from google.genai import errors' in full_text

    # Find the index of the target line
    target_idx = None
    for idx, line in enumerate(source):
        if TARGET in line:
            target_idx = idx
            break

    if target_idx is None:
        return source, False

    # Determine indentation from the target line
    target_line = source[target_idx]
    stripped_target = target_line.rstrip('\n').rstrip('\r')
    indent_len = len(stripped_target) - len(stripped_target.lstrip())
    prefix = stripped_target[:indent_len]

    # Build replacement lines
    block_start = 2 if has_errors_import else 0  # skip 'from google.genai import errors' + blank
    rep_lines = []
    block_to_use = BLOCK[block_start:]

    for content, has_nl in block_to_use:
        if content == '':
            rep_lines.append('\n')
        else:
            rep_lines.append(prefix + content + ('\n' if has_nl else ''))

    # Build the output:
    # - Everything before target_idx
    # - Replacement block
    # - Everything after target_idx, skipping SUPERSEDED lines

    before = list(source[:target_idx])
    after_raw = list(source[target_idx + 1:])

    # Filter out SUPERSEDED lines from after
    after = []
    for line in after_raw:
        content_stripped = line.rstrip('\n').rstrip('\r').strip()
        if content_stripped in SUPERSEDED:
            continue
        after.append(line)

    # Combine
    new_source = before + rep_lines + after

    # Ensure last line has no trailing newline (Jupyter notebook convention)
    if new_source and new_source[-1].endswith('\n'):
        new_source[-1] = new_source[-1][:-1]

    # But if there were lines after the block, we need the last rep line to have a newline
    # (it was added without one). Let's fix: if there are 'after' lines,
    # the last rep_line needs a newline, and the last overall line should not.
    # Actually our logic above handles it: we strip the final newline at the end.
    # But we need to make sure the rep_lines[-1] has a newline if there are after lines.
    if after:
        # Find last rep_line in new_source and ensure it has newline before the after section
        # new_source = before + rep_lines + after
        # rep_lines end at index len(before) + len(rep_lines) - 1
        rep_end_idx = len(before) + len(rep_lines) - 1
        if rep_end_idx < len(new_source) and not new_source[rep_end_idx].endswith('\n'):
            new_source[rep_end_idx] = new_source[rep_end_idx] + '\n'

    return new_source, True


def process_notebook(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    total_changes = 0
    for cell_idx, cell in enumerate(nb['cells']):
        if cell['cell_type'] != 'code':
            continue
        new_source, changed = transform_cell_source(cell['source'])
        if changed:
            cell['source'] = new_source
            total_changes += 1
            print(f"  Cell {cell_idx}: updated")

    if total_changes > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
            f.write('\n')
        print(f"  => Wrote {total_changes} change(s) to {os.path.basename(filepath)}")
    else:
        print(f"  => No changes needed in {os.path.basename(filepath)}")

    return total_changes


def main():
    total_files_changed = 0
    total_cells_changed = 0

    for rel_path in FILES:
        full_path = os.path.join(BASE, rel_path)
        if not os.path.exists(full_path):
            print(f"[MISSING] {full_path}")
            continue
        print(f"Processing: {rel_path.split('/')[-1]}")
        n = process_notebook(full_path)
        if n > 0:
            total_files_changed += 1
            total_cells_changed += n

    print(f"\n{'='*60}")
    print(f"Done. Modified {total_files_changed} files, {total_cells_changed} cells total.")


if __name__ == '__main__':
    main()
