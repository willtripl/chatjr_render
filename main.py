from flask import Flask, request, jsonify, render_template import json, os import requests import firebase_admin from firebase_admin import credentials

app = Flask(name)

Load Firebase credentials

cred = credentials.Certificate('/etc/secrets/firebase-key.json') firebase_admin.initialize_app(cred, { 'databaseURL': 'https://chatjrlearning-default-rtdb.firebaseio.com/' })

Your Groq API key and endpoint

GROQ_API_KEY = 'your_groq_api_key_here' GROQ_ENDPOINT = 'https://api.groq.com/openai/v1/chat/completions'

Chat response function

def chatjr_response(user_input): headers = { "Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json" } payload = { "messages": [{"role": "user", "content": user_input}], "model": "mixtral-8x7b-32768", "temperature": 0.7 } response = requests.post(GROQ_ENDPOINT, headers=headers, json=payload) data = response.json() if "choices" in data: return data["choices"][0]["message"]["content"] else: return "Sorry, something went wrong."

Landing page

@app.route('/') def home(): return render_template('index.html')

Chat endpoint

@app.route('/chat', methods=['POST']) def chat(): user_input = request.json.get("message") reply = chatjr_response(user_input) return jsonify({"reply": reply})

Run app

if name == "main": app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))

