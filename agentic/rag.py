from pathlib import Path
import sqlite3
import os

from dotenv import load_dotenv

load_dotenv()

# Cohere Chat uses CO_API_KEY.
# CohereEmbeddings expects COHERE_API_KEY.
if os.getenv("CO_API_KEY") and not os.getenv("COHERE_API_KEY"):
    os.environ["COHERE_API_KEY"] = os.getenv("CO_API_KEY")

from langchain_cohere import CohereEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


# SQLite database location
DB_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "core"
    / "uda_hub.db"
)


# Cohere embedding model
_embeddings = CohereEmbeddings(
    model="embed-english-v3.0"
)


def load_knowledge_articles():
    """Load CultPass knowledge articles from SQLite."""

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    rows = conn.execute(
        """
        SELECT knowledge_id, title, content, category
        FROM Knowledge
        ORDER BY knowledge_id
        """
    ).fetchall()

    conn.close()

    return [
        Document(
            page_content=f"{row['title']}\n{row['content']}",
            metadata={
                "id": row["knowledge_id"],
                "title": row["title"],
                "category": row["category"]
            }
        )
        for row in rows
    ]


def build_vector_store():
    """Create a FAISS vector store from knowledge articles."""

    documents = load_knowledge_articles()

    if not documents:
        raise ValueError(
            "No knowledge articles found in database."
        )

    return FAISS.from_documents(
        documents,
        _embeddings
    )


def search_knowledge(query: str, k: int = 3):
    """Search the knowledge base using semantic similarity."""

    vector_store = build_vector_store()

    results = vector_store.similarity_search_with_score(
        query,
        k=k
    )

    articles = []

    for document, score in results:
        articles.append({
            "id": document.metadata["id"],
            "title": document.metadata["title"],
            "content": document.page_content,
            "category": document.metadata["category"],
            "score": float(score)
        })

    return articles