# Approach and Implementation

## Approach

The cryptocurrency AI agent is designed to seamlessly handle user queries about cryptocurrency prices and rankings, even when provided in multiple languages. It integrates a large language model (LLM) with real-time data APIs, ensuring accurate and context-aware responses. The approach is divided into several logical steps to ensure efficiency, scalability, and user-friendliness.

### Key Components of the Approach:

1. **Multilingual Query Handling**:
   - The agent detects the input language and translates non-English queries into English using the Lecto Translation API.
   - This ensures consistent input for the LLM, reducing ambiguity and improving response accuracy.

2. **Context Management**:
   - User queries and responses are stored in a session-specific database to maintain conversational flow without cross-session interference.
   - Vector embeddings are generated and stored in Chroma DB for fast retrieval and enhanced context awareness.

3. **Cryptocurrency Data Retrieval**:
   - Real-time cryptocurrency prices and metadata are fetched from the CoinCap API.
   - The agent filters relevant data based on the user query and prepares it for response generation.

4. **LLM Integration for Processing**:
   - The Together AI's LLaMA-3.1-8B model is used to:
     - Extract cryptocurrency names mentioned in the query.
     - Generate concise and accurate responses using structured prompts.
   - Prompt engineering ensures the LLM understands the task, avoids hallucinations, and delivers structured output.

5. **Error Handling and Robustness**:
   - The agent handles invalid queries and API failures gracefully, returning helpful messages to users while logging issues for debugging.

---

## Implementation

The implementation follows a step-by-step process to handle user queries and generate responses. Below are the core steps:

### Step 1: Translate User Input to English (if Necessary)
The first step involves detecting the language of the user input and translating it into English if required.

```python
translated_query = detect_and_translate(user_input)
logger.info(f"Translated query: {translated_query}")
```

- **Translation Process**:
  - If the query is not in English, the Lecto Translation API translates it into English.
  - The translation ensures uniform processing by the LLM.

---

### Step 2: Retrieve Context from Past Queries
For continuity in conversations, the agent retrieves relevant context from the session-specific database.

```python
context = retrieve_context_for_query(translated_query)
```

- **Context Database**:
  - A CSV-based context DB stores previous query-response pairs.
  - Chroma DB is used to maintain vector embeddings of past interactions for quick retrieval.
  - This ensures the agent can answer follow-up queries accurately.

---

### Step 3: Extract Cryptocurrency Data from API
The agent identifies cryptocurrency names in the query and fetches their data from the CoinCap API.

```python
coin_data = process_user_query(translated_query, context)
```

- **Cryptocurrency Name Extraction**:
  - A predefined list of valid cryptocurrencies is used to match and extract names from the query.
  - This extraction process uses an LLM prompt to ensure accurate parsing.

- **API Integration**:
  - Data for the identified cryptocurrencies is retrieved from the CoinCap API in real-time.
  - If the API fails, fallback mechanisms log the error and return a default response.

---

### Step 4: Generate Response Using LLM
With the translated query, context, and cryptocurrency data, the agent generates the final response.

```python
final_response = generate_final_response(coin_data, translated_query)
```

- **Prompt Engineering**:
  - The prompt includes the cryptocurrency data, context, and user query, ensuring the LLM has all necessary information.
  - The response is structured to be user-friendly and accurate.

---

### Step 5: Save Query and Response for Context
Finally, the query and response are saved to the session-specific database for future reference.

```python
add_query_to_context(translated_query, final_response)
```

- **Session Management**:
  - This step ensures that the current interaction contributes to the session's ongoing context.
  - The stored data is used to maintain conversational flow and support follow-up queries.

---

## Summary of Workflow

1. **Input Handling**: Accept and translate multilingual queries into English.
2. **Context Retrieval**: Fetch relevant context from the session database.
3. **Cryptocurrency Data**: Identify cryptocurrencies mentioned in the query and retrieve their real-time data.
4. **Response Generation**: Use the LLM to generate context-aware, concise responses.
5. **Context Storage**: Store the query and response for future interactions.

