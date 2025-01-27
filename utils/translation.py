

import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# API key for Lecto
LECTO_API_KEY = "LECTO_API_KEY" # please use my lecto api key listed down for language translation

def detect_and_translate(text: str, target_language: str = "en") -> str:
    """
    Detects the language of the given text and translates it to English if necessary.

    Args:
        text (str): The input text to be checked and translated.
        target_language (str): The language to translate the text into. Defaults to English ("en").

    Returns:
        str: The translated text in the target language.
    """
    if not isinstance(text, str) or not text.strip():
        logger.warning("Invalid input text provided for translation.")
        return ""  # Return empty string if input is invalid

    # API endpoint for Lecto
    url = "https://api.lecto.ai/v1/translate/text"
    payload = {
        "texts": [text],  # Wrap the text in a list as per the API spec
        "to": [target_language],
    }
    headers = {
        "X-API-Key": LECTO_API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        translation_result = response.json()

        # Extract the translated text properly
        translations = translation_result.get("translations", [])
        if translations and isinstance(translations[0], str):
            logger.info("Translation successful.")
            return translations[0].strip()
        else:
            logger.warning("Unexpected response format from Lecto API: %s", translation_result)
            return text.strip()  # Fallback to the original text

    except requests.exceptions.RequestException as e:
        logger.error(f"Error during translation: {e}", exc_info=True)
        return text.strip()
