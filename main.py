from flask import Flask, request, jsonify render_template
import json, os
import requests
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)

# Load Firebase credentials from secret file
cred = credentials.Certificate('/etc/secrets/firebase-key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://chatjrlearning-default-rtdb.firebaseio.com/'
})

# Your Groq API key and endpoint
GROQ_API_KEY = 'your_groq_api_key_here'
GROQ_ENDPOINT = 'https://api.groq.com/openai/v1/chat/completions'

# Memory handling (basic)
memory_file = "memory.json"
if os.path.exists(memory_file):
    with open(memory_file, "r") as f:
        memory = json.load(f)
else:
    memory = {}

# Your chat response function
def chatjr_response(user_input):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "messages": [{"role": "user", "content": user_input}],
        "model": "mixtral-8x7b-32768",
        "temperature": 0.7
    }
    response = requests.post(GROQ_ENDPOINT, headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]
# Landing Page
@app.route('/')
def home():
    return render_template('index.html')
# Routes
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    reply = chatjr_response(user_input)
    return jsonify({"reply": reply})

# Run app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
