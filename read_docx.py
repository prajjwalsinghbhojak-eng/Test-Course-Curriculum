import zipfile
import xml.etree.ElementTree as ET

doc_path = "C:/Users/lokesh.m.lv/AI_CoE_L-D/curriculum/10-Day Intensive AI Program_ LLM Engineering, RAG Systems & Agentic AI.docx"
try:
    with zipfile.ZipFile(doc_path) as document:
        xml_content = document.read('word/document.xml')
    tree = ET.XML(xml_content)
    namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    texts = []
    for node in tree.iterfind('.//w:t', namespace):
        if node.text:
            texts.append(node.text)
    text = '\n'.join(texts)
    with open('C:/Users/lokesh.m.lv/AI_CoE_L-D/doc_text.txt', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Extracted", len(text), "chars")
except Exception as e:
    print("Error:", e)
