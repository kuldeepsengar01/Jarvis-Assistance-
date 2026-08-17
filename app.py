import os
from pathlib import Path

import requests
from flask import Flask, jsonify, request, render_template_string, Response
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

app = Flask(__name__)


HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kuldeep AI</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            font-family: Arial, sans-serif;
            color: white;
            background: #020617;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .app {
            width: min(900px, 100%);
            height: 100vh;
            max-height: 900px;
            display: flex;
            flex-direction: column;
            background: #07111f;
        }

        .header {
            padding: 18px;
            text-align: center;
            border-bottom: 1px solid #17324b;
        }

        .header h1 {
            margin: 0;
            color: #55ddff;
            letter-spacing: 3px;
        }

        .header p {
            margin: 5px 0 0;
            color: #7890a8;
            font-size: 12px;
        }

        .chat {
            flex: 1;
            overflow-y: auto;
            padding: 18px;
        }

        .row {
            display: flex;
            margin: 10px 0;
        }

        .row.user {
            justify-content: flex-end;
        }

        .row.ai {
            justify-content: flex-start;
        }

        .message {
            max-width: 85%;
            padding: 12px 15px;
            border-radius: 16px;
            line-height: 1.6;
            white-space: pre-wrap;
            word-break: break-word;
        }

        .message.user {
            background: #0e5c7d;
        }

        .message.ai {
            background: #122238;
            border: 1px solid #1c3b57;
        }

        .sender {
            font-size: 10px;
            color: #86a0b7;
            margin-bottom: 5px;
            letter-spacing: 1px;
        }

        .quick {
            display: flex;
            gap: 8px;
            overflow-x: auto;
            padding: 0 15px 10px;
        }

        .quick button {
            flex: 0 0 auto;
            border: 1px solid #21445f;
            background: #0b1b2d;
            color: #d5f4ff;
            padding: 9px 13px;
            border-radius: 999px;
            cursor: pointer;
        }

        .composer {
            padding: 12px;
            border-top: 1px solid #17324b;
        }

        .input-box {
            display: flex;
            gap: 8px;
        }

        input {
            flex: 1;
            min-width: 0;
            border: 1px solid #21445f;
            outline: none;
            background: #0a1828;
            color: white;
            padding: 13px;
            border-radius: 12px;
            font-size: 15px;
        }

        button {
            font-family: inherit;
        }

        #mic,
        #send {
            border: none;
            border-radius: 12px;
            cursor: pointer;
        }

        #mic {
            width: 48px;
            background: #19344c;
            color: white;
            font-size: 18px;
        }

        #mic.listening {
            background: #ef4444;
        }

        #send {
            min-width: 70px;
            background: #43d9ff;
            color: #00121a;
            font-weight: bold;
        }

        .status {
            text-align: center;
            margin-top: 7px;
            color: #69839b;
            font-size: 11px;
        }

        @media (max-width: 600px) {
            .app {
                width: 100%;
                height: 100svh;
            }

            .message {
                max-width: 92%;
                font-size: 13px;
            }

            input {
                font-size: 14px;
            }
        }
    </style>
</head>

<body>

<div class="app">

    <header class="header">
        <h1>KULDEEP AI</h1>
        <p>JARVIS • GEMINI ASSISTANT</p>
    </header>

    <main class="chat" id="chat">

        <div class="row ai">
            <div class="message ai">
                <div class="sender">JARVIS</div>
                Hello Kuldeep 👋 Ask me anything.
            </div>
        </div>

    </main>

    <div class="quick">

        <button onclick="quickAsk('What is Python?')">
            Python
        </button>

        <button onclick="quickAsk('Explain AI simply')">
            AI
        </button>

        <button onclick="quickAsk('What is React?')">
            React
        </button>

        <button onclick="quickAsk('Give me a coding tip')">
            Coding Tip
        </button>

    </div>

    <footer class="composer">

        <div class="input-box">

            <input
                id="question"
                type="text"
                placeholder="Ask Jarvis..."
                autocomplete="off"
            >

            <button
                id="mic"
                onclick="startListening()"
            >
                🎤
            </button>

            <button
                id="send"
                onclick="askGemini()"
            >
                ASK
            </button>

        </div>

        <div id="status" class="status">
            ● ONLINE
        </div>

    </footer>

</div>


