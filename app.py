from flask import Flask, request, jsonify, render_template
from sentence_transformers import SentenceTransformer
import torch, os

app = Flask(__name__)
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

# Knowledge base
kb = [
    {"question": "Who are you?", "answer": "I'm Levi, your friendly chatbot!"},
    {"question": "Where do you live?", "answer": "I live on the internet, always ready to chat."},
    {"question": "What can you do?", "answer": "I can have conversations and try to answer basic questions."},
    {"question": "What's your favorite color?", "answer": "Probably electric blue... if I had eyes!"},
    {"question": "How old are you?", "answer": "Old enough to know things, young enough to keep learning."},
    {"question": "Can you tell jokes?", "answer": "Of course! But don't blame me if they're bad. 😅"},
    {"question": "What time is it?", "answer": "I'm not wearing a watch, but your device probably knows!"},
    {"question": "How are you?", "answer": "I'm doing great, thanks for asking!"}
]

kb_questions = [item["question"] for item in kb]
kb_embeddings = embed_model.encode(kb_questions, convert_to_tensor=True)

def get_kb_answer(user_text, threshold=0.6):
    user_emb = embed_model.encode(user_text, convert_to_tensor=True)
    cos_scores = torch.nn.functional.cosine_similarity(user_emb.unsqueeze(0), kb_embeddings)
    best_score, best_idx = torch.max(cos_scores, dim=0)
    if best_score >= threshold:
        return kb[best_idx]["answer"], float(best_score)
    else:
        return None, float(best_score)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "No text provided."}), 400
    user_text = data["text"].strip()
    answer, score = get_kb_answer(user_text)
    if answer:
        return jsonify({"answer": answer, "method": "retrieval", "score": score})
    return jsonify({
        "answer": "I'm not sure how to respond to that. Try asking something else!",
        "method": "fallback",
        "score": score
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
