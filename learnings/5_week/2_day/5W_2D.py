from utils.generic_utils import data_visualization_2d, data_visualization_3d
from utils.ingest import ingestion

if __name__ == '__main__':
    vectorstore = ingestion(
        folders_path="~/Desktop/Personal/AI_Projects/llm_engineering/learnings/5_week/knowledge-base/*",
    )
    data_visualization_2d(vectorstore)
    # data_visualization_3d(vectorstore)
