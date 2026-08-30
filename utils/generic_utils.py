import numpy
import plotly.graph_objects as go
from langchain_chroma import Chroma
from sklearn.manifold import TSNE


def run_python_code_str(python_code_str):
    """
        This exec function will let us run the Python code which is in string format
        for Example:
            run: exec("print(2+2)")
            output: 4
    """

    globals = {"__builtins__": __builtins__}
    exec(python_code_str, globals)


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

