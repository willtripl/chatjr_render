from flask import Flask, request, jsonify, render_template
import json, os

app = Flask(__name__)

memory_file = "memory.json"
if os.path.exists(memory_file):
    with open(memory_file, "r") as f:
        memory = json.load(f)
else:
    memory = {}

def chatjr_response(user_input):
    if user_input in memory:
        return memory[user_input]
    else:
        reply = f"Chat Jr. says: You said '{user_input}'"
        memory[user_input] = reply
        with open(memory_file, "w") as f:
            json.dump(memory, f)
        return reply

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
