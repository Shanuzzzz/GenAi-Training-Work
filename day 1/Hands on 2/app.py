from flask import Flask, request, render_template_string
import requests
import re
import os

API_KEY = os.getenv("GROQ_API_KEY")
BASE_URL = "https://api.groq.com/openai/v1"

app = Flask(__name__)

TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Math CoT Solver</title>
  <style>
    body { margin:0; font-family:system-ui, sans-serif; background:linear-gradient(135deg,#1f2937,#0f172a); color:#e2e8f0; }
    .page { min-height:100vh; display:flex; align-items:center; justify-content:center; padding:2rem; }
    .card { width:100%; max-width:700px; background:rgba(15,23,42,.92); border:1px solid rgba(148,163,184,.2); border-radius:20px; box-shadow:0 20px 60px rgba(15,23,42,.45); padding:2rem; }
    h1 { margin:0 0 1rem; font-size:2rem; letter-spacing:.04em; color:#7dd3fc; }
    form { display:grid; gap:1rem; }
    input { width:100%; border:1px solid rgba(148,163,184,.3); border-radius:12px; padding:0.9rem 1rem; background:#0f172a; color:#f8fafc; font-size:1rem; }
    button { border:none; border-radius:12px; padding:0.95rem 1.4rem; font-size:1rem; font-weight:600; color:#0f172a; background:#38bdf8; cursor:pointer; transition:transform .15s ease, background .15s ease; }
    button:hover { transform:translateY(-1px); background:#60a5fa; }
    pre { background:rgba(30,41,59,.98); border-radius:14px; padding:1rem; overflow-x:auto; color:#f8fafc; white-space:pre-wrap; word-break:break-word; }
    .note { color:#94a3b8; margin-bottom:1rem; }
  </style>
</head>
<body>
  <div class="page">
    <div class="card">
      <h1>Math CoT Solver</h1>
      <p class="note">Enter a math problem and get concise chain-of-thought steps plus the final answer.</p>
      <form method="post">
        <input name="problem" placeholder="e.g. 12*5 + 8/2" required>
        <button type="submit">Solve</button>
      </form>
      {% if result %}
      <pre>{{ result }}</pre>
      {% endif %}
    </div>
  </div>
</body>
</html>
"""

def solve_math_problem(problem):
    prompt = f"Solve step by step, keep short, limit to 5 steps: {problem}"
    url = f"{BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        reasoning = result['choices'][0]['message']['content']
        code_match = re.search(r'```python\n(.*?)\n```', reasoning, re.DOTALL)
        if code_match:
            code = code_match.group(1)
            try:
                exec_result = eval(code)
                return f"{reasoning}\nFinal answer: {exec_result}"
            except Exception as e:
                return f"{reasoning}\nError: {str(e)}"
        return reasoning
    return f"Error: {response.status_code} - {response.text}"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        problem = request.form['problem']
        result = solve_math_problem(problem)
    return render_template_string(TEMPLATE, result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
