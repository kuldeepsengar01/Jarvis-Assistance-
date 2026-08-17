import os

from flask import Flask, request, jsonify
from dotenv import load_dotenv
from google import genai


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("WARNING: GEMINI_API_KEY is not configured.")
    client = None
else:
    print("Gemini API key loaded.")
    client = genai.Client(api_key=API_KEY)


# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__)


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():
    return jsonify({
        "status": "success",
        "message": "Kuldeep Python API is running",
        "service": "Jarvis AI Backend"
    })


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "gemini": client is not None
    })


# =========================================================
# GEMINI
# =========================================================

@app.post("/ask")
def ask_gemini():

    data = request.get_json(silent=True) or {}

    question = data.get("question", "").strip()

    if not question:
        return jsonify({
            "success": False,
            "message": "Question is required"
        }), 400

    if not client:
        return jsonify({
            "success": False,
            "message": "GEMINI_API_KEY is not configured on the server"
        }), 500

    try:

        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=question
        )

        answer = interaction.output_text

        return jsonify({
            "success": True,
            "question": question,
            "answer": answer
        })

    except Exception as error:

        print("Gemini Error:", error)

        return jsonify({
            "success": False,
            "message": "Gemini request failed",
            "error": str(error)
        }), 500


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 5000)
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
