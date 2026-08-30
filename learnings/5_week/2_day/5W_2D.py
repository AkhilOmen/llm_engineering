from utils.generic_utils import covert_docs_into_chunks, convert_chunks_into_vectors_and_store, get_vector_dimensions, \
    data_visualization_2d, data_visualization_3d

if __name__ == '__main__':
    chunks = covert_docs_into_chunks(
        folders_path="~/Desktop/Personal/AI_Projects/llm_engineering/learnings/5_week/knowledge-base/*",
        chunk_size=1000,
        chunk_overlap=200
    )
    vectorstore = convert_chunks_into_vectors_and_store(chunks)
    get_vector_dimensions(vectorstore)
    data_visualization_2d(vectorstore)
    # data_visualization_3d(vectorstore)

    pass