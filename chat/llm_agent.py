import os
import json
import re
import logging
from together import Together

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


# Set the API key for Groq
os.environ["TOGETHER_API_KEY"] = "TOGETHER_API_KEY" # add your together api key
# my api key - if needed - 413ac117da2566fb5dcbfbe7a6a5a2fae14b0beb39cd9ea2ac584903d5261aad (limit: $1 only)

# Initialize the Together client
try:
    client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))
    logger.info("Together client initialized successfully.")
except Exception as e:
    logger.error(f"Error initializing Together client: {e}")
    raise

def extract_coin_names(user_query: str) -> list:
    """
    Extracts cryptocurrency names from the user's query using LLM, ensuring the response is in JSON format.
    Parses the JSON and returns a list of valid cryptocurrency names.

    Args:
        user_query (str): The user's query.

    Returns:
        list: A list of extracted cryptocurrency names.
    """
    if not isinstance(user_query, str) or not user_query.strip():
        logger.warning("Invalid user query received. Skipping extraction.")
        return []

    # List of valid cryptocurrency names
    valid_cryptos = [
        'bitcoin', 'ethereum', 'tether', 'solana', 'binance-coin', 'dogecoin', 'xrp', 'usd-coin', 'steth',
        'cardano', 'tron', 'avalanche', 'shiba-inu', 'wrapped-bitcoin', 'chainlink', 'bitcoin-cash', 'polkadot',
        'near-protocol', 'unus-sed-leo', 'litecoin', 'stellar', 'multi-collateral-dai', 'uniswap', 'sp8de',
        'internet-computer', 'crypto-com-coin', 'ethereum-classic', 'fetch', 'stacks', 'monero', 'okb', 'filecoin',
        'aave', 'vechain', 'fantom', 'the-graph', 'injective-protocol', 'thorchain', 'mantra-dao', 'raydium',
        'algorand', 'theta', 'cosmos', 'bitcoin-sv', 'maker', 'hedera-hashgraph', 'kucoin-token', 'arweave',
        'lido-dao', 'gala', 'flow', 'helium', 'eos', 'quant', 'polygon', 'gatetoken', 'ecash', 'neo', 'axie-infinity',
        'pendle', 'aioz-network', 'the-sandbox', 'akash-network', 'tezos', 'nexo', 'mina', 'decentraland',
        'elrond-egld', 'conflux-network', 'zcash', 'gnosis-gno', 'superfarm', 'chiliz', 'ftx-token', 'nervos-network',
        'oasis-network', 'iota', 'pancakeswap', 'dexe', 'xinfin-network', 'kava', 'trueusd', 'compound', 'wootrade',
        'nxm', 'theta-fuel', 'curve-dao-token', 'trust-wallet-token', 'amp', '1inch', 'livepeer', 'iotex',
        'synthetix-network-token', 'reserve-rights', 'zilliqa', 'holo', 'celo', 'golem-network-tokens', 'dash', 'kusama'
    ]

    try:
        # Prepare the LLM prompt
        messages = [
            {
                "role": "user",
                "content": (
                    f""" You are an expert in understanding the user input query, and following a set of instructions. You will be given a list of valid
    cryptocurrency names:{valid_cryptos}. Your task is simple, understand the user input query, and identify the valid cyrptocurrency(s) mentioned
     in the user query. You should try to interpret any ambiguous terms present in the user query as something related to the cryptocurrency domain within the realm of rationality.
     ** Important Points: **
     1.You should ALWAYS return the output as a single json only. There should be absolutely nothing else apart from a single json object at all.
     2. Never include filler lines in the beginning of the output like:
        'Here is the information about "valid cyrptocurrency name" 
    
    ** Output Format: **
        {{
            "currencies_mentioned": ["currency1","currency2","currency3"]
        }}
    
    ** Example: **
    User Query: Give me info about Solana
    Expected Output: 
        {{
            "currencies_mentioned": ["solana"]
        }}
    
    User Query: Give me info about Shibu and ETH
    Expected Output: 
        {{
            "currencies_mentioned": ["shiba-inu", "ethereum"]
        }}
    
    ** NOTE:**
    1. Do not make any mistakes. Always double check before returning the output.

"""
                ),
            },
            {"role": "user", "content": user_query.strip()},
        ]

        # Call the Together API
        chat_completion = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3-8B-Instruct-Lite",
            messages=messages,
            temperature=0,
            max_tokens=200,
            top_p=1,
            stream=False,
            stop=None
        )

        # Extract the response
        extracted_text = chat_completion.choices[0].message.content
        logger.info(f"LLM Response: {extracted_text}")

        # Attempt to extract JSON from the response
        json_match = re.search(r"\{.*\}", extracted_text, re.DOTALL)
        if json_match:
            json_data = json.loads(json_match.group())
            currencies = json_data.get("currencies_mentioned", [])
        else:
            logger.warning("No valid JSON found in LLM response.")
            return []

        # Filter valid cryptocurrencies
        filtered_currencies = [crypto for crypto in currencies if crypto in valid_cryptos]
        return filtered_currencies

    except Exception as e:
        logger.error(f"Error extracting coin names: {e}", exc_info=True)
        return []

def generate_final_response(coin_data: dict, user_query: str) -> str:
    """
    Generates the final user response using LLM.

    Args:
        coin_data (dict): Fetched coin data.
        user_query (str): The user's original query.

    Returns:
        str: The final response generated by LLM.
    """
    try:
        # Prepare messages for LLM
        messages = [
            {"role": "user", "content": "Use the following data to answer the query:"},
            {"role": "user", "content": f"Coin Data: {coin_data}"},
            {"role": "user", "content": f"Query: {user_query}"},
        ]

        # Call the Together API
        chat_completion = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3-8B-Instruct-Lite",
            messages=messages,
            temperature=0,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None
        )
        response = chat_completion.choices[0].message.content
        logger.info("Final response generated successfully.")
        return response

    except Exception as e:
        logger.error(f"Error generating final response: {e}", exc_info=True)
        return "An error occurred while generating the response."
