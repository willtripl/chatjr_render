from flask import Flask, request, jsonify, render_template
import json, os
import requests
import firebase_admin
from firebase_admin import credentials

app = Flask(__name__)

# Load Firebase credentials from secret file
cred = credentials.Certificate('/etc/secrets/firebase-key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://chatjrlearning.firebaseio.com/'
})

# Groq API key and endpoint
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

# ChatJR response function
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

# Chat Route
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    reply = chatjr_response(user_input)
    return jsonify({"reply": reply})

# Run App
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
