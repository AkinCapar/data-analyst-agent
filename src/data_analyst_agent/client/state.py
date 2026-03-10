from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages

class GraphState(TypedDict):
    """
    Represents the state of our data analyst graph.
    It holds the conversation history and the tool execution results.
    """
    messages: Annotated[list, add_messages]