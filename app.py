import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key) if api_key else None


@app.get("/")
def home():
    return jsonify({
        "message": "Kuldeep Python API is running"
    })


@app.post("/ask")
def ask():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "").strip()

    if not question:
        return jsonify({
            "error": "Question is required"
        }), 400

    if not client:
        return jsonify({
            "error": "GEMINI_API_KEY is not configured"
        }), 500

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=question
        )

        return jsonify({
            "question": question,
            "answer": response.text
        })

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port
    )