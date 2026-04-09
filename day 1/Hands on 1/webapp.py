import os
from openai import OpenAI
import requests
import json
from flask import Flask, request, render_template_string

app = Flask(__name__)

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

def react_agent(question, max_steps=10):
    scratchpad = f"Question: {question}\nYou are a ReAct agent. Use the following format:\nThought: [your reasoning]\nAction: Search[query] or Final Answer: [answer]\nObservation: [result if action taken]\n\n"
    for step in range(max_steps):
        prompt = scratchpad + "Thought: "
        try:
            resp = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0
            )
            output = resp.choices[0].message.content.strip()
        except Exception as e:
            return f"API error: {str(e)}"
        
        if "Final Answer:" in output:
            return output.split("Final Answer:")[-1].strip()
        
        # Parse the output
        lines = output.split('\n')
        thought = ""
        action = ""
        for line in lines:
            if line.startswith("Thought:"):
                thought = line[8:].strip()
            elif line.startswith("Action:"):
                action = line[7:].strip()
        
        if action.startswith("Search[") and action.endswith("]"):
            query = action[7:-1]
            obs = web_search(query)
            scratchpad += f"Thought: {thought}\nAction: {action}\nObservation: {obs}\n"
        elif action.startswith("Final Answer:"):
            return action[13:].strip()
        else:
            scratchpad += f"Thought: {output}\n"
    return "Max steps reached. No answer."

@app.route('/', methods=['GET', 'POST'])
def home():
    answer = None
    if request.method == 'POST':
        question = request.form['question']
        answer = react_agent(question)
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>ReAct Agent</title>
    </head>
    <body>
        <h1>ReAct Agent Web App</h1>
        <form method="post">
            <label for="question">Enter your question:</label><br>
            <input type="text" id="question" name="question" required><br>
            <input type="submit" value="Ask">
        </form>
        {% if answer %}
        <h2>Answer:</h2>
        <p>{{ answer }}</p>
        {% endif %}
    </body>
    </html>
    ''', answer=answer)

if __name__ == '__main__':
    app.run(debug=False)