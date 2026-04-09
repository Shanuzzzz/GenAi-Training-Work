import os
from openai import OpenAI
import requests
import json

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def web_search(query):
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json"
        resp = requests.get(url, timeout=5)
        data = resp.json()
        return data.get('AbstractText', 'No summary found.')
    except Exception as e:
        return f"Search error: {str(e)}"

def react_agent(question, max_steps=5):
    scratchpad = f"Question: {question}\n"
    for step in range(max_steps):
        prompt = f"You are a ReAct agent. {scratchpad}Thought: "
        try:
            resp = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0
            )
            output = resp.choices[0].message.content.strip()
        except Exception as e:
            return f"API error: {str(e)}"
        
        if "Final Answer:" in output:
            return output.split("Final Answer:")[-1].strip()
        
        if "Action:" in output:
            action_part = output.split("Action:")[-1].strip()
            if action_part.startswith("Search["):
                query = action_part[7:-1]
                obs = web_search(query)
                scratchpad += f"Thought: {output.split('Action:')[0].strip()}\nAction: {action_part}\nObservation: {obs}\n"
            else:
                scratchpad += f"Thought: {output}\n"
        else:
            scratchpad += f"Thought: {output}\n"
    return "Max steps reached. No answer."

# Example usage
print(react_agent("What is the capital of France?"))