from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os

# Alle Textdateien im data-Ordner laden
docs = []
data_dir = "data"
for filename in os.listdir(data_dir):
    if filename.endswith(".md") or filename.endswith(".txt"):
        loader = TextLoader(os.path.join(data_dir, filename))
        docs.extend(loader.load())

# In kleinere Chunks splitten (bessere Suche)
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.split_documents(docs)

# Chroma-Datenbank erstellen und Daten speichern (lokale Embeddings!)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma.from_documents(
    docs,
    embeddings,
    persist_directory="chroma_db"
)
db.persist()
print("Datenbank erstellt und Daten geladen.")