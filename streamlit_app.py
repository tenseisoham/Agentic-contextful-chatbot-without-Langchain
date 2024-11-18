
import streamlit as st
import logging
from chat.context_manager import add_query_to_context, retrieve_context_for_query
from chat.query_processor import process_user_query
from chat.llm_agent import generate_final_response
from utils.translation import detect_and_translate
import uuid
from datetime import datetime

# Configure logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Streamlit Page Configuration
st.set_page_config(page_title="Chatbot", layout="wide")

# Ensure a unique session ID for the user session
if "session_id" not in st.session_state:
    st.session_state["session_id"] = f"session_{uuid.uuid4().hex[:8]}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    logger.info(f"Session ID initialized: {st.session_state['session_id']}")

# Initialize Session State for Context and Chat History
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []  # Holds the conversation
    st.session_state["context"] = None  # For persistent context during the session

# Page Title
st.title("💬 Cryptocurrency Chatbot")
st.caption("Ask questions about cryptocurrency prices, ranks, and more!")

def handle_user_input(user_input: str) -> str:
    """
    Handles the user input and generates a response.
    
    Args:
        user_input (str): The user's input message.
    
    Returns:
        str: The bot's response.
    """
    if not isinstance(user_input, str) or not user_input.strip():
        st.error("Invalid input. Please enter a valid query.")
        return ""

    try:
        # Step 1: Translate user input to English if necessary
        translated_query = detect_and_translate(user_input)
        logger.info(f"Translated query: {translated_query}")

        # Step 2: Retrieve context from past queries
        context = retrieve_context_for_query(translated_query)  # Uses session-specific DB

        # Step 3: Extract cryptocurrency data from API
        coin_data = process_user_query(translated_query, context)

        # Step 4: Generate response using LLM
        final_response = generate_final_response(coin_data, translated_query)

        # Step 5: Save query and response for context
        add_query_to_context(translated_query, final_response)  # Uses session-specific DB

        # Step 6: Append to chat history for display
        st.session_state["chat_history"].append({"user": user_input, "bot": final_response})

        return final_response

    except Exception as e:
        logger.error(f"Error handling user input: {e}", exc_info=True)
        return "I'm sorry, something went wrong. Please try again."

# Chat Interface
st.write("### Chat with the Bot")

# Display Chat History
for chat in st.session_state["chat_history"]:
    with st.chat_message("user"):
        st.markdown(chat["user"])
    with st.chat_message("bot"):
        st.markdown(chat["bot"])

# Input Box for New User Queries
if prompt := st.chat_input("Type your message..."):
    with st.chat_message("user"):
        st.markdown(prompt)  # Display the user's message in the chat

    # Generate and display bot response
    with st.spinner("Generating response..."):
        try:
            response = handle_user_input(prompt)
        except Exception as e:
            response = "I'm sorry, something went wrong. Please try again."
            st.error(f"Error: {str(e)}")

    with st.chat_message("bot"):
        st.markdown(response)  # Display the bot's response in the chat