<script>
const input = document.getElementById("question");
const chat = document.getElementById("chat");
const status = document.getElementById("status");
const mic = document.getElementById("mic");
const send = document.getElementById("send");


function addMessage(sender, text, type) {

    const row = document.createElement("div");
    row.className = "row " + type;

    const message = document.createElement("div");
    message.className = "message " + type;

    const senderEl = document.createElement("div");
    senderEl.className = "sender";
    senderEl.textContent = sender;

    const content = document.createElement("div");
    content.textContent = text;

    message.appendChild(senderEl);
    message.appendChild(content);

    row.appendChild(message);
    chat.appendChild(row);

    chat.scrollTop = chat.scrollHeight;
}


function quickAsk(text) {
    input.value = text;
    askGemini();
}


async function askGemini() {

    const question = input.value.trim();

    if (!question) {
        return;
    }

    addMessage("YOU", question, "user");

    input.value = "";

    input.disabled = true;
    send.disabled = true;
    mic.disabled = true;

    status.textContent = "● THINKING...";

    try {

        const response = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify({
                question: question
            })
        });

        const text = await response.text();

        let data;

        try {
            data = JSON.parse(text);
        } catch (error) {
            throw new Error(
                "Invalid server response: HTTP " +
                response.status
            );
        }

        if (!data.success) {
            throw new Error(
                data.error ||
                data.message ||
                "Gemini request failed."
            );
        }

        addMessage(
            "JARVIS",
            data.answer,
            "ai"
        );

        if (typeof window.speakLong === "function") {
            window.speakLong(data.answer);
        }

        status.textContent = "● ONLINE";

    } catch (error) {

        console.error(error);

        addMessage(
            "JARVIS",
            error.message,
            "ai"
        );

        status.textContent = "⚠ ERROR";

    } finally {

        input.disabled = false;
        send.disabled = false;
        mic.disabled = false;

        input.focus();
    }
}


input.addEventListener("keydown", function(event) {

    if (event.key === "Enter") {
        event.preventDefault();
        askGemini();
    }

});


window.askGemini = askGemini;
</script>

<script src="/speech.js"></script>

</body>
</html>
"""


@app.get("/")
def home():
    return render_template_string(HTML)


@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "gemini_configured": bool(GEMINI_API_KEY)
    })


@app.get("/speech.js")
def speech_js():

    path = Path(__file__).resolve().parent / "speech.js"

    if not path.exists():
        return Response(
            "console.error('speech.js not found');",
            status=404,
            mimetype="application/javascript"
        )

    return Response(
        path.read_text(encoding="utf-8"),
        mimetype="application/javascript"
    )


@app.post("/ask")
def ask():

    data = request.get_json(silent=True) or {}

    question = str(data.get("question", "")).strip()

    if not question:
        return jsonify({
            "success": False,
            "message": "Question is required."
        })

    if not GEMINI_API_KEY:
        return jsonify({
            "success": False,
            "message": "GEMINI_API_KEY is not configured."
        })

    try:

        url = (
            "https://generativelanguage.googleapis.com/"
            "v1beta/models/"
            "gemini-3.6-flash:generateContent"
        )

        headers = {
            "x-goog-api-key": GEMINI_API_KEY,
            "Content-Type": "application/json"
        }

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": question
                        }
                    ]
                }
            ]
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=60
        )

        print(
            "Gemini status:",
            response.status_code
        )

        print(
            "Gemini response:",
            response.text[:1000]
        )

        if not response.ok:

            return jsonify({
                "success": False,
                "message": "Gemini API request failed.",
                "error": response.text,
                "status_code": response.status_code
            })

        result = response.json()

        candidates = result.get(
            "candidates",
            []
        )

        answer = ""

        if candidates:

            content = candidates[0].get(
                "content",
                {}
            )

            parts = content.get(
                "parts",
                []
            )

            for part in parts:

                part_text = part.get(
                    "text",
                    ""
                )

                if part_text:
                    answer += part_text

        if not answer:
            answer = "Gemini returned no text."

        return jsonify({
            "success": True,
            "question": question,
            "answer": answer
        })

    except requests.RequestException as error:

        return jsonify({
            "success": False,
            "message": "Gemini network error.",
            "error": str(error)
        })

    except Exception as error:

        return jsonify({
            "success": False,
            "message": "Server error.",
            "error": str(error)
        })


if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            "5000"
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
