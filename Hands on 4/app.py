import streamlit as st
import os
from typing import TypedDict
from langgraph import StateGraph
from langchain_openai import ChatOpenAI
import chromadb
from chromadb.utils import embedding_functions

# Set up LangSmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = ""

# Define State
class State(TypedDict):
    query: str
    docs: list
    draft: str
    final: str

# Initialize ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="docs")

# Add sample documents
docs = [
    "Artificial Intelligence (AI) is a field of computer science that aims to create machines capable of intelligent behavior.",
    "Multi-agent systems involve multiple autonomous agents that interact to achieve goals.",
    "LangGraph is a library for building stateful, multi-actor applications with LLMs.",
    "Retrieval-Augmented Generation (RAG) combines retrieval and generation for better responses.",
    "ChromaDB is a vector database for storing and retrieving embeddings."
]
collection.add(documents=docs, ids=[str(i) for i in range(len(docs))])

# Initialize OpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Define Agents
def researcher(state: State) -> State:
    query = state["query"]
    results = collection.query(query_texts=[query], n_results=3)
    docs = results["documents"][0]
    return {"docs": docs}

def writer(state: State) -> State:
    docs = "\n".join(state["docs"])
    query = state["query"]
    prompt = f"Write a structured draft report on '{query}' based on this context:\n\n{docs}\n\nKeep it concise."
    response = llm.invoke(prompt)
    draft = response.content
    return {"draft": draft}

def editor(state: State) -> State:
    draft = state["draft"]
    query = state["query"]
    prompt = f"Refine and format this draft report on '{query}'. Make it professional and coherent:\n\n{draft}"
    response = llm.invoke(prompt)
    final = response.content
    return {"final": final}

# Build Graph
graph = StateGraph(State)
graph.add_node("researcher", researcher)
graph.add_node("writer", writer)
graph.add_node("editor", editor)
graph.add_edge("researcher", "writer")
graph.add_edge("writer", "editor")
graph.set_entry_point("researcher")
app = graph.compile()

# Streamlit UI
st.set_page_config(page_title="Multi-Agent Research Pipeline", page_icon="🔍", layout="wide")

# Custom CSS for colors
st.markdown("""
<style>
    .main {background-color: #f0f2f6;}
    .stTextInput > div > div > input {background-color: #ffffff; border: 2px solid #4CAF50;}
    .stButton > button {background-color: #4CAF50; color: white; border: none; padding: 10px 20px; border-radius: 5px;}
    .stButton > button:hover {background-color: #45a049;}
    .report-section {background-color: #ffffff; padding: 20px; border-radius: 10px; margin: 10px 0; box-shadow: 0 4px 8px rgba(0,0,0,0.1);}
</style>
""", unsafe_allow_html=True)

st.title("🔍 Multi-Agent Research Pipeline")
st.markdown("A token-efficient system using LangGraph, OpenAI, and ChromaDB for high-quality report generation.")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Input Query")
    query = st.text_input("Enter your research query:", placeholder="e.g., What is AI?")
    generate_button = st.button("🚀 Generate Report", use_container_width=True)

with col2:
    st.subheader("System Architecture")
    st.markdown("""
    - **Researcher**: Retrieves relevant documents using ChromaDB vector search
    - **Writer**: Generates a structured draft from retrieved context
    - **Editor**: Refines and formats the final report
    """)
    st.image("https://via.placeholder.com/400x200/4CAF50/FFFFFF?text=Agent+Workflow", caption="Agent Workflow Diagram")

if generate_button and query:
    progress_bar = st.progress(0)
    status_text = st.empty()

    # Initialize state
    state = {"query": query, "docs": [], "draft": "", "final": ""}

    # Researcher step
    status_text.text("🔎 Researching relevant information...")
    progress_bar.progress(25)
    result = researcher(state)
    state.update(result)

    # Writer step
    status_text.text("✍️ Generating draft report...")
    progress_bar.progress(50)
    result = writer(state)
    state.update(result)

    # Editor step
    status_text.text("📝 Refining final report...")
    progress_bar.progress(75)
    result = editor(state)
    state.update(result)

    progress_bar.progress(100)
    status_text.text("✅ Report generation complete!")

    # Display results
    st.success("Report generated successfully!")

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.expander("📄 Retrieved Documents", expanded=True):
            st.markdown('<div class="report-section">', unsafe_allow_html=True)
            for i, doc in enumerate(state["docs"], 1):
                st.markdown(f"**Document {i}:** {doc}")
            st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        with st.expander("📝 Draft Report", expanded=True):
            st.markdown('<div class="report-section">', unsafe_allow_html=True)
            st.write(state["draft"])
            st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        with st.expander("🎯 Final Report", expanded=True):
            st.markdown('<div class="report-section">', unsafe_allow_html=True)
            st.write(state["final"])
            st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("Enter a query and click 'Generate Report' to start the multi-agent pipeline.")

st.markdown("---")
st.markdown("**Built with:** LangGraph, OpenAI GPT-3.5-turbo, ChromaDB, Streamlit")
st.markdown("**Optimized for:** Token efficiency, clear agent separation, scalable architecture")