async function sendMessage() {
    const input = document.getElementById("messageInput");
    const message = input.value;
    if (!message.trim()) return;

    appendMessage("You", message);

    const response = await fetch("/ask", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ message })
    });

    const data = await response.json();
    appendMessage("Chat Jr.", data.reply);
    input.value = "";
}

function appendMessage(sender, text) {
    const chatbox = document.getElementById("chatbox");
    const messageDiv = document.createElement("div");
    messageDiv.innerHTML = `<strong>${sender}:</strong> ${text}`;
    chatbox.appendChild(messageDiv);
    chatbox.scrollTop = chatbox.scrollHeight;
}
