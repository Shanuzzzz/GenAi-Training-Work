from flask import Flask, request, render_template_string
import ast
from groq import Groq

app = Flask(__name__)
client = Groq(api_key="")

def analyze_code(code):
    try:
        ast.parse(code)
        return None
    except SyntaxError as e:
        return f"Syntax error: {e}"

def review_code(code):
    prompt = f"Review this Python code for bugs and improvements: {code}"
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    return response.choices[0].message.content.strip()

def self_reflect(initial_review, code):
    prompt = f"Critique this review and provide an improved version: {initial_review}\nCode: {code}"
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    return response.choices[0].message.content.strip()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        code = request.form['code']
        syntax_error = analyze_code(code)
        if syntax_error:
            result = syntax_error
        else:
            initial = review_code(code)
            refined = self_reflect(initial, code)
            result = f"Initial: {initial}\n\nRefined: {refined}"
        return render_template_string('''
        <form method="post">
        <textarea name="code" rows="10" cols="50">{{ code }}</textarea><br>
        <input type="submit">
        </form>
        <pre>{{ result }}</pre>
        ''', code=code, result=result)
    return render_template_string('''
    <form method="post">
    <textarea name="code" rows="10" cols="50"></textarea><br>
    <input type="submit">
    </form>
    ''')

if __name__ == '__main__':
    app.run(debug=True)