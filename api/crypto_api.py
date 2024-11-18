
import requests
import logging
from time import sleep

# Configure logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Constants
BASE_URL = "https://api.coincap.io/v2/assets"
MAX_RETRIES = 3  # Number of retries
TIMEOUT = 10  # Timeout for each request (in seconds)
RETRY_DELAY = 2  # Delay between retries (in seconds)

def fetch_coin_data(coin_name: str) -> dict:
    """
    Fetches data for a specific coin from the CoinCap API.

    Args:
        coin_name (str): The name of the cryptocurrency.

    Returns:
        dict: Data for the requested cryptocurrency or None if the API call fails.
    """
    url = f"{BASE_URL}/{coin_name.lower()}"
    retries = 0

    while retries < MAX_RETRIES:
        try:
            logger.info(f"Fetching data for {coin_name}, attempt {retries + 1}...")
            response = requests.get(url, timeout=TIMEOUT)
            response.raise_for_status()  # Raise HTTPError for bad responses
            logger.info(f"Successfully fetched data for {coin_name}.")
            return response.json().get("data", {})
        except requests.exceptions.RequestException as e:
            retries += 1
            logger.error(f"Error fetching data for {coin_name}: {e}")
            if retries < MAX_RETRIES:
                logger.info(f"Retrying in {RETRY_DELAY} seconds...")
                sleep(RETRY_DELAY)
            else:
                logger.error(f"Failed to fetch data for {coin_name} after {MAX_RETRIES} attempts.")
                return None
