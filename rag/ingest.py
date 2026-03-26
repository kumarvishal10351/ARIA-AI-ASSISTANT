from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os

def create_vector_store():
    documents = []

    data_path = "data"

    for file in os.listdir(data_path):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(data_path, file))
            documents.extend(loader.load())

    embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)

    db = Chroma.from_documents(
        documents,
        embedding=embeddings,
        persist_directory="chroma_db"
    )

    db = Chroma.from_documents(
    documents,
    embedding=embeddings,
    persist_directory="chroma_db"
)

    db.persist()  # 🔥 IMPORTANT

    print("Chroma DB created successfully!")

if __name__ == "__main__":
    create_vector_store()