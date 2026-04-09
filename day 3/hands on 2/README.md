# Sentiment-Based Response Generator

A minimal web application that uses LangGraph for conditional branching based on sentiment analysis.

## Features

- **Sentiment Analysis**: Uses Hugging Face's DistilBERT model to classify text as positive, negative, or neutral.
- **Dynamic Routing**: LangGraph workflow routes queries to appropriate response generators.
- **Attractive UI**: Bootstrap-based responsive interface with animations.
- **Groq Integration**: Uses Groq API for generating contextual responses.

## Architecture

1. **Input**: User submits text via web form.
2. **Analysis**: Hugging Face pipeline analyzes sentiment.
3. **Routing**: LangGraph decision node routes to:
   - Positive → Encouraging response
   - Negative → Empathetic response
   - Neutral → Informative response
4. **Output**: Display generated response.

## Setup

1. Install dependencies:
   ```bash
   pip install flask langchain langchain-groq langgraph transformers torch
   ```

2. Run the app:
   ```bash
   python web.py
   ```

3. Open http://127.0.0.1:5000 in your browser.

## Workflow

The LangGraph workflow consists of:
- `analyze_sentiment`: Classifies sentiment using transformers.
- `decide`: Routes based on sentiment.
- `positive_response`, `negative_response`, `neutral_response`: Generate responses using Groq LLM.

## Optimization

- Lightweight DistilBERT model for fast sentiment analysis.
- Minimal token usage with short prompts.
- Efficient Flask app for simple deployment.