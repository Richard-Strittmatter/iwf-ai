import os
import re
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

ALLOWED_EXTENSIONS = (".md", ".txt", ".php", ".js", ".jsx", ".ts", ".tsx", ".yaml", ".yml", ".json", ".xml", ".pdf")

def split_php_by_function_or_class(code, file_path):
    pattern = r"(class\s+\w+\s*.*?\{)|(function\s+\w+\s*\(.*?\)\s*\{)"
    matches = list(re.finditer(pattern, code, re.DOTALL))
    chunks = []
    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i+1].start() if i+1 < len(matches) else len(code)
        chunk_content = code[start:end].strip()
        if chunk_content:
            name_match = re.match(r"(class|function)\s+(\w+)", match.group())
            name = name_match.group(2) if name_match else "unknown"
            chunk = {
                "content": chunk_content,
                "file_path": file_path,
                "type": "class" if "class" in match.group() else "function",
                "name": name
            }
            chunks.append(chunk)
    return chunks

def split_jsx_by_component(code, file_path):
    pattern = r"(function\s+\w+\s*\(.*?\)\s*\{)|(class\s+\w+\s+extends\s+React\.Component\s*\{)"
    matches = list(re.finditer(pattern, code, re.DOTALL))
    chunks = []
    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i+1].start() if i+1 < len(matches) else len(code)
        chunk_content = code[start:end].strip()
        if chunk_content:
            name_match = re.match(r"(class|function)\s+(\w+)", match.group())
            name = name_match.group(2) if name_match else "unknown"
            chunk = {
                "content": chunk_content,
                "file_path": file_path,
                "type": "component",
                "name": name
            }
            chunks.append(chunk)
    return chunks

docs = []
data_dir = "data"
for root, dirs, files in os.walk(data_dir):
    for filename in files:
        path = os.path.join(root, filename)
        rel_path = os.path.relpath(path, data_dir)
        ext = os.path.splitext(filename)[1]
        if ext == ".php":
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                code = f.read()
            code_chunks = split_php_by_function_or_class(code, rel_path)
            for chunk in code_chunks:
                doc = Document(
                    page_content=chunk["content"],
                    metadata={
                        "source": rel_path,
                        "type": "code",
                        "code_type": chunk["type"],
                        "name": chunk["name"]
                    }
                )
                docs.append(doc)
        elif ext == ".jsx":
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                code = f.read()
            code_chunks = split_jsx_by_component(code, rel_path)
            for chunk in code_chunks:
                doc = Document(
                    page_content=chunk["content"],
                    metadata={
                        "source": rel_path,
                        "type": "code",
                        "code_type": chunk["type"],
                        "name": chunk["name"]
                    }
                )
                docs.append(doc)
        elif filename.endswith(".pdf"):
            loader = PyPDFLoader(path)
            loaded_docs = loader.load()
            for doc in loaded_docs:
                doc.metadata = doc.metadata or {}
                doc.metadata["source"] = rel_path
                doc.metadata["type"] = "docs"
                docs.append(doc)
        elif filename.endswith(ALLOWED_EXTENSIONS):
            loader = TextLoader(path)
            loaded_docs = loader.load()
            for doc in loaded_docs:
                doc.metadata = doc.metadata or {}
                doc.metadata["source"] = rel_path
                doc.metadata["type"] = "docs"
                docs.append(doc)

# Unterschiedliches Chunking für Code und Doku (optional)
splitter_code = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=80)
splitter_docs = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=100)

split_docs = []
for doc in docs:
    if doc.metadata.get("type") == "code":
        # Code-Chunks nicht nochmal splitten, sie sind schon logisch!
        split_docs.append(doc)
    else:
        split_docs.extend(splitter_docs.split_documents([doc]))

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma.from_documents(
    split_docs,
    embeddings,
    persist_directory="chroma_db"
)
db.persist()
print("Datenbank erstellt und Daten geladen.")