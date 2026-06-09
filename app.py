import os
from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Initialize the Groq engine using native package structures
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
        return jsonify({"error": "Prompt parameter cannot be empty."}), 400
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": user_input}]
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
            
    except Exception as e:
        return jsonify({"error": f"Groq API Link Failure: {str(e)}"}), 500

# Left in place for local testing execution blocks
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)