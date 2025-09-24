<!DOCTYPE html>
<html>
<head>
  <title>Levi Chatbot</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
    #chatbox { width: 100%; max-width: 500px; margin: auto; padding: 20px; background: white; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
    .message { margin: 10px 0; }
    .user { font-weight: bold; color: #2b7cff; }
    .bot { font-weight: bold; color: #00a86b; }
    input, button { padding: 10px; margin-top: 10px; width: 100%; box-sizing: border-box; }
  </style>
</head>
<body>
  <div id="chatbox">
    <h2>Chat with Levi 🤖</h2>
    <div id="messages"></div>
    <input type="text" id="userInput" placeholder="Type your message..." />
    <button onclick="sendMessage()">Send</button>
  </div>

  <script>
    async function sendMessage() {
      const input = document.getElementById("userInput");
      const text = input.value.trim();
      if (!text) return;

      const messagesDiv = document.getElementById("messages");
      messagesDiv.innerHTML += `<div class='message user'>You: ${text}</div>`;

      const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: text })
      });

      const data = await response.json();
      messagesDiv.innerHTML += `<div class='message bot'>Levi: ${data.answer}</div>`;
      input.value = "";
    }
  </script>
</body>
</html>
