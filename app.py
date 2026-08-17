import os

from flask import Flask, request, jsonify, render_template_string
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
# HTML UI
# =========================================================

HTML = r"""
<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <meta name="theme-color" content="#030712">

    <title>Kuldeep AI</title>

    <style>

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            min-height: 100vh;
            font-family: Arial, sans-serif;
            color: white;

            background:
                radial-gradient(
                    circle at 20% 10%,
                    rgba(56, 217, 255, 0.15),
                    transparent 30%
                ),
                radial-gradient(
                    circle at 80% 20%,
                    rgba(88, 90, 255, 0.12),
                    transparent 30%
                ),
                linear-gradient(
                    135deg,
                    #02040b,
                    #07101e,
                    #020611
                );
        }

        .app {
            width: 100%;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .shell {
            width: min(1000px, 100%);
            height: min(900px, 94vh);

            display: flex;
            flex-direction: column;

            overflow: hidden;

            border: 1px solid rgba(110, 220, 255, 0.15);
            border-radius: 28px;

            background: rgba(8, 15, 31, 0.88);

            box-shadow:
                0 30px 100px rgba(0, 0, 0, 0.55),
                0 0 80px rgba(40, 210, 255, 0.06);

            backdrop-filter: blur(20px);
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;

            padding: 18px 22px;

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

            background:
                radial-gradient(
                    circle,
                    #b8f8ff,
                    #36d9ff 30%,
                    #0a5074 65%,
                    #061222
                );

            color: #00131a;
            font-weight: bold;

            box-shadow:
                0 0 30px rgba(56, 217, 255, 0.4);
        }

        .brand h1 {
            font-size: 22px;
            letter-spacing: 3px;
        }

        .brand p {
            margin-top: 3px;
            color: #7d95ac;
            font-size: 9px;
            letter-spacing: 1.5px;
        }

        .online {
            display: flex;
            align-items: center;
            gap: 7px;

            padding: 7px 10px;

            border-radius: 999px;

            background: rgba(63, 255, 168, 0.06);

            color: #68efae;
            font-size: 11px;
        }

        .online-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #55ef9f;
            box-shadow: 0 0 10px #55ef9f;
        }

        .hero {
            display: grid;
            place-items: center;
            padding: 20px 10px 8px;
        }

        .orb {
            width: 92px;
            height: 92px;

            display: grid;
            place-items: center;

            border-radius: 50%;

            background:
                radial-gradient(
                    circle at 35% 30%,
                    #ecffff,
                    #58e8ff 18%,
                    #08749d 48%,
                    #061322 73%
                );

            box-shadow:
                0 0 35px rgba(56, 217, 255, 0.45),
                0 0 90px rgba(56, 217, 255, 0.15);

            animation: pulse 3s ease-in-out infinite;

            position: relative;
        }

        .orb::before {
            content: "";
            position: absolute;
            inset: -11px;

            border-radius: 50%;

            border:
                1px solid rgba(90, 225, 255, 0.35);

            animation: spin 8s linear infinite;
        }

        .orb::after {
            content: "";
            position: absolute;
            inset: -20px;

            border-radius: 50%;

            border:
                1px solid rgba(90, 225, 255, 0.10);

            border-left-color:
                rgba(90, 225, 255, 0.60);

            animation: spinReverse 12s linear infinite;
        }

        .orb-core {
            width: 22px;
            height: 22px;

            border-radius: 50%;

            background: white;

            box-shadow:
                0 0 28px white;
        }

        @keyframes pulse {

            0%, 100% {
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

        .hero-title {
            margin-top: 12px;
            color: #68dcff;
            font-size: 13px;
            letter-spacing: 2px;
        }

        .chat {
            flex: 1;

            overflow-y: auto;

            padding: 10px 22px 18px;
        }

        .chat::-webkit-scrollbar {
            width: 5px;
        }

        .chat::-webkit-scrollbar-thumb {
            background: #18334c;
            border-radius: 999px;
        }

        .message-row {
            display: flex;
            margin: 10px 0;
        }

        .message-row.user {
            justify-content: flex-end;
        }

        .message-row.ai {
            justify-content: flex-start;
        }

        .message {
            max-width: 82%;

            padding: 12px 14px;

            border-radius: 17px;

            font-size: 14px;
            line-height: 1.55;

            white-space: pre-wrap;
            word-break: break-word;
        }

        .message.user {
            background:
                linear-gradient(
                    135deg,
                    #0b5574,
                    #123957
                );

            border-bottom-right-radius: 5px;
        }

        .message.ai {
            background: rgba(18, 31, 57, 0.88);

            border:
                1px solid
                rgba(100, 220, 255, 0.08);

            border-bottom-left-radius: 5px;
        }

        .sender {
            color: #7f9ab2;
            font-size: 9px;
            letter-spacing: 1px;
            margin-bottom: 5px;
        }

        .quick {
            display: flex;
            gap: 8px;

            overflow-x: auto;

            padding: 0 22px 12px;
        }

        .quick::-webkit-scrollbar {
            display: none;
        }

        .quick button {
            flex: 0 0 auto;

            padding: 9px 13px;

            border-radius: 999px;

            border:
                1px solid
                rgba(82, 207, 255, 0.11);

            background:
                rgba(14, 28, 51, 0.8);

            color: #c7edff;

            cursor: pointer;
        }

        .composer {
            padding: 12px 18px 15px;

            border-top:
                1px solid rgba(255, 255, 255, 0.06);

            background:
                rgba(2, 7, 16, 0.8);
        }

        .input-wrap {
            display: flex;
            gap: 7px;
            align-items: center;

            padding: 6px;

            border-radius: 18px;

            border:
                1px solid
                rgba(82, 207, 255, 0.13);

            background:
                rgba(12, 22, 40, 0.96);
        }

        input {
            flex: 1;
            min-width: 0;

            border: none;
            outline: none;

            background: transparent;

            color: white;

            font-size: 15px;

            padding: 12px 10px;
        }

        input::placeholder {
            color: #59728a;
        }

        button {
            font-family: inherit;
        }

        .send {
            height: 42px;
            min-width: 72px;

            border: none;
            border-radius: 13px;

            background:
                linear-gradient(
                    135deg,
                    #9af3ff,
                    #2ac8ef
                );

            color: #00131a;

            font-weight: bold;

            cursor: pointer;
        }

        .send:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .status {
            text-align: center;

            margin-top: 7px;

            color: #526c85;

            font-size: 9px;

            letter-spacing: 1px;
        }

        .typing {
            display: none;
            gap: 4px;

            padding: 10px 13px;

            width: fit-content;

            border-radius: 14px;

            background:
                rgba(18, 31, 57, 0.88);
        }

        .typing span {
            width: 6px;
            height: 6px;

            border-radius: 50%;

            background: #46dfff;

            animation: typing 1s infinite;
        }

        .typing span:nth-child(2) {
            animation-delay: .15s;
        }

        .typing span:nth-child(3) {
            animation-delay: .3s;
        }

        @keyframes typing {

            0%, 100% {
                opacity: .3;
                transform: translateY(0);
            }

            50% {
                opacity: 1;
                transform: translateY(-3px);
            }
        }

        @media (max-width: 700px) {

            .app {
                padding: 0;
            }

            .shell {
                width: 100%;
                height: 100svh;
                border-radius: 0;
                border: none;
            }

            .header {
                padding: 15px 16px;
            }

            .chat {
                padding-left: 15px;
                padding-right: 15px;
            }

            .quick {
                padding-left: 15px;
                padding-right: 15px;
            }

            .message {
                max-width: 92%;
                font-size: 13px;
            }

            .brand h1 {
                font-size: 17px;
            }

            .brand p {
                font-size: 8px;
            }

            .logo {
                width: 39px;
                height: 39px;
            }

            .online {
                font-size: 9px;
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
                    <h1>KULDEEP AI</h1>
                    <p>GEMINI INTELLIGENCE</p>
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


        <section class="chat" id="chat">

            <div class="message-row ai">

                <div class="message ai">

                    <div class="sender">
                        JARVIS
                    </div>

                    Hello Kuldeep 👋
                    Ask me anything.

                </div>

            </div>

            <div
                class="message-row ai"
                id="typing-row"
                style="display:none;"
            >

                <div
                    class="typing"
                    id="typing"
                >
                    <span></span>
                    <span></span>
                    <span></span>
                </div>

            </div>

        </section>


        <div class="quick">

            <button onclick="quickAsk('What is Python?')">
                🐍 Python
            </button>

            <button onclick="quickAsk('Explain Artificial Intelligence')">
                🤖 AI
            </button>

            <button onclick="quickAsk('What is React?')">
                ⚛ React
            </button>

            <button onclick="quickAsk('Explain JavaScript')">
                JS
            </button>

            <button onclick="quickAsk('Give me a programming tip')">
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
                    class="send"
                    id="send"
                    onclick="askGemini()"
                >
                    ASK
                </button>

            </div>

            <div
                class="status"
                id="status"
            >
                SECURE • AI ONLINE • READY
            </div>

        </footer>

    </main>

</div>


<script>

const input =
    document.getElementById("question");

const chat =
    document.getElementById("chat");

const typing =
    document.getElementById("typing");

const typingRow =
    document.getElementById("typing-row");

const status =
    document.getElementById("status");

const send =
    document.getElementById("send");


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


function quickAsk(question) {

    input.value = question;

    askGemini();

}


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


    const senderEl =
        document.createElement("div");

    senderEl.className =
        "sender";

    senderEl.textContent =
        sender;


    const content =
        document.createElement("div");

    content.textContent =
        text;


    box.appendChild(senderEl);

    box.appendChild(content);

    row.appendChild(box);


    chat.insertBefore(
        row,
        typingRow
    );


    chat.scrollTop =
        chat.scrollHeight;
}


function showTyping() {

    typingRow.style.display =
        "flex";

    typing.style.display =
        "flex";

    status.textContent =
        "JARVIS IS THINKING...";

    chat.scrollTop =
        chat.scrollHeight;
}


function hideTyping() {

    typingRow.style.display =
        "none";

    typing.style.display =
        "none";

    status.textContent =
        "SECURE • AI ONLINE • READY";
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


    input.value = "";

    input.disabled = true;

    send.disabled = true;


    showTyping();


    try {

        const response =
            await fetch(
                "/ask",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        question: question
                    })
                }
            );


        const data =
            await response.json();


        hideTyping();


        if (
            response.ok &&
            data.success
        ) {

            addMessage(
                "JARVIS",
                data.answer,
                "ai"
            );

        } else {

            addMessage(
                "ERROR",
                data.message ||
                "Gemini request failed.",
                "ai"
            );

        }


    } catch (error) {

        hideTyping();

        addMessage(
            "ERROR",
            "Unable to connect to Jarvis.",
            "ai"
        );

        console.error(error);

    }


    input.disabled = false;

    send.disabled = false;

    input.focus();

}

</script>

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
# HEALTH
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
        "message": "Use the web interface or POST /ask."
    })


# =========================================================
# ASK - POST
# =========================================================

@app.post("/ask")
def ask():

    data = request.get_json(silent=True) or {}

    question = str(
        data.get("question", "")
    ).strip()

    if not question:
        return jsonify({
            "success": False,
            "message": "Question is required."
        }), 400

    if not client:
        return jsonify({
            "success": False,
            "message": "GEMINI_API_KEY is not configured."
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
            "message": "Gemini request failed.",
            "error": str(error)
        }), 500


# =========================================================
# RUN
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
