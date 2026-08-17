import os
from pathlib import Path

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request, render_template_string, Response


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    print("Gemini API key loaded successfully.")
else:
    print("WARNING: GEMINI_API_KEY is not configured.")


# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__)


# =========================================================
# WEB PAGE
# =========================================================

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <meta
        name="theme-color"
        content="#020617"
    >

    <title>Kuldeep AI</title>

    <style>

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        :root {
            --bg: #020617;
            --panel: rgba(8, 15, 31, 0.94);
            --panel2: rgba(14, 25, 47, 0.88);
            --border: rgba(93, 211, 255, 0.14);
            --cyan: #41dcff;
            --cyan2: #9cf4ff;
            --text: #f5fbff;
            --muted: #7890a8;
            --danger: #ff5c6c;
        }

        html,
        body {
            width: 100%;
            min-height: 100%;
        }

        body {
            min-height: 100vh;

            font-family:
                Inter,
                Arial,
                Helvetica,
                sans-serif;

            color: var(--text);

            background:
                radial-gradient(
                    circle at 10% 10%,
                    rgba(23, 196, 255, 0.14),
                    transparent 30%
                ),
                radial-gradient(
                    circle at 90% 20%,
                    rgba(80, 80, 255, 0.12),
                    transparent 28%
                ),
                linear-gradient(
                    135deg,
                    #01030a,
                    #04101d 50%,
                    #02050d
                );
        }

        .app {
            min-height: 100vh;

            padding: 18px;

            display: flex;
            justify-content: center;
            align-items: center;
        }

        .shell {
            width: min(1050px, 100%);
            height: min(900px, 94vh);

            display: flex;
            flex-direction: column;

            overflow: hidden;

            border:
                1px solid var(--border);

            border-radius: 28px;

            background:
                var(--panel);

            box-shadow:
                0 30px 90px rgba(0, 0, 0, 0.55),
                0 0 100px rgba(40, 220, 255, 0.05);

            backdrop-filter: blur(18px);
        }

        /* HEADER */

        .header {
            min-height: 74px;

            display: flex;
            justify-content: space-between;
            align-items: center;

            padding: 14px 20px;

            border-bottom:
                1px solid rgba(255, 255, 255, 0.06);
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .logo {
            width: 44px;
            height: 44px;

            display: grid;
            place-items: center;

            border-radius: 14px;

            font-size: 19px;
            font-weight: 700;

            color: #00151c;

            background:
                radial-gradient(
                    circle at 35% 30%,
                    #f3ffff,
                    #43ddff 24%,
                    #08789e 55%,
                    #071321 78%
                );

            box-shadow:
                0 0 30px rgba(64, 220, 255, 0.35);
        }

        .brand h1 {
            font-size: 21px;
            letter-spacing: 3px;
        }

        .brand p {
            margin-top: 3px;

            color: var(--muted);

            font-size: 9px;
            letter-spacing: 1.6px;
        }

        .online {
            display: flex;
            align-items: center;
            gap: 7px;

            padding: 7px 11px;

            border-radius: 999px;

            color: #6ef1b1;

            background:
                rgba(79, 255, 173, 0.07);

            font-size: 10px;
            letter-spacing: 0.6px;
        }

        .online-dot {
            width: 7px;
            height: 7px;

            border-radius: 50%;

            background: #58efa5;

            box-shadow: 0 0 12px #58efa5;
        }

        /* HERO */

        .hero {
            display: grid;
            place-items: center;

            padding: 18px 10px 12px;
        }

        .orb {
            width: 94px;
            height: 94px;

            position: relative;

            display: grid;
            place-items: center;

            border-radius: 50%;

            background:
                radial-gradient(
                    circle at 35% 30%,
                    #f5ffff,
                    #57e9ff 18%,
                    #08769f 48%,
                    #061322 74%
                );

            box-shadow:
                0 0 40px rgba(56, 217, 255, 0.42),
                0 0 90px rgba(56, 217, 255, 0.10);

            animation: pulse 3s ease-in-out infinite;
        }

        .orb::before {
            content: "";

            position: absolute;

            inset: -11px;

            border-radius: 50%;

            border:
                1px solid
                rgba(95, 225, 255, 0.32);

            border-right-color:
                rgba(95, 225, 255, 0.75);

            animation:
                spin 8s linear infinite;
        }

        .orb::after {
            content: "";

            position: absolute;

            inset: -19px;

            border-radius: 50%;

            border:
                1px solid
                rgba(95, 225, 255, 0.09);

            border-left-color:
                rgba(95, 225, 255, 0.50);

            animation:
                spinReverse
                11s linear infinite;
        }

        .orb-core {
            width: 23px;
            height: 23px;

            border-radius: 50%;

            background: #ffffff;

            box-shadow:
                0 0 28px #ffffff;
        }

        .hero-title {
            margin-top: 11px;

            color: var(--cyan);

            font-size: 11px;

            letter-spacing: 2.5px;
        }

        @keyframes pulse {
            0%,
            100% {
                transform: scale(1);
            }

            50% {
                transform: scale(1.05);
            }
        }

        @keyframes spin {
            to {
                transform: rotate(360deg);
            }
        }

        @keyframes spinReverse {
            to {
                transform: rotate(-360deg);
            }
        }

        /* CHAT */

        .chat {
            flex: 1;

            overflow-y: auto;

            padding:
                8px 20px 18px;

            scroll-behavior: smooth;
        }

        .chat::-webkit-scrollbar {
            width: 5px;
        }

        .chat::-webkit-scrollbar-thumb {
            background: #1a344d;
            border-radius: 999px;
        }

        .message-row {
            display: flex;

            margin:
                9px 0;
        }

        .message-row.user {
            justify-content: flex-end;
        }

        .message-row.ai {
            justify-content: flex-start;
        }

        .message {
            max-width: 82%;

            padding:
                12px 14px;

            border-radius: 17px;

            font-size: 14px;

            line-height: 1.6;

            white-space: pre-wrap;

            word-break: break-word;
        }

        .message.user {
            background:
                linear-gradient(
                    135deg,
                    #0b5d7c,
                    #123a59
                );

            border-bottom-right-radius: 5px;
        }

        .message.ai {
            background:
                var(--panel2);

            border:
                1px solid
                rgba(98, 220, 255, 0.08);

            border-bottom-left-radius: 5px;
        }

        .sender {
            margin-bottom: 5px;

            color:
                #7895ae;

            font-size: 9px;

            letter-spacing: 1px;
        }

        /* QUICK */

        .quick {
            display: flex;

            gap: 8px;

            overflow-x: auto;

            padding:
                0 20px 11px;
        }

        .quick::-webkit-scrollbar {
            display: none;
        }

        .quick button {
            flex:
                0 0 auto;

            padding:
                9px 13px;

            border:
                1px solid
                rgba(85, 215, 255, 0.12);

            border-radius: 999px;

            background:
                rgba(14, 29, 53, 0.78);

            color:
                #cdf1ff;

            cursor: pointer;
        }

        /* COMPOSER */

        .composer {
            padding:
                12px 16px 15px;

            border-top:
                1px solid
                rgba(255, 255, 255, 0.06);

            background:
                rgba(2, 8, 18, 0.86);
        }

        .input-wrap {
            display: flex;

            align-items: center;

            gap: 7px;

            padding: 6px;

            border:
                1px solid
                rgba(82, 213, 255, 0.14);

            border-radius: 18px;

            background:
                rgba(11, 22, 40, 0.96);
        }

        .input-wrap input {
            flex: 1;

            min-width: 0;

            padding:
                12px 10px;

            border: none;
            outline: none;

            background:
                transparent;

            color:
                white;

            font-size:
                15px;
        }

        .input-wrap input::placeholder {
            color:
                #58718a;
        }

        .mic,
        .send {
            flex:
                0 0 auto;

            border: none;

            cursor: pointer;
        }

        .mic {
            width: 44px;
            height: 44px;

            border-radius: 13px;

            color:
                white;

            background:
                rgba(34, 55, 81, 0.90);

            font-size:
                18px;
        }

        .mic.listening {
            background:
                var(--danger);

            box-shadow:
                0 0 24px
                rgba(255, 92, 108, 0.40);
        }

        .mic:disabled,
        .send:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .send {
            min-width: 73px;
            height: 44px;

            padding:
                0 14px;

            border-radius: 13px;

            background:
                linear-gradient(
                    135deg,
                    #9cf5ff,
                    #2bc9ef
                );

            color:
                #00131a;

            font-weight:
                800;

            letter-spacing:
                0.4px;
        }

        .status {
            margin-top:
                7px;

            text-align:
                center;

            color:
                #536e87;

            font-size:
                9px;

            letter-spacing:
                1px;
        }

        /* MOBILE */

        @media (max-width: 700px) {

            .app {
                padding: 0;
            }

            .shell {
                width: 100%;
                height: 100svh;

                border:
                    none;

                border-radius:
                    0;
            }

            .header {
                padding:
                    13px 14px;
            }

            .brand h1 {
                font-size:
                    17px;
            }

            .brand p {
                font-size:
                    8px;
            }

            .logo {
                width:
                    40px;

                height:
                    40px;
            }

            .online {
                font-size:
                    9px;
            }

            .orb {
                width:
                    82px;

                height:
                    82px;
            }

            .orb-core {
                width:
                    20px;

                height:
                    20px;
            }

            .chat {
                padding:
                    8px 14px 15px;
            }

            .message {
                max-width:
                    92%;

                font-size:
                    13px;
            }

            .quick {
                padding:
                    0 14px 10px;
            }

            .composer {
                padding:
                    10px 9px
                    max(
                        10px,
                        env(safe-area-inset-bottom)
                    );
            }

            .input-wrap input {
                font-size:
                    14px;
            }

            .send {
                min-width:
                    60px;
            }
        }

    </style>

</head>

<body>

<div class="app">

    <main class="shell">

        <header class="header">

            <div class="brand">

                <div class="logo">
                    ◉
                </div>

                <div>

                    <h1>
                        KULDEEP AI
                    </h1>

                    <p>
                        GEMINI INTELLIGENCE
                    </p>

                </div>

            </div>

            <div class="online">

                <span class="online-dot"></span>

                ONLINE

            </div>

        </header>


        <section class="hero">

            <div class="orb">

                <div class="orb-core"></div>

            </div>

            <div class="hero-title">
                JARVIS IS READY
            </div>

        </section>


        <section
            class="chat"
            id="chat"
        >

            <div class="message-row ai">

                <div class="message ai">

                    <div class="sender">
                        JARVIS
                    </div>

                    Hello Kuldeep 👋
                    Ask me anything.

                </div>

            </div>

        </section>


        <div class="quick">

            <button
                onclick="quickAsk('What is Python?')"
            >
                🐍 Python
            </button>

            <button
                onclick="quickAsk('Explain Artificial Intelligence')"
            >
                🤖 AI
            </button>

            <button
                onclick="quickAsk('What is React?')"
            >
                ⚛ React
            </button>

            <button
                onclick="quickAsk('Explain JavaScript')"
            >
                JS
            </button>

            <button
                onclick="quickAsk('Give me a programming tip')"
            >
                💡 Tip
            </button>

        </div>


        <footer class="composer">

            <div class="input-wrap">

                <input
                    id="question"
                    type="text"
                    autocomplete="off"
                    placeholder="Ask Jarvis anything..."
                >

                <button
                    id="mic"
                    class="mic"
                    type="button"
                    onclick="startListening()"
                >
                    🎤
                </button>

                <button
                    id="send"
                    class="send"
                    type="button"
                    onclick="askGemini()"
                >
                    ASK
                </button>

            </div>

            <div
                id="status"
                class="status"
            >
                ● SECURE • AI ONLINE • READY
            </div>

        </footer>

    </main>

</div>


<script>

const input =
    document.getElementById("question");

const chat =
    document.getElementById("chat");

const status =
    document.getElementById("status");

const micButton =
    document.getElementById("mic");

const sendButton =
    document.getElementById("send");


function addMessage(
    sender,
    text,
    type
) {

    const row =
        document.createElement("div");

    row.className =
        "message-row " + type;


    const box =
        document.createElement("div");

    box.className =
        "message " + type;


    const senderElement =
        document.createElement("div");

    senderElement.className =
        "sender";

    senderElement.textContent =
        sender;


    const content =
        document.createElement("div");

    content.textContent =
        text;


    box.appendChild(
        senderElement
    );

    box.appendChild(
        content
    );


    row.appendChild(
        box
    );


    chat.appendChild(
        row
    );


    chat.scrollTop =
        chat.scrollHeight;
}


function quickAsk(text) {

    input.value =
        text;

    askGemini();
}


async function askGemini() {

    const question =
        input.value.trim();


    if (!question) {

        input.focus();

        return;
    }


    addMessage(
        "YOU",
        question,
        "user"
    );


    input.value =
        "";


    input.disabled =
        true;

    sendButton.disabled =
        true;

    micButton.disabled =
        true;


    status.textContent =
        "🧠 JARVIS IS THINKING...";


    try {

        const response =
            await fetch(
                "/ask",
                {
                    method:
                        "POST",

                    headers: {
                        "Content-Type":
                            "application/json",

                        "Accept":
                            "application/json"
                    },

                    body:
                        JSON.stringify({
                            question:
                                question
                        })
                }
            );


        const raw =
            await response.text();


        let data;


        try {

            data =
                JSON.parse(raw);

        } catch (parseError) {

            console.error(
                "Non-JSON server response:",
                raw
            );

            throw new Error(
                "Server returned an invalid response. HTTP " +
                response.status
            );
        }


        if (!response.ok) {

            throw new Error(
                data.error ||
                data.message ||
                ("HTTP " + response.status)
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
            data.answer ||
                "I received an empty answer.",
            "ai"
        );


        speakLong(
            data.answer || ""
        );


        status.textContent =
            "● ONLINE";


    } catch (error) {

        console.error(
            "ASK ERROR:",
            error
        );


        addMessage(
            "JARVIS ERROR",
            error.message ||
                "Request failed.",
            "ai"
        );


        status.textContent =
            "⚠ REQUEST FAILED";


    } finally {

        input.disabled =
            false;

        sendButton.disabled =
            false;

        micButton.disabled =
            false;

        input.focus();
    }
}


/*
    Long response speech.

    We split long text into chunks because
    some browsers handle very long utterances
    poorly.
*/

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


    const cleanText =
        text
            .replace(
                /```[\s\S]*?```/g,
                " code block "
            )
            .replace(
                /[*#_`]/g,
                ""
            )
            .trim();


    const sentences =
        cleanText.match(
            /[^.!?]+[.!?]+|[^.!?]+$/g
        );


    if (!sentences) {
        return;
    }


    const chunks = [];

    let current = "";


    for (
        const sentence
        of sentences
    ) {

        const next =
            (
                current +
                " " +
                sentence
            ).trim();


        if (
            next.length > 220
        ) {

            if (current) {
                chunks.push(
                    current
                );
            }

            current =
                sentence.trim();

        } else {

            current =
                next;
        }
    }


    if (current) {
        chunks.push(
            current
        );
    }


    let index = 0;


    function speakNext() {

        if (
            index >=
            chunks.length
        ) {
            return;
        }


        const utterance =
            new SpeechSynthesisUtterance(
                chunks[index]
            );


        utterance.lang =
            "en-IN";

        utterance.rate =
            0.98;

        utterance.pitch =
            1;

        utterance.volume =
            1;


        utterance.onend =
            function () {

                index++;

                setTimeout(
                    speakNext,
                    80
                );
            };


        utterance.onerror =
            function (event) {

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


input.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "Enter"
        ) {

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


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():
    return render_template_string(HTML)


# =========================================================
# SPEECH.JS FILE
# =========================================================

@app.get("/speech.js")
def speech_js():

    js_path = (
        Path(__file__).resolve().parent
        / "speech.js"
    )


    if not js_path.exists():

        return Response(
            "console.error('speech.js not found');",
            status=404,
            mimetype="application/javascript"
        )


    return Response(
        js_path.read_text(
            encoding="utf-8"
        ),
        mimetype="application/javascript"
    )


# =========================================================
# HEALTH
# =========================================================

@app.get("/health")
def health():

    return jsonify({
        "status": "ok",
        "gemini_configured":
            bool(GEMINI_API_KEY)
    })


# =========================================================
# ASK GET
# =========================================================

@app.get("/ask")
def ask_get():

    return jsonify({
        "success": True,
        "message":
            "Use POST /ask or the web interface."
    })


# =========================================================
# ASK POST
# =========================================================

@app.post("/ask")
def ask():

    data =
        request.get_json(
            silent=True
        ) or {}


    question =
        str(
            data.get(
                "question",
                ""
            )
        ).strip()


    if not question:

        return jsonify({
            "success": False,
            "message":
                "Question is required."
        }), 400


    if not GEMINI_API_KEY:

        return jsonify({
            "success": False,
            "message":
                "GEMINI_API_KEY is not configured."
        }), 500


    try:

        url = (
            "https://generativelanguage.googleapis.com"
            "/v1/interactions"
        )


        headers = {

            "x-goog-api-key":
                GEMINI_API_KEY,

            "Content-Type":
                "application/json"
        }


        payload = {

            "model":
                "gemini-3.6-flash",

            "input":
                question
        }


        print(
            "Sending request to Gemini..."
        )


        response =
            requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=90
            )


        print(
            "Gemini status:",
            response.status_code
        )


        if not response.ok:

            print(
                "Gemini response:",
                response.text
            )


            return jsonify({

                "success":
                    False,

                "message":
                    "Gemini API request failed.",

                "error":
                    response.text,

                "status_code":
                    response.status_code

            }), 502


        result =
            response.json()


        answer =
            result.get(
                "output_text",
                ""
            )


        if not answer:

            for step in result.get(
                "steps",
                []
            ):

                if (
                    step.get("type")
                    != "model_output"
                ):
                    continue


                for content in step.get(
                    "content",
                    []
                ):

                    if (
                        content.get("type")
                        == "text"
                    ):

                        answer += (
                            content.get(
                                "text",
                                ""
                            )
                        )


        if not answer:

            answer =
                "Gemini returned an empty response."


        return jsonify({

            "success":
                True,

            "question":
                question,

            "answer":
                answer
        })


    except requests.RequestException as error:

        print(
            "Gemini network error:",
            error
        )


        return jsonify({

            "success":
                False,

            "message":
                "Could not connect to Gemini API.",

            "error":
                str(error)
        }), 502


    except Exception as error:

        print(
            "Gemini server error:",
            error
        )


        return jsonify({

            "success":
                False,

            "message":
                "Server error.",

            "error":
                str(error)
        }), 500


# =========================================================
# LOCAL SERVER
# =========================================================

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
