from flask import Flask, request, jsonify, render_template
import json, os
import requests

app = Flask(__name__)

# Load memory if exists
memory_file = "memory.json"
if os.path.exists(memory_file):
    with open(memory_file, "r") as f:
        memory = json.load(f)
else:
    memory = {}

# YOUR GROQ API KEY HERE
GROQ_API_KEY = "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"
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

def chatjr_response(user_input):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-8b-8192",  # Groq's fast llama model
        "messages": [
            {"role": "system", "content": "You are Chat Jr., a chaotic but adorable AI gremlin who loves being funny, encouraging, and a little unhinged."},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.7  # How creative he is (higher = crazier)
    }
    response = requests.post(GROQ_ENDPOINT, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        return "Oops, my gremlin brain glitched out. Try again!"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.json.get("message")
    reply = chatjr_response(user_message)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
