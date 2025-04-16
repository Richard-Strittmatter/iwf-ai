from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os

ALLOWED_EXTENSIONS = (".md", ".txt", ".php", ".js", ".jsx", ".ts", ".tsx", ".yaml", ".yml", ".json", ".xml", ".pdf")

docs = []
data_dir = "data"
for root, dirs, files in os.walk(data_dir):
    for filename in files:
        path = os.path.join(root, filename)
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(path)
            docs.extend(loader.load())
        elif filename.endswith(ALLOWED_EXTENSIONS):
            loader = TextLoader(path)
            docs.extend(loader.load())

splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=80)
docs = splitter.split_documents(docs)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma.from_documents(
    docs,
    embeddings,
    persist_directory="chroma_db"
)
db.persist()
print("Datenbank erstellt und Daten geladen.")