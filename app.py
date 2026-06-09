import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# Use os.environ.get. Vercel injects the API key directly into the environment
# when you add it to the Project Settings > Environment Variables.
api_key = os.environ.get("GROQ_API_KEY")

# Initialize client only if key exists, otherwise handle it gracefully
client = Groq(api_key=api_key) if api_key else None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    if not client:
        return jsonify({"error": "AI Service not configured"}), 500
        
    data = request.get_json()
    user_input = data.get("prompt")
    
    if not user_input:
        return jsonify({"error": "Prompt parameter cannot be blank."}), 400

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": user_input}]
        )
        
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)