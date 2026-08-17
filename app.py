import os
from pathlib import Path

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request, render_template_string, Response


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

app = Flask(__name__)


HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#020617">
    <title>Kuldeep AI</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            font-family: Arial, sans-serif;
            color: #ffffff;
            background:
                radial-gradient(
                    circle at 20% 10%,
                    rgba(0, 210, 255, 0.14),
                    transparent 30%
                ),
                radial-gradient(
                    circle at 80% 20%,
                    rgba(90, 80, 255, 0.12),
                    transparent 30%
                ),
                #020617;
        }

        .app {
            width: 100%;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 15px;
        }

        .shell {
            width: min(1000px, 100%);
            height: min(900px, 95vh);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            background: rgba(8, 16, 31, 0.95);
            border: 1px solid rgba(80, 210, 255, 0.15);
            border-radius: 25px;
            box-shadow: 0 30px 90px rgba(0, 0, 0, 0.5);
        }

        .header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 16px 20px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        }

        .title {
            margin: 0;
            font-size: 21px;
            color: #55ddff;
            letter-spacing: 3px;
        }

        .subtitle {
            margin: 4px 0 0;
            color: #7189a0;
            font-size: 9px;
            letter-spacing: 1.5px;
        }

        .online {
            color: #60f0aa;
            font-size: 10px;
        }

        .hero {
            text-align: center;
            padding: 18px 10px;
        }

        .orb {
            width: 82px;
            height: 82px;
            margin: auto;
            border-radius: 50%;
            background:
                radial-gradient(
                    circle at 35% 30%,
                    #f4ffff,
                    #50e3ff 25%,
                    #096f98 55%,
                    #061321 75%
                );
            box-shadow:
                0 0 35px rgba(50, 220, 255, 0.4),
                0 0 90px rgba(50, 220, 255, 0.1);
        }

        .ready {
            margin-top: 10px;
            color: #63deff;
            font-size: 11px;
            letter-spacing: 2px;
        }

        .chat {
            flex: 1;
            overflow-y: auto;
            padding: 10px 18px;
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
            padding: 12px 14px;
            border-radius: 16px;
            line-height: 1.6;
            white-space: pre-wrap;
            word-break: break-word;
            font-size: 14px;
        }

        .message.user {
            background: #0b5878;
        }

        .message.ai {
            background: #122239;
            border: 1px solid #1a3954;
        }

        .sender {
            margin-bottom: 5px;
            font-size: 9px;
            color: #7c97ae;
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
            border: 1px solid #21435d;
            border-radius: 999px;
            background: #0b192b;
            color: #cfefff;
            padding: 9px 13px;
            cursor: pointer;
        }

        .composer {
            padding: 10px;
            border-top: 1px solid rgba(255, 255, 255, 0.06);
        }

        .input-wrap {
            display: flex;
            gap: 7px;
        }

        #question {
            flex: 1;
            min-width: 0;
            border: 1px solid #22465f;
            border-radius: 12px;
            background: #091727;
            color: white;
            padding: 13px;
            outline: none;
            font-size: 15px;
        }

        #mic,
        #send {
            border: none;
            border-radius: 12px;
            cursor: pointer;
        }

        #mic {
            width: 48px;
            background: #17344d;
            color: white;
            font-size: 18px;
        }

        #mic.listening {
            background: #ef4444;
        }

        #send {
            min-width: 70px;
            background: #42d9ff;
            color: #00131a;
            font-weight: bold;
        }

        .status {
            text-align: center;
            margin-top: 7px;
            color: #607990;
            font-size: 10px;
        }

        @media (max-width: 650px) {
            .app {
                padding: 0;
            }

            .shell {
                width: 100%;
                height: 100svh;
                border: none;
                border-radius: 0;
            }

            .message {
                max-width: 92%;
                font-size: 13px;
            }

            #question {
                font-size: 14px;
            }
        }
    </style>
</head>

<body>

