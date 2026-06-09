import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# Initialize the Groq client
# We use os.environ.get to pull from Vercel's Environment Variables
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
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
        return jsonify({"error": f"Groq API Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)