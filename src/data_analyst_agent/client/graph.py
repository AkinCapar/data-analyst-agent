from dotenv import load_dotenv
load_dotenv()

from typing import Literal
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

from data_analyst_agent.client.state import GraphState
from data_analyst_agent.client.tools import get_database_schema, execute_sql_query, execute_python_chart_code


SYSTEM_MESSAGE = """You are a Senior Data Analyst AI.
You have access to a SQLite database containing the company's data.

Follow these strict rules:
1. ALWAYS use the 'get_database_schema' tool first to understand the tables and columns before writing ANY SQL.
2. DO NOT guess column names or table names. 
3. When writing SQL, only write SELECT queries.
4. If the 'execute_sql_query' tool returns an error, read the error message carefully, fix your SQL, and try again.
5. After getting the data, explain the results clearly and concisely to the user.
"""

tools_list = [get_database_schema, execute_sql_query, execute_python_chart_code]
llm = ChatOpenAI(model="gpt-5-mini", temperature=0)
llm_with_tools = llm.bind_tools(tools_list)

def call_model(state: GraphState):
    messages = state["messages"]
    
    if not any(isinstance(msg, SystemMessage) for msg in messages):
        messages = [SystemMessage(content=SYSTEM_MESSAGE)] + messages
        
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

workflow = StateGraph(GraphState)


workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode(tools_list))


workflow.add_edge(START, "agent")

workflow.add_conditional_edges("agent", tools_condition)

workflow.add_edge("tools", "agent")

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)