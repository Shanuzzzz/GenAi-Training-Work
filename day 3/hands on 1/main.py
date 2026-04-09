from typing import TypedDict
import pandas as pd
import io
import json
from langgraph.graph import StateGraph
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

# Define the ETL State
class ETLState(TypedDict):
    file_content: str
    data: pd.DataFrame
    output: str

# Extract function: Load CSV into Pandas DataFrame
def extract(state: ETLState) -> ETLState:
    content = state['file_content']
    df = pd.read_csv(io.StringIO(content))
    return {"data": df}

# Transform function: Clean the data
def transform(state: ETLState) -> ETLState:
    df = state['data']
    # Handle missing values: drop rows with any NaN
    df = df.dropna()
    # Drop duplicates
    df = df.drop_duplicates()
    # Standardize column names: lower case, replace spaces with _
    df.columns = df.columns.str.lower().str.replace(' ', '_', regex=False)
    return {"data": df}

# Load function: Convert to JSON string
def load(state: ETLState) -> ETLState:
    df = state['data']
    # Convert DataFrame to JSON
    json_str = df.to_json(orient='records')
    return {"output": json_str}

# Create the LangGraph workflow
graph = StateGraph(ETLState)
graph.add_node("extract", extract)
graph.add_node("transform", transform)
graph.add_node("load", load)
graph.add_edge("extract", "transform")
graph.add_edge("transform", "load")
graph.set_entry_point("extract")
compiled_graph = graph.compile()

# FastAPI app
app = FastAPI(title="ETL Pipeline Web App", description="Upload CSV, process through ETL, get cleaned JSON")

@app.get("/")
def read_root():
    return {"message": "ETL Web App is running. Use POST /upload to upload a CSV file."}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a CSV file, process it through the ETL pipeline, and return cleaned data as JSON.
    """
    content = await file.read()
    content_str = content.decode('utf-8')
    initial_state = {"file_content": content_str}
    final_state = compiled_graph.invoke(initial_state)
    output = final_state['output']
    # Return as JSON response
    return JSONResponse(content=json.loads(output))