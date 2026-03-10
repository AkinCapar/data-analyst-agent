# 📊 AI Data Analyst Agent

An autonomous, agentic Data Analyst built with **LangGraph**, **Streamlit**, and **OpenAI**. This agent doesn't just chat; it actively explores a SQLite database, writes and executes SQL queries, self-corrects its errors, and generates dynamic data visualizations.

## 🌟 Key Features

* **🧠 Agentic Reasoning (ReAct):** Powered by native Tool Calling, the agent decides when to check the schema, when to query data, and when to draw charts without rigid rule-based programming.
* **💾 Persistent Memory:** Utilizes LangGraph's `MemorySaver` checkpointer. The agent remembers previous queries, allowing for highly contextual follow-up questions.
* **⚡ Real-Time Streaming UI:** Built with Streamlit, the frontend streams the agent's internal thought processes, node transitions, and tool executions in real-time.

## 🏗️ Architecture

The core logic is driven by a **LangGraph StateGraph** consisting of two main nodes:
1.  **Agent Node (`call_model`):** The LLM (`gpt-5-mini`) evaluates the user's request and the conversation history to either generate a final text response or invoke a tool.
2.  **Tools Node (`ToolNode`):** A secure execution environment containing three custom tools:
    * `get_database_schema`: Retrieves table structures and column types.
    * `execute_sql_query`: Runs read-only (`SELECT`) queries against the SQLite database.
    * `execute_python_chart_code`: Runs LLM-generated visualization code.

## 🛠️ Tech Stack

* **Framework:** LangChain/Langgraph
* **LLM:** OpenAI (`gpt-5-mini`)
* **UI:** Streamlit
* **Database:** SQLite (Superstore Sales Dataset)
* **Data Manipulation & Visualization:** Pandas, Matplotlib
* **Package Manager:** `uv`

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python installed, and have a .csv dataset in data folder.

### 2. Dependencies
langchain-openai langgraph streamlit pandas matplotlib tabulate python-dotenv