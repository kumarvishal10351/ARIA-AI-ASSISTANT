from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

def get_relevant_docs(query):
    embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)

    db = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )

    docs = db.similarity_search(query, k=3)
    return docs