# Customer Support AI - Minimal Prompt Templates

## 1. ReAct Pattern (Reason + Act with Tools)

**Definition:** Reason through available tools, then act on them to resolve customer issues.

### Template
```
You are a support agent. Reason about the issue, then use tools.

Customer: {query}

Reasoning:
- Identify issue type
- Determine tool needed

Tool Call: [tool_name] with {params}
Response: {answer}
```

**When to use:** FAQs with lookups, account checks, order status, password resets, API integrations.

---

## 2. Chain-of-Thought (CoT) Pattern

**Definition:** Break down reasoning into clear, sequential steps before answering.

### Template
```
You are a support agent. Think step-by-step.

Customer: {query}

Step 1: Understand the issue
Step 2: Identify root cause
Step 3: Provide solution

Answer: {response}
Confidence: {level}
```

**When to use:** Complex troubleshooting, multi-step problems, technical issues requiring explanation.

---

## 3. Self-Reflection Pattern

**Definition:** Generate an answer, review it, then improve if needed.

### Template
```
You are a support agent. Answer, then review.

Customer: {query}

Initial Response: {answer}

Review:
- Is it accurate? [Yes/No]
- Missing info? [list]
- Refine? [Yes/No]

Final Response: {improved_answer}
```

**When to use:** Sensitive issues, complex policies, customized solutions, high-value customers.

---

## Usage Summary

| Pattern | Latency | Tokens | Best For |
|---------|---------|--------|----------|
| **ReAct** | Fast | Low | Straightforward lookups |
| **CoT** | Medium | Medium | Troubleshooting |
| **Self-Reflection** | Slow | High | Quality-critical responses |

## Implementation Tips
- Strip whitespace and redundant phrases from templates
- Use variable placeholders instead of examples
- Combine patterns for complex workflows
- Monitor token count per query
