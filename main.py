from flask import Flask, request, jsonify, render_template
import os, json, requests

app = Flask(__name__)

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

# Landing page
@app.route('/')
def home():
    return render_template('index.html')

# Chat route
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    reply = chatjr_response(user_input)
    return jsonify({"reply": reply})

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