<div class="app">
    <main class="shell">

        <header class="header">
            <div>
                <h1 class="title">KULDEEP AI</h1>
                <p class="subtitle">JARVIS • GEMINI ASSISTANT</p>
            </div>

            <div class="online">● ONLINE</div>
        </header>

        <section class="hero">
            <div class="orb"></div>
            <div class="ready">JARVIS IS READY</div>
        </section>

        <section class="chat" id="chat">
            <div class="row ai">
                <div class="message ai">
                    <div class="sender">JARVIS</div>
                    Hello Kuldeep 👋 Ask me anything.
                </div>
            </div>
        </section>

        <div class="quick">
            <button type="button" onclick="quickAsk('What is Python?')">Python</button>
            <button type="button" onclick="quickAsk('Explain AI simply')">AI</button>
            <button type="button" onclick="quickAsk('What is React?')">React</button>
            <button type="button" onclick="quickAsk('Give me a coding tip')">Coding Tip</button>
        </div>

        <footer class="composer">
            <div class="input-wrap">
                <input
                    id="question"
                    type="text"
                    placeholder="Ask Jarvis..."
                    autocomplete="off"
                >

                <button
                    id="mic"
                    type="button"
                    onclick="startListening()"
                >
                    🎤
                </button>

                <button
                    id="send"
                    type="button"
                    onclick="askGemini()"
                >
                    ASK
                </button>
            </div>

            <div id="status" class="status">
                ● ONLINE
            </div>
        </footer>

    </main>
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

    const box = document.createElement("div");
    box.className = "message " + type;

    const senderElement = document.createElement("div");
    senderElement.className = "sender";
    senderElement.textContent = sender;

    const content = document.createElement("div");
    content.textContent = text;

    box.appendChild(senderElement);
    box.appendChild(content);

    row.appendChild(box);
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
        input.focus();
        return;
    }

    addMessage(
        "YOU",
        question,
        "user"
    );

    input.value = "";

    input.disabled = true;
    send.disabled = true;
    mic.disabled = true;

    status.textContent =
        "🧠 JARVIS IS THINKING...";


    try {

        const response = await fetch(
            "/ask",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },

                body: JSON.stringify({
                    question: question
                })
            }
        );


        const raw = await response.text();

        let data;

        try {

            data = JSON.parse(raw);

        } catch (error) {

            throw new Error(
                "Server returned invalid JSON. HTTP " +
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
            data.answer || "No answer received.",
            "ai"
        );


        if (
            typeof window.speakLong ===
            "function"
        ) {

            window.speakLong(
                data.answer || ""
            );
        }


        status.textContent =
            "● ONLINE";


    } catch (error) {

        console.error(
            "Jarvis request error:",
            error
        );

        addMessage(
            "JARVIS",
            error.message || "Request failed.",
            "ai"
        );

        status.textContent =
            "⚠ ERROR";


    } finally {

        input.disabled = false;
        send.disabled = false;
        mic.disabled = false;

        input.focus();
    }
}


function speakLong(text) {

    if (
        !("speechSynthesis" in window)
    ) {
        return;
    }

    if (!text) {
        return;
    }

    window.speechSynthesis.cancel();


    const parts = text.match(
        /[^.!?]+[.!?]+|[^.!?]+$/g
    );


    if (!parts) {
        return;
    }


    let index = 0;


    function speakNext() {

        if (index >= parts.length) {
            return;
        }


        const utterance =
            new SpeechSynthesisUtterance(
                parts[index].trim()
            );


        utterance.lang = "en-IN";
        utterance.rate = 0.98;
        utterance.pitch = 1;
        utterance.volume = 1;


        utterance.onend =
            function() {

                index += 1;

                setTimeout(
                    speakNext,
                    80
                );
            };


        utterance.onerror =
            function(event) {

                console.error(
                    "Speech synthesis error:",
                    event.error
                );
            };


        window.speechSynthesis.speak(
            utterance
        );
    }


    speakNext();
}


window.askGemini = askGemini;
window.speakLong = speakLong;


input.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {

            event.preventDefault();

            askGemini();
        }
    }
);

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

    path = Path(
        __file__
    ).resolve().parent / "speech.js"


    if not path.exists():

        return Response(
            "console.error('speech.js not found');",
            status=404,
            mimetype="application/javascript"
        )


    return Response(
        path.read_text(
            encoding="utf-8"
        ),
        mimetype="application/javascript"
    )


@app.post("/ask")
def ask():

    data = request.get_json(
        silent=True
    ) or {}


    question = str(
        data.get(
            "question",
            ""
        )
    ).strip()


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


    models = [
        "gemini-3.6-flash",
        "gemini-3.5-flash-lite"
    ]


    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY
    }


    last_error = "Gemini request failed."


    for model in models:

        payload = {
            "model": model,
            "input": question
        }


        for attempt in range(3):

            try:

                response = requests.post(
                    "https://generativelanguage.googleapis.com/v1/interactions",
                    headers=headers,
                    json=payload,
                    timeout=90
                )


                print(
                    "Gemini model:",
                    model,
                    "attempt:",
                    attempt + 1,
                    "status:",
                    response.status_code
                )


                if response.ok:

                    result = response.json()


                    answer_parts = []


                    for step in result.get(
                        "steps",
                        []
                    ):

                        if step.get(
                            "type"
                        ) != "model_output":

                            continue


                        for content in step.get(
                            "content",
                            []
                        ):

                            if content.get(
                                "type"
                            ) != "text":

                                continue


                            text = content.get(
                                "text",
                                ""
                            )


                            if text:

                                answer_parts.append(
                                    text
                                )


                    answer = "\n".join(
                        answer_parts
                    ).strip()


                    if answer:

                        return jsonify({
                            "success": True,
                            "question": question,
                            "answer": answer,
                            "model": model
                        })


                    last_error = (
                        "Gemini returned an empty response."
                    )

                    break


                last_error = response.text


                if response.status_code in (
                    429,
                    500,
                    502,
                    503,
                    504
                ):

                    continue


                break


            except requests.RequestException as error:

                last_error = str(error)
                continue


            except Exception as error:

                last_error = str(error)
                break


    return jsonify({
        "success": False,
        "message": "Gemini request failed after retries.",
        "error": last_error
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
