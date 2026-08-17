import os

from flask import Flask, request, jsonify
from dotenv import load_dotenv
from google import genai


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    print("Gemini API key loaded successfully.")
    client = genai.Client(api_key=GEMINI_API_KEY)
else:
    print("WARNING: GEMINI_API_KEY is not configured.")
    client = None


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
        "gemini_configured": client is not None
    })


# =========================================================
# ASK - GET
# =========================================================

@app.get("/ask")
def ask_get():
    return jsonify({
        "success": True,
        "message": "Use POST /ask with JSON body: {\"question\": \"Your question\"}"
    })


# =========================================================
# ASK - POST
# =========================================================

@app.post("/ask")
def ask_post():

    data = request.get_json(silent=True) or {}

    question = data.get("question")

    if question is None:
        return jsonify({
            "success": False,
            "message": "question is required"
        }), 400

    question = str(question).strip()

    if not question:
        return jsonify({
            "success": False,
            "message": "question cannot be empty"
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
# SERVER
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
