"""
Customer Support AI Web App - Groq Integration
Implements ReAct, CoT, and Self-Reflection patterns
"""

from flask import Flask, request, jsonify
from groq import Groq
import os
from datetime import datetime
import json

app = Flask(__name__)

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY", ))

# Pattern templates (ultra-concise)
PATTERNS = {
    "react": """You are a support agent. Reason, then act.
Issue: {query}
Reasoning: Identify issue type and required action.
Action: Resolve based on tool availability.
Response: Clear, direct answer.""",
    
    "cot": """You are a support agent. Think step-by-step.
Issue: {query}
Step 1: Understand the problem
Step 2: Identify root cause
Step 3: Provide solution
Answer: Clear explanation with reasoning.""",
    
    "reflection": """You are a support agent. Answer then review.
Issue: {query}
Initial: Generate response
Review: Check accuracy and completeness
Final: Provide improved answer."""
}

# Tool functions (mock implementations)
TOOLS = {
    "lookup_faq": lambda q: f"FAQ result for: {q}",
    "check_account": lambda user: f"Account status for: {user}",
    "get_order_status": lambda order_id: f"Order {order_id}: In Transit",
    "troubleshoot": lambda issue: f"Troubleshooting steps for: {issue}"
}


def call_groq(prompt: str, pattern: str, model: str = "llama-3.1-8b-instant") -> dict:
    """Call Groq API with specified pattern"""
    try:
        message = client.chat.completions.create(
            model=model,
            max_tokens=512,  # Minimal tokens
            messages=[{"role": "user", "content": prompt}]
        )
        return {
            "success": True,
            "response": message.choices[0].message.content,
            "tokens_used": message.usage.total_tokens if hasattr(message, 'usage') else "N/A"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.route('/', methods=['GET'])
def health():
    """Health check"""
    return {"status": "running", "patterns": list(PATTERNS.keys())}


@app.route('/support', methods=['POST'])
def support_query():
    """Process customer support queries"""
    data = request.json
    query = data.get("query", "")
    pattern = data.get("pattern", "cot")  # Default: CoT
    
    if not query:
        return {"error": "Query required"}, 400
    
    if pattern not in PATTERNS:
        return {"error": f"Pattern must be: {list(PATTERNS.keys())}"}, 400
    
    # Build prompt
    prompt = PATTERNS[pattern].format(query=query)
    
    # Call Groq
    result = call_groq(prompt, pattern)
    
    return {
        "query": query,
        "pattern": pattern,
        "response": result.get("response", "Error"),
        "tokens": result.get("tokens_used", 0),
        "timestamp": datetime.now().isoformat()
    }


@app.route('/patterns', methods=['GET'])
def get_patterns():
    """Get all available patterns"""
    return {
        "patterns": [
            {
                "name": "react",
                "description": "Reason + Act with tools",
                "use_case": "Lookups, API checks, status queries",
                "template": PATTERNS["react"]
            },
            {
                "name": "cot",
                "description": "Chain-of-Thought step-by-step",
                "use_case": "Troubleshooting, complex reasoning",
                "template": PATTERNS["cot"]
            },
            {
                "name": "reflection",
                "description": "Answer + Review + Improve",
                "use_case": "Sensitive issues, quality-critical",
                "template": PATTERNS["reflection"]
            }
        ]
    }


@app.route('/batch', methods=['POST'])
def batch_queries():
    """Process multiple queries efficiently"""
    data = request.json
    queries = data.get("queries", [])
    pattern = data.get("pattern", "cot")
    
    results = []
    for q in queries[:10]:  # Max 10 queries per batch
        prompt = PATTERNS[pattern].format(query=q)
        result = call_groq(prompt, pattern)
        results.append({
            "query": q,
            "response": result.get("response", "Error"),
            "success": result.get("success", False)
        })
    
    return {
        "batch_size": len(results),
        "pattern": pattern,
        "results": results
    }


@app.route('/admin/config', methods=['GET'])
def get_config():
    """Get current configuration (patterns only, no keys)"""
    return {
        "model": "llama-3.1-8b-instant",
        "max_tokens": 512,
        "patterns": list(PATTERNS.keys()),
        "tools": list(TOOLS.keys())
    }


if __name__ == '__main__':
    app.run(debug=True, port=5000)
