from langgraph.graph import StateGraph
from langgraph.constants import END
from typing import TypedDict
import pandas as pd

class ETLState(TypedDict):
    data: pd.DataFrame
    source: pd.DataFrame

def extract(state):
    src = state["source"]
    if not isinstance(src, pd.DataFrame):
        raise ValueError("extract expects a DataFrame input")
    state["data"] = src.copy()
    return state

def transform(state):
    df = state["data"].copy()
    df = df.fillna(method="ffill").fillna(method="bfill").fillna(0)
    df = df.drop_duplicates().reset_index(drop=True)
    state["data"] = df
    return state

def load(state):
    from io import BytesIO
    buffer = BytesIO()
    state["data"].to_csv(buffer, index=False)
    buffer.seek(0)
    state["output"] = buffer
    return state

graph = StateGraph(ETLState)
graph.add_node("extract", extract)
graph.add_node("transform", transform)
graph.add_node("load", load)
graph.set_entry_point("extract")
graph.add_edge("extract", "transform")
graph.add_edge("transform", "load")
graph.add_edge("load", END)
etl_graph = graph.compile()