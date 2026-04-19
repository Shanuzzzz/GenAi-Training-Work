import streamlit as st
import os
from typing import TypedDict
from transformers import pipeline
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END

# --- CONFIGURATION & SETUP ---
# For this lab, the user provided their Groq API Key explicitly
GROQ_API_KEY = ""
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

st.set_page_config(page_title="Sentient Router", page_icon="🔀", layout="centered")

# --- UI STYLING (Colorful & Presentable) ---
st.markdown("""
    <style>
    /* Main Background Pattern */
    .stApp {
        background-color: #0e1117;
        background-image: radial-gradient(#262730 1px, transparent 1px);
        background-size: 20px 20px;
    }
    
    /* Elegant Title */
    h1 {
        text-align: center;
        background: -webkit-linear-gradient(45deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    hr {
        border: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, #4ECDC4, transparent);
    }

    /* Input Field Customization */
    div[data-baseweb="input"] {
        background-color: #1e212b;
        border: 1px solid #4ECDC4;
        border-radius: 10px;
    }

    /* Stylish Button */
    .stButton > button {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
        color: white;
        font-weight: bold;
        border-radius: 20px;
        border: none;
        width: 100%;
        padding: 0.5rem 1rem;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.6);
        color: #fff;
    }

    /* Output Card / Glassmorphism */
    .result-card {
        background: rgba(30, 33, 43, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 25px;
        margin-top: 20px;
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    /* Badges */
    .badge {
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 15px;
    }
    .badge-positive { background-color: rgba(78, 205, 196, 0.2); color: #4ECDC4; border: 1px solid #4ECDC4; }
    .badge-neutral { background-color: rgba(255, 230, 109, 0.2); color: #FFE66D; border: 1px solid #FFE66D; }
    .badge-negative { background-color: rgba(255, 107, 107, 0.2); color: #FF6B6B; border: 1px solid #FF6B6B; }
    </style>
""", unsafe_allow_html=True)

# --- STATE DEFINITION ---
class WorkflowState(TypedDict):
    user_input: str
    sentiment: str
    response: str
    handler_used: str

# --- INITIALIZE MODELS ---
# Cache the HF pipeline to avoid reloading on every Streamlit run
@st.cache_resource
def load_sentiment_model():
    # Utilizing a lightweight distilled model that yields positive/neutral/negative
    return pipeline("sentiment-analysis", model="lxyuan/distilbert-base-multilingual-cased-sentiments-student", return_all_scores=False)

sentiment_pipeline = load_sentiment_model()

# Initialize lightweight, lightning-fast Groq LLM
llm = ChatGroq(temperature=0.3, model_name="llama3-8b-8192")

# --- LANGGRAPH NODES ---
def analyze_sentiment(state: WorkflowState):
    """Determines sentiment using lightweight HF model."""
    result = sentiment_pipeline(state['user_input'])[0]
    sentiment_label = result['label'].lower() # 'positive', 'neutral', 'negative'
    return {"sentiment": sentiment_label}

def pos_handler(state: WorkflowState):
    """Handles positive sentiment queries."""
    msg = llm.invoke([
        SystemMessage(content="You are a helpful AI. The user is feeling positive. Respond with brief, upbeat enthusiasm. Max 2 sentences."),
        HumanMessage(content=state['user_input'])
    ])
    return {"response": msg.content, "handler_used": "pos_handler (Enthusiastic Route)"}

def neu_handler(state: WorkflowState):
    """Handles neutral sentiment queries."""
    msg = llm.invoke([
        SystemMessage(content="You are a factual AI. The user is asking a standard query. Provide a direct, concise, and clear response. Max 2 sentences."),
        HumanMessage(content=state['user_input'])
    ])
    return {"response": msg.content, "handler_used": "neu_handler (Direct Route)"}

def neg_handler(state: WorkflowState):
    """Handles negative sentiment queries."""
    msg = llm.invoke([
         SystemMessage(content="You are an empathetic AI. The user may be frustrated or upset. Acknowledge their feeling briefly, and provide concise help. Max 2 sentences."),
         HumanMessage(content=state['user_input'])
    ])
    return {"response": msg.content, "handler_used": "neg_handler (Empathetic Route)"}

# --- LANGGRAPH EDGES (ROUTING LOGIC) ---
def route_sentiment(state: WorkflowState):
    """Returns the next node based on sentiment."""
    return state["sentiment"]

# --- COMPILE WORKFLOW ---
@st.cache_resource
def build_workflow():
    workflow = StateGraph(WorkflowState)
    
    # Add Nodes
    workflow.add_node("analyze_sentiment", analyze_sentiment)
    workflow.add_node("positive", pos_handler)
    workflow.add_node("neutral", neu_handler)
    workflow.add_node("negative", neg_handler)
    
    # Connect Graph
    workflow.add_edge(START, "analyze_sentiment")
    
    # Conditional Branching
    workflow.add_conditional_edges(
        "analyze_sentiment",
        route_sentiment,
        {
            "positive": "positive",
            "neutral": "neutral",
            "negative": "negative"
        }
    )
    
    workflow.add_edge("positive", END)
    workflow.add_edge("neutral", END)
    workflow.add_edge("negative", END)
    
    return workflow.compile()

graph_app = build_workflow()

# --- STREAMLIT UI LAYOUT ---
st.markdown("<h1>🔀 Sentient Router Workflow</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a1a1aa;'>Dynamic conditional routing based on distilled HF sentiment analysis.</p>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# Input Section
st.write("### What's on your mind?")
user_text = st.text_input("Enter your text below:", placeholder="e.g., 'I absolutely love this new feature!' or 'This is so frustrating to use.'", label_visibility="collapsed")

if st.button("Process Route 🚀"):
    if user_text.strip():
        with st.spinner("Analyzing sentiment and routing..."):
            initial_state = {"user_input": user_text}
            result_state = graph_app.invoke(initial_state)
            
            # Display Results
            st.markdown("<div class='result-card'>", unsafe_allow_html=True)
            
            # Badge rendering
            sentiment = result_state['sentiment']
            badge_class = f"badge-{sentiment}"
            st.markdown(f"<div class='badge {badge_class}'>🔍 Detected Sentiment: {sentiment.upper()}</div>", unsafe_allow_html=True)
            
            st.write(f"**🛣️ Route Taken:** `{result_state['handler_used']}`")
            st.write(f"**🤖 AI Response:**")
            st.write(f"_{result_state['response']}_")
            
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please enter some text to begin.")

# Instructions / Footer
with st.expander("ℹ️ How it works (Architecture)"):
    st.markdown("""
    **Architecture Diagram:**
    1. **Input:** User query.
    2. **Sentiment Node:** Local Hugging Face Model (`distilbert-base-multilingual-cased-sentiments-student`).
    3. **Router:** LangGraph conditional edge dynamically routes to one of three handlers.
    4. **Handlers:** Specialized system prompts executed via **Llama-3-8b** on Groq for ultra-low latency generation.
    """)
