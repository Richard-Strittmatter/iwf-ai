from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

import os

def get_context(query, k=10):
    db_path = "/Users/richardstrittmatter/repositories/iwf-ai/chroma_db"
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = Chroma(persist_directory=db_path, embedding_function=embeddings)
    docs = db.similarity_search(query, k=k)
    return "\n\n".join([doc.page_content for doc in docs])

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Bitte gib eine Frage als Argument an.")
        sys.exit(1)
    question = " ".join(sys.argv[1:])
    context = get_context(question)
    if context.strip():
        print('Frage: ' + question)
        print('Kontext: ' + context)
    else:
        print("Kein relevanter Kontext gefunden.")