
# Cryptocurrency AI Agent Assignment

[![Architecture](./assets/architecture.png)](./assets/architecture.JPG)

This repository contains my submission for the AI Agent Assignment, designed to demonstrate the implementation of a cryptocurrency chatbot with Together AI's LLaMA 3.1 8B model. It fetches live cryptocurrency prices, handles multilingual user queries, and maintains conversational context.

---

## 📋 Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Setup Instructions](#setup-instructions)
4. [Documentation](#documentation)
5. [Acknowledgments](#acknowledgments)

---

## 🔍 Overview
This project showcases:
- Integration with **Together AI's LLaMA 3.1 8B** model for conversational abilities.
- **Public Cryptocurrency APIs** for fetching real-time cryptocurrency prices.
- Handling **multilingual inputs**, translating queries into English while maintaining system responses in English.
- Context retention across multiple user interactions.

This project is developed as part of an assignment to deepen understanding of LLMs, API integration, and conversational AI systems.

---

## 🌟 Features
### Core Features:
1. Fetch live cryptocurrency prices (e.g., Bitcoin, Ethereum).
2. Maintain query context for natural conversational flow.
3. Robust error handling for invalid inputs and API failures.

### Bonus Features:
1. Multilingual support: Translate user queries into English and respond accordingly.
2. API rate limiting and caching for optimized performance.

---

## 🛠️ Setup Instructions
Follow these steps to set up the project locally:

### 1. Clone the Repository
```bash
git clone https://github.com/your-assignment-repo/crypto-ai-agent.git
cd crypto-ai-agent
```

### 2. Create a Virtual Environment
Use Conda to create and activate a Python 3.11.8 environment:
```bash
conda create -n crypto-agent python=3.11.8
conda activate crypto-agent
```

### 3. Install Dependencies
Install required Python packages:
```bash
pip install -r requirements.txt
```

### 4. Configure API Keys
Add your API keys:
- **Together AI API Key** in `chat/llm_agent.py`:
  ```python
  TOGETHER_API_KEY = "your_together_api_key_here"
  ```
- **Lecto API Key** in `utils/translation.py`:
  ```python
  LECTO_API_KEY = "FQPKAF3-ANCM7VR-H3QT99G-3RRYF6H"
  ```

---

## 📚 Documentation
Detailed implementation and design documentation is available [here](./docs/README.md).

---

## 🙏 Acknowledgments
I would like to thank **Sarvam.ai** for crafting this wonderful assignment. It has significantly deepened my understanding of:
1. Working with Together AI API.
2. API integrations and prompt engineering.
3. Building end-to-end conversational AI agents.

---

## 💡 Notes
- This submission is structured to demonstrate the ability to build an AI agent from scratch, without using libraries like LangChain.
- Any additional questions or clarifications can be discussed upon request.
