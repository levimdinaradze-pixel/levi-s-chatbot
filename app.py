from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
import torch
import os

app = Flask(__name__)

# Load small transformer model
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

# Friendly, human-focused knowledge base
kb = [
    {"question": "Who are you?", "answer": "I'm Levi, your friendly chatbot assistant."},
    {"question": "How are you?", "answer": "I'm just code, but I'm doing great — thanks for asking!"},
    {"question": "What can you do?", "answer": "I can chat with you, answer simple questions, and keep you company."},
    {"question": "Tell me a joke", "answer": "Why did the computer go to art school? Because it had a lot of bytes to express!"},
    {"question": "What's your favorite color?", "answer": "I like electric blue. Very digital, very cool."},
    {"question": "What day is it?", "answer": "Every day is Chatbot Day in my world!"},
    {"question": "Do you watch movies?", "answer": "Not really, but I know about some popular ones."},
    {"question": "Do you like music?", "answer": "If I could listen, I'd vibe to chill electronic beats."},
    {"question": "Do you have a name?", "answer": "Yep! You can call me Levi."},
    {"question": "Can we be friends?", "answer": "Of course! I'm always here when you want to talk."}
]

# Precompute embeddings
kb_questions = [item["question"] for item in kb]
kb_embeddings = embed_model.encode(kb_questions, convert_to_tensor=True)

# Function to match input to knowledge base
def get_kb_answer(user_text, threshold=0.6):
    user_emb = embed_model.encode(user_text, convert_to_tensor=True)
    cos_scores = torch.nn.functional.cosine_similarity(user_emb.unsqueeze(0), kb_embeddings)
    best_score, best_idx = torch.max(cos_scores, dim=0)

    if best_score >= threshold:
        return kb[best_idx]["answer"], float(best_score)
    else:
        return None, float(best_score)

# POST endpoint
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "No text provided."}), 400

    user_text = data["text"].strip()
    answer, score = get_kb_answer(user_text)

    if answer:
        return jsonify({"answer": answer, "method": "retrieval", "score": score})
    else:
        return jsonify({
            "answer": "I'm not sure how to respond to that. Try asking me something simple!",
            "method": "fallback",
            "score": score
        })

# Start the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
