from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse, JSONResponse
import pandas as pd
import io
from langgraph.graph import StateGraph

# Simple ETL state model
class ETLState(dict):
    pass

# Extract: load CSV from upload
def extract(state: ETLState) -> ETLState:
    content = state["file_content"]
    df = pd.read_csv(io.StringIO(content))
    return {"data": df}

# Transform: clean the dataset
def transform(state: ETLState) -> ETLState:
    df = state["data"]
    df = df.dropna()
    df = df.drop_duplicates()
    df.columns = df.columns.str.lower().str.replace(" ", "_", regex=False)
    return {"data": df}

# Load: provide cleaned CSV stream
def load(state: ETLState) -> ETLState:
    df = state["data"]
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    return {"csv": buffer}

# Build workflow graph
graph = StateGraph(ETLState)
graph.add_node("extract", extract)
graph.add_node("transform", transform)
graph.add_node("load", load)
graph.add_edge("extract", "transform")
graph.add_edge("transform", "load")
graph.set_entry_point("extract")
compiled_graph = graph.compile()

app = FastAPI(title="Handson 2 ETL App")

@app.get("/")
def home():
    return {"status": "ready", "endpoint": "/upload"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    content = await file.read()
    state = {"file_content": content.decode("utf-8")}
    result = compiled_graph.invoke(state)
    csv_stream = result["csv"]
    return StreamingResponse(csv_stream, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=cleaned.csv"})

@app.post("/upload/json")
async def upload_json(file: UploadFile = File(...)):
    content = await file.read()
    state = {"file_content": content.decode("utf-8")}
    result = compiled_graph.invoke(state)
    df = pd.read_csv(result["csv"])
    return JSONResponse(content=df.to_dict(orient="records"))
