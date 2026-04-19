"""
Customer Support AI - Test Client
Examples using all 3 prompt patterns
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_react_pattern():
    """ReAct: Fast lookup queries"""
    query = "What's my order status for order #12345?"
    response = requests.post(f"{BASE_URL}/support", json={
        "query": query,
        "pattern": "react"
    })
    print("\n=== ReAct Pattern (Fast Lookup) ===")
    print(f"Query: {query}")
    print(f"Response: {response.json()['response']}")
    print(f"Tokens: {response.json()['tokens']}")


def test_cot_pattern():
    """CoT: Step-by-step reasoning"""
    query = "My app keeps timing out. I've already restarted, but it's still slow."
    response = requests.post(f"{BASE_URL}/support", json={
        "query": query,
        "pattern": "cot"
    })
    print("\n=== CoT Pattern (Troubleshooting) ===")
    print(f"Query: {query}")
    print(f"Response: {response.json()['response']}")
    print(f"Tokens: {response.json()['tokens']}")


def test_reflection_pattern():
    """Self-Reflection: Quality-critical response"""
    query = "Can I return my purchase after 90 days if it's unused?"
    response = requests.post(f"{BASE_URL}/support", json={
        "query": query,
        "pattern": "reflection"
    })
    print("\n=== Self-Reflection Pattern (Policy) ===")
    print(f"Query: {query}")
    print(f"Response: {response.json()['response']}")
    print(f"Tokens: {response.json()['tokens']}")


def test_batch():
    """Test batch query processing"""
    queries = [
        "How do I reset my password?",
        "What are your business hours?",
        "How do I cancel my subscription?"
    ]
    response = requests.post(f"{BASE_URL}/batch", json={
        "queries": queries,
        "pattern": "cot"
    })
    print("\n=== Batch Processing ===")
    for result in response.json()['results']:
        print(f"\nQ: {result['query']}")
        print(f"A: {result['response'][:100]}...")


def get_patterns():
    """Retrieve all available patterns"""
    response = requests.get(f"{BASE_URL}/patterns")
    print("\n=== Available Patterns ===")
    for pattern in response.json()['patterns']:
        print(f"\n{pattern['name'].upper()}")
        print(f"  Description: {pattern['description']}")
        print(f"  Use case: {pattern['use_case']}")


if __name__ == "__main__":
    print("Customer Support AI - Test Client")
    print("=" * 50)
    
    # Show available patterns
    get_patterns()
    
    # Run tests
    test_react_pattern()
    test_cot_pattern()
    test_reflection_pattern()
    test_batch()
    
    print("\n" + "=" * 50)
    print("Tests completed!")
