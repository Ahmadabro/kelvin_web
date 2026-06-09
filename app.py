import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

# Load local environment configuration if available
load_dotenv()

app = Flask(__name__)

# Initialize the Groq client using the official OpenAI-compatible structure
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://groq.com"
)

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
        # Utilizing a high-performance, long-context model
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": user_input}]
        )
        
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
            
    except Exception as e:
        return jsonify({"error": f"API Connection Error: {str(e)}"}), 500

if __name__ == '__main__':
    # Dynamically bind to the cloud host target deployment port
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)