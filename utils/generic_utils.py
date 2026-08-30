import glob
import os

import numpy
from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sklearn.manifold import TSNE
import plotly.graph_objects as go

from core.config import settings


def run_python_code_str(python_code_str):
    """
        This exec function will let us run the Python code which is in string format
        for Example:
            run: exec("print(2+2)")
            output: 4
    """

    globals = {"__builtins__": __builtins__}
    exec(python_code_str, globals)


def covert_docs_into_chunks(folders_path, chunk_size, chunk_overlap):
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

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_documents(documents)
    print(f"Divided into {len(chunks)} chunks")

    return chunks


def convert_chunks_into_vectors_and_store(chunks):
    # embeddings = HuggingFaceEmbeddings(model="all-MiniLM-L6-v2")
    embeddings = HuggingFaceEndpointEmbeddings(
        model="Qwen/Qwen3-Embedding-8B",
        task="feature-extraction",
        huggingfacehub_api_token=settings.HUGGINGFACE_ACCESS_TOKEN
    )
    # embeddings = OllamaEmbeddings(model="ryanshillington/Qwen3-Embedding-8B:latest")
    # embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=settings.OPENAI_API_KEY)
    # embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=settings.OPENAI_API_KEY)
    db_name = "vector_db"

    if os.path.exists(db_name):
        Chroma(persist_directory=db_name, embedding_function=embeddings).delete_collection()

    vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=db_name)
    return vectorstore


def get_vector_dimensions(vectorstore: Chroma):
    collections = vectorstore._collection
    count = collections.count()

    sample_embedding = collections.get(limit=1, include=["embeddings"])["embeddings"][0]
    dimensions = len(sample_embedding)

    print(f"There are {count:,} vectors with {dimensions:,} dimensions in vector store")


def data_visualization_2d(vectorstore: Chroma):
    collections = vectorstore._collection
    results = collections.get(include=['embeddings', 'documents', 'metadatas'])
    vectors = numpy.array(results['embeddings'])
    documents = results['documents']
    metadatas = results['metadatas']
    doc_types = [metadata['doc_type'] for metadata in metadatas]

    colors = [
        ['blue', 'green', 'red', 'orange'] [['products', 'employees', 'contracts', 'company'].index(t)]
        for t in doc_types
    ]

    tsne = TSNE(n_components=2, random_state=42)
    reduced_vectors = tsne.fit_transform(vectors)

    # Create the 2D scatter plot
    fig = go.Figure(data=[go.Scatter(
        x=reduced_vectors[:, 0],
        y=reduced_vectors[:, 1],
        mode='markers',
        marker=dict(size=5, color=colors, opacity=0.8),
        text=[f"Type: {t}<br>Text: {d[:100]}..." for t, d in zip(doc_types, documents)],
        hoverinfo='text'
    )])

    fig.update_layout(
        title='2D Chroma Vector Store Visualization',
        scene=dict(xaxis_title='x', yaxis_title='y'),
        width=800,
        height=600,
        margin=dict(r=20, b=10, l=10, t=40)
    )

    fig.show()


def data_visualization_3d(vectorstore: Chroma):
    collections = vectorstore._collection
    results = collections.get(include=['embeddings', 'documents', 'metadatas'])
    vectors = numpy.array(results['embeddings'])
    documents = results['documents']
    metadatas = results['metadatas']
    doc_types = [metadata['doc_type'] for metadata in metadatas]

    colors = [
        ['blue', 'green', 'red', 'orange'] [['products', 'employees', 'contracts', 'company'].index(t)]
        for t in doc_types
    ]

    tsne = TSNE(n_components=3, random_state=42)
    reduced_vectors = tsne.fit_transform(vectors)

    # Create the 3D scatter plot
    fig = go.Figure(data=[go.Scatter3d(
        x=reduced_vectors[:, 0],
        y=reduced_vectors[:, 1],
        z=reduced_vectors[:, 2],
        mode='markers',
        marker=dict(size=5, color=colors, opacity=0.8),
        text=[f"Type: {t}<br>Text: {d[:100]}..." for t, d in zip(doc_types, documents)],
        hoverinfo='text'
    )])

    fig.update_layout(
        title='3D Chroma Vector Store Visualization',
        scene=dict(xaxis_title='x', yaxis_title='y', zaxis_title='z'),
        width=900,
        height=700,
        margin=dict(r=10, b=10, l=10, t=40)
    )

    fig.show()

