

import logging
from api.crypto_api import fetch_coin_data
from chat.llm_agent import extract_coin_names

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def process_user_query(user_query: str, context: list) -> dict:
    """
    Process the user's query to extract coin names, fetch data for those coins,
    and return the coin information, considering context.

    Args:
        user_query (str): The user's query.
        context (list): The context of previous queries and responses.

    Returns:
        dict: A dictionary of coin data for each coin mentioned in the query.
    """
    try:
        logger.info(f"Processing query: {user_query}")

        # Build context information
        prev_info = ""
        for elem in context:
            pair = f"Query: {elem['query']} Response: {elem['response']}\n"
            prev_info += pair

        # Combine the query with context
        combined_query = f"This is the context: {prev_info}\nQuery: {user_query}"
        
        # Extract coin names considering context
        coin_names = extract_coin_names(combined_query)
        logger.info(f"Extracted coin names: {coin_names}")

        # Fetch data for each coin
        coin_data = {}
        for coin_name in coin_names:
            data = fetch_coin_data(coin_name)
            if data:
                coin_data[coin_name] = data
                logger.info(f"Fetched data for coin: {coin_name}")
            else:
                logger.warning(f"No data found for coin: {coin_name}")

        return coin_data
    except Exception as e:
        logger.error(f"Error processing user query: {e}", exc_info=True)
        return {}
