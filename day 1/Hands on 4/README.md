# Customer Support AI - Quick Start

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set environment (or use .env)
set GROQ_API_KEY=your_api_key

# 3. Run the app
python app.py
```

## API Endpoints

### Get Patterns
```
GET http://localhost:5000/patterns
```

### Single Query (with pattern selection)
```
POST http://localhost:5000/support
{
  "query": "How do I reset my password?",
  "pattern": "react"
}
```

### Batch Queries
```
POST http://localhost:5000/batch
{
  "queries": [
    "What is your return policy?",
    "How do I track my order?"
  ],
  "pattern": "cot"
}
```

## Pattern Guide

| Pattern | Use Case | Example |
|---------|----------|---------|
| **react** | Quick lookups, FAQs | Order status, account checks |
| **cot** | Complex issues | Troubleshooting, explanations |
| **reflection** | Quality-critical | Sensitive policies, disputes |

## Example Requests

### ReAct - Fast Lookup
```json
{
  "query": "What's my order status?",
  "pattern": "react"
}
```

### CoT - Troubleshooting
```json
{
  "query": "My app keeps crashing on startup",
  "pattern": "cot"
}
```

### Self-Reflection - Quality Response
```json
{
  "query": "Can I return an item after 60 days?",
  "pattern": "reflection"
}
```

## Token Optimization

- **ReAct**: ~80-120 tokens (fastest)
- **CoT**: ~150-250 tokens (balanced)
- **Reflection**: ~200-350 tokens (most thorough)

Switch patterns based on query complexity to minimize costs.

## Deployment

Use Flask with Gunicorn in production:
```bash
pip install gunicorn
gunicorn -w 4 app:app
```

## Monitoring

Check `/admin/config` for current model, max tokens, and available patterns.
