import os
from flask import Flask, render_template, request
from langgraph.graph import StateGraph
from langchain_groq import ChatGroq
from transformers import pipeline
from typing import TypedDict

app = Flask(__name__)

# Define the workflow state
class WorkflowState(TypedDict):
    text: str
    sentiment: str
    response: str

# Sentiment analysis node
def analyze_sentiment(state: WorkflowState):
    sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    result = sentiment_pipeline(state["text"])[0]
    label = result["label"].lower()
    if label == "positive":
        sentiment = "positive"
    elif label == "negative":
        sentiment = "negative"
    else:
        sentiment = "neutral"
    return {"sentiment": sentiment}

# Decision node
def decide(state: WorkflowState):
    if state["sentiment"] == "positive":
        return "positive_response"
    elif state["sentiment"] == "negative":
        return "negative_response"
    else:
        return "neutral_response"

# Response nodes
def positive_response(state: WorkflowState):
    llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model="llama-3.1-8b-instant")
    prompt = f"Generate a short, encouraging response based on this positive sentiment text: {state['text']}"
    response = llm.invoke(prompt)
    return {"response": response.content}

def negative_response(state: WorkflowState):
    llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model="llama-3.1-8b-instant")
    prompt = f"Generate a short, empathetic and supportive response based on this negative sentiment text: {state['text']}"
    response = llm.invoke(prompt)
    return {"response": response.content}

def neutral_response(state: WorkflowState):
    llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model="llama-3.1-8b-instant")
    prompt = f"Generate a short, informative response based on this neutral sentiment text: {state['text']}"
    response = llm.invoke(prompt)
    return {"response": response.content}

# Build the graph
graph = StateGraph(WorkflowState)
graph.add_node("analyze", analyze_sentiment)
graph.add_node("positive", positive_response)
graph.add_node("negative", negative_response)
graph.add_node("neutral", neutral_response)
graph.add_conditional_edges("analyze", decide, {"positive_response": "positive", "negative_response": "negative", "neutral_response": "neutral"})
graph.set_entry_point("analyze")
workflow_app = graph.compile()

@app.route('/', methods=['GET', 'POST'])
def index():
    response = None
    if request.method == 'POST':
        text = request.form.get('text', '')
        if text:
            result = workflow_app.invoke({"text": text})
            response = result['response']
    return render_template('index.html', response=response)

if __name__ == '__main__':
    app.run(debug=True)
