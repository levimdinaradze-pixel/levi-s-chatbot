from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
import torch
import os

app = Flask(__name__)

# Load model
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

# Knowledge Base
kb = [
    {"question": "What is artificial intelligence?", "answer": "Artificial intelligence is when machines or computers do tasks that normally require human intelligence."},
    {"question": "How can I learn programming?", "answer": "Start with simple languages like Python, do small projects, learn by doing, and read tutorials."},
    {"question": "What is Georgia country?", "answer": "Georgia is a country located at the intersection of Europe and Asia, in the Caucasus region."},
    {"question": "What languages can you speak?", "answer": "I can understand many languages but currently I respond best in English."}
]

# Precompute embeddings
kb_questions = [item["question"] for item in kb]
kb_embeddings = embed_model.encode(kb_questions, convert_to_tensor=True)

# Match input to KB
def get_kb_answer(user_text, threshold=0.6):
    user_emb = embed_model.encode(user_text, convert_to_tensor=True)
    cos_scores = torch.nn.functional.cosine_similarity(user_emb.unsqueeze(0), kb_embeddings)
    best_score, best_idx = torch.max(cos_scores, dim=0)

    if best_score >= threshold:
        return kb[best_idx]["answer"], float(best_score)
    else:
        return None, float(best_score)

# Flask route
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
            "answer": "I’m not sure about that. Can you ask something else or more clearly?",
            "method": "fallback",
            "score": score
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
