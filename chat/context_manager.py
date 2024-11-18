
import os
import csv
import pandas as pd
import uuid
import logging
from datetime import datetime
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Constants
CHROMA_DB_DIR_BASE = "./chroma_db"
CSV_DB_DIR_BASE = "./context_db"
EMBEDDING_MODEL_NAME = "distilbert-base-nli-stsb-mean-tokens"
COLLECTION_NAME = "query_context"

# Initialize session-specific paths
session_id = f"session_{uuid.uuid4().hex[:8]}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
CHROMA_DB_DIR = f"{CHROMA_DB_DIR_BASE}_{session_id}"
CSV_DB_PATH = f"{CSV_DB_DIR_BASE}_{session_id}.csv"

# Initialize the embedding model
try:
    logger.info("Initializing embedding model...")
    EMBEDDING_MODEL = SentenceTransformer(EMBEDDING_MODEL_NAME)
    logger.info("Embedding model initialized successfully.")
except Exception as e:
    logger.error(f"Error initializing embedding model: {e}")
    raise

# Initialize ChromaDB client
try:
    os.makedirs(CHROMA_DB_DIR, exist_ok=True)
    logger.info(f"ChromaDB directory ensured at: {CHROMA_DB_DIR}")
    client = PersistentClient(path=CHROMA_DB_DIR)
    logger.info("ChromaDB client initialized.")
except Exception as e:
    logger.error(f"Error initializing ChromaDB client: {e}")
    raise

# Initialize ChromaDB collection
try:
    logger.info(f"Creating ChromaDB collection: {COLLECTION_NAME}")
    collection = client.create_collection(name=COLLECTION_NAME)
    logger.info(f"ChromaDB collection '{COLLECTION_NAME}' initialized.")
except Exception as e:
    logger.error(f"Error initializing ChromaDB collection: {e}")
    raise

def initialize_csv_db() -> None:
    """
    Ensures the CSV database exists for the current session.
    """
    try:
        with open(CSV_DB_PATH, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["query", "response"])
        logger.info(f"CSV database initialized at: {CSV_DB_PATH}")
    except Exception as e:
        logger.error(f"Error initializing CSV database: {e}")
        raise

def add_query_to_context(query: str, response: str) -> None:
    """
    Adds a query and its response to both the CSV database and ChromaDB.

    Args:
        query (str): The user query.
        response (str): The response generated by the chatbot.
    """
    try:
        logger.info(f"Adding query to context: Query: {query}, Response: {response}")
        
        # Save to CSV
        with open(CSV_DB_PATH, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([query, response])
        logger.info("Query and response successfully added to CSV.")

        # Save to ChromaDB
        embedding = EMBEDDING_MODEL.encode([query]).tolist()[0]
        logger.info("Generated embedding for query.")
        collection.add(
            documents=[query],
            embeddings=[embedding],
            ids=[f"query_{len(collection.get()['documents']) + 1}"]  # Generate unique ID
        )
        logger.info(f"Query successfully added to ChromaDB: {query}")

    except Exception as e:
        logger.error(f"Error adding query to context: {e}")
        raise

def retrieve_context_for_query(query: str, top_k: int = 3) -> list[dict]:
    """
    Retrieves the most relevant past queries and responses as context.

    Args:
        query (str): The new user query.
        top_k (int): The number of top results to retrieve.

    Returns:
        list[dict]: A list of dictionaries containing "query" and "response" as keys.
    """
    try:
        logger.info(f"Retrieving context for query: {query}")
        # Generate embedding for the input query
        query_embedding = EMBEDDING_MODEL.encode([query]).tolist()[0]
        logger.info("Generated embedding for context retrieval.")

        # Query ChromaDB for similar embeddings
        results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
        logger.info(f"ChromaDB query results: {results}")

        if not results["documents"]:
            logger.info("No relevant context found in ChromaDB.")
            return []

        # Retrieve corresponding data from the CSV database
        context_entries = []
        csv_db = pd.read_csv(CSV_DB_PATH)
        logger.info(f"CSV database loaded with {len(csv_db)} entries.")

        for retrieved_query in results["documents"][0]:
            matching_row = csv_db[csv_db["query"] == retrieved_query]
            if not matching_row.empty:
                context_entries.append(
                    {"query": matching_row.iloc[0]["query"], "response": matching_row.iloc[0]["response"]}
                )

        logger.info(f"Retrieved context entries: {context_entries}")
        return context_entries

    except Exception as e:
        logger.error(f"Error retrieving context for query: {query} - {e}")
        return []

# Ensure the session-specific database is initialized
initialize_csv_db()
