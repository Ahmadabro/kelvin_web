import os
from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Point to parent directories for templates and design assets
app = Flask(__name__, template_folder='../templates', static_folder='../static')

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    user_input = data.get("prompt")
    
    if not user_input:
        return jsonify({"error": "Prompt cannot be blank."}), 400
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": user_input}]
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
            
    except Exception as e:
        return jsonify({"error": f"Groq API Error: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)