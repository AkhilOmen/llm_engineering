import glob
import os

from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from core.config import settings
from utils.constants import DB_NAME


def fetch_documents(folders_path):
    folders = glob.glob(
        os.path.expanduser(
            folders_path
        )
    )

    documents: list = []
    for folder in folders:
        doc_type = os.path.basename(folder)
        loader = DirectoryLoader(folder, glob="**/*.md", loader_cls=TextLoader, loader_kwargs={'encoding': 'utf-8'})
        folder_docs = loader.load()
        for doc in folder_docs:
            doc.metadata["doc_type"] = doc_type
            documents.append(doc)
    return documents


def create_chunks(documents, chunk_size: int = 1000, chunk_overlap: int = 200):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_documents(documents)
    print(f"Divided into {len(chunks)} chunks")

    return chunks


def create_embeddings(chunks):
    # embeddings = HuggingFaceEmbeddings(model="all-MiniLM-L6-v2")
    # embeddings = HuggingFaceEndpointEmbeddings(
    #     model="Qwen/Qwen3-Embedding-8B",
    #     task="feature-extraction",
    #     huggingfacehub_api_token=settings.HUGGINGFACE_ACCESS_TOKEN
    # )
    # embeddings = OllamaEmbeddings(model="ryanshillington/Qwen3-Embedding-8B:latest")
    # embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=settings.OPENAI_API_KEY)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=settings.OPENAI_API_KEY)

    if os.path.exists(DB_NAME):
        Chroma(persist_directory=DB_NAME, embedding_function=embeddings).delete_collection()

    vectorstore = Chroma.from_documents(
        documents=chunks, embedding=embeddings, persist_directory=DB_NAME
    )

    collections = vectorstore._collection
    count = collections.count()
    sample_embedding = collections.get(limit=1, include=["embeddings"])["embeddings"][0]
    dimensions = len(sample_embedding)
    print(f"There are {count:,} vectors with {dimensions:,} dimensions in vector store")

    return vectorstore


def ingestion(folders_path: str):
    documents = fetch_documents(folders_path=folders_path)
    create_chunks(documents=documents, chunk_size=1000, chunk_overlap=200)
    embeddings = create_embeddings(chunks=documents)

    return embeddings