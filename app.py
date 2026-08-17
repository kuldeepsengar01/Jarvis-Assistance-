import os

from flask import Flask, request, jsonify, render_template_string
from dotenv import load_dotenv
from google import genai


# =========================================================
# ENV
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
# FLASK
# =========================================================

app = Flask(__name__)


# =========================================================
# WEB UI
# =========================================================

HTML = r"""
<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0, viewport-fit=cover"
    >

    <meta name="theme-color" content="#050816">

    <title>Kuldeep AI</title>

    <style>

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        :root {
            --bg: #030712;
            --panel: rgba(10, 18, 38, 0.78);
            --panel-2: rgba(16, 28, 55, 0.75);
            --border: rgba(106, 220, 255, 0.16);
            --cyan: #38d9ff;
            --cyan-soft: #71e8ff;
            --text: #f4fbff;
            --muted: #8ba4bb;
            --user: linear-gradient(135deg, #0d5b78, #123a58);
            --ai: rgba(17, 29, 53, 0.88);
        }

        html,
        body {
            width: 100%;
            min-height: 100%;
        }

        body {

            font-family:
                Inter,
                system-ui,
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;

            background:
                radial-gradient(
                    circle at 20% 10%,
                    rgba(0, 205, 255, 0.12),
                    transparent 30%
                ),
                radial-gradient(
                    circle at 80% 20%,
                    rgba(77, 90, 255, 0.10),
                    transparent 30%
                ),
                linear-gradient(
                    135deg,
                    #02050d,
                    #050b19 50%,
                    #020611
                );

            color: var(--text);

            min-height: 100svh;

            overflow: hidden;
        }

        /* BACKGROUND STARS */

        body::before {
            content: "";
            position: fixed;
            inset: 0;

            background-image:
                radial-gradient(
                    rgba(255,255,255,0.7) 1px,
                    transparent 1px
                );

            background-size: 44px 44px;

            opacity: 0.10;

            pointer-events: none;
        }


        /* APP */

        .app {

            width: 100%;
            height: 100svh;

            display: flex;
            justify-content: center;
            align-items: center;

            padding: 22px;
        }


        /* MAIN CARD */

        .shell {

            width: min(1050px, 100%);

            height: min(900px, 94svh);

            display: flex;
            flex-direction: column;

            border: 1px solid var(--border);

            border-radius: 30px;

            background: var(--panel);

            backdrop-filter: blur(22px);
            -webkit-backdrop-filter: blur(22px);

            box-shadow:
                0 30px 90px rgba(0,0,0,0.55),
                0 0 80px rgba(0,200,255,0.07);

            overflow: hidden;
        }


        /* HEADER */

        .header {

            display: flex;

            justify-content: space-between;
            align-items: center;

            padding:
                20px 24px;

            border-bottom:
                1px solid rgba(255,255,255,0.06);
        }

        .brand {

            display: flex;
            align-items: center;
            gap: 13px;
        }

        .logo {

            width: 46px;
            height: 46px;

            display: grid;
            place-items: center;

            border-radius: 15px;

            background:
                radial-gradient(
                    circle,
                    #67e8ff 0%,
                    #157ea8 35%,
                    #071629 72%
                );

            box-shadow:
                0 0 28px
                rgba(56,217,255,0.25);

            font-size: 20px;
        }

        .brand h1 {

            font-size: clamp(18px, 3vw, 25px);

            letter-spacing: 3px;
        }

        .brand p {

            margin-top: 3px;

            color: var(--muted);

            font-size: 11px;

            letter-spacing: 1.4px;
        }


        .online {

            display: flex;
            align-items: center;
            gap: 8px;

            padding: 8px 12px;

            border-radius: 999px;

            background:
                rgba(61, 255, 166, 0.07);

            color: #70f5b5;

            font-size: 12px;
        }

        .online-dot {

            width: 7px;
            height: 7px;

            border-radius: 50%;

            background: #55f3a5;

            box-shadow:
                0 0 12px #55f3a5;
        }


        /* HERO */

        .hero {

            display: grid;

            place-items: center;

            padding: 20px 20px 4px;
        }

        .orb {

            position: relative;

            width: 110px;
            height: 110px;

            display: grid;
            place-items: center;

            border-radius: 50%;

            background:
                radial-gradient(
                    circle at 35% 30%,
                    #bbf8ff,
                    #49dfff 20%,
                    #08749f 48%,
                    #061326 72%
                );

            box-shadow:
                0 0 35px rgba(56,217,255,0.5),
                0 0 90px rgba(56,217,255,0.18);

            animation:
                pulse 3s ease-in-out infinite;
        }

        .orb::before {

            content: "";

            position: absolute;

            inset: -12px;

            border-radius: 50%;

            border:
                1px solid rgba(90,225,255,0.38);

            animation:
                spin 8s linear infinite;
        }

        .orb::after {

            content: "";

            position: absolute;

            inset: -22px;

            border-radius: 50%;

            border:
                1px solid rgba(90,225,255,0.11);

            border-left-color:
                rgba(90,225,255,0.65);

            animation:
                spinReverse 12s linear infinite;
        }

        .orb-core {

            width: 28px;
            height: 28px;

            border-radius: 50%;

            background: #eaffff;

            box-shadow:
                0 0 30px #dffcff;

        }

        @keyframes pulse {

            0%,
            100% {
                transform: scale(1);
            }

            50% {
                transform: scale(1.04);
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

            margin-top: 13px;

            font-size: clamp(14px, 2vw, 17px);

            color: var(--cyan-soft);

            letter-spacing: 2px;
        }


        /* CHAT */

        .chat {

            flex: 1;

            overflow-y: auto;

            padding:
                14px
                24px
                20px;

            scroll-behavior: smooth;
        }

        .chat::-webkit-scrollbar {
            width: 5px;
        }

        .chat::-webkit-scrollbar-thumb {
            background: #18304b;
            border-radius: 999px;
        }


        .message-row {

            display: flex;

            margin:
                11px 0;
        }

        .message-row.user {

            justify-content: flex-end;
        }

        .message-row.ai {

            justify-content: flex-start;
        }


        .message {

            max-width: min(760px, 82%);

            padding:
                13px
                15px;

            border-radius: 18px;

            line-height: 1.55;

            font-size: 14px;

            white-space: pre-wrap;

            word-break: break-word;
        }

        .message.user {

            background: var(--user);

            border-bottom-right-radius: 5px;

            box-shadow:
                0 8px 25px
                rgba(0,0,0,0.18);
        }

        .message.ai {

            background: var(--ai);

            border:
                1px solid
                rgba(100,220,255,0.08);

            border-bottom-left-radius: 5px;
        }

        .sender {

            font-size: 10px;

            color: var(--muted);

            margin-bottom: 5px;

            letter-spacing: 1px;
        }


        /* TYPING */

        .typing {

            display: none;

            align-items: center;

            gap: 5px;

            padding: 12px 14px;

            width: fit-content;

            border-radius: 16px;

            background: var(--ai);
        }

        .typing span {

            width: 6px;
            height: 6px;

            border-radius: 50%;

            background: var(--cyan);

            animation:
                typing 1.2s infinite;
        }

        .typing span:nth-child(2) {
            animation-delay: .15s;
        }

        .typing span:nth-child(3) {
            animation-delay: .3s;
        }

        @keyframes typing {

            0%,
            60%,
            100% {
                opacity: .25;
                transform: translateY(0);
            }

            30% {
                opacity: 1;
                transform: translateY(-3px);
            }
        }


        /* QUICK ACTIONS */

        .quick {

            display: flex;

            gap: 8px;

            overflow-x: auto;

            padding:
                0
                24px
                13px;
        }

        .quick::-webkit-scrollbar {
            display: none;
        }

        .quick button {

            flex:
                0 0 auto;

            border:
                1px solid
                rgba(86,208,255,0.10);

            background:
                rgba(15,29,52,0.72);

            color: #ccecff;

            padding:
                9px
                13px;

            border-radius: 999px;

            cursor: pointer;

            font-size: 12px;

            transition:
                .2s ease;
        }

        .quick button:hover {

            border-color:
                rgba(56,217,255,0.38);

            transform:
                translateY(-1px);
        }


        /* INPUT */

        .composer {

            padding:
                13px
                18px
                max(
                    15px,
                    env(safe-area-inset-bottom)
                );

            border-top:
                1px solid
                rgba(255,255,255,0.06);

            background:
                rgba(3,8,18,0.65);
        }

        .input-wrap {

            display: flex;

            align-items: center;

            gap: 8px;

            padding: 6px;

            border:
                1px solid
                rgba(84,211,255,0.13);

            border-radius: 18px;

            background:
                rgba(11,20,38,0.95);

            transition: .2s ease;
        }

        .input-wrap:focus-within {

            border-color:
                rgba(56,217,255,0.48);

            box-shadow:
                0 0 25px
                rgba(56,217,255,0.08);
        }


        input {

            flex: 1;

            min-width: 0;

            border: none;

            outline: none;

            background: transparent;

            color: white;

            font-size: 15px;

            padding:
                12px
                10px;
        }

        input::placeholder {
            color: #58718b;
        }


        .icon-btn,
        .send-btn {

            border: none;

            cursor: pointer;

            display: grid;

            place-items: center;

            flex-shrink: 0;
        }

        .icon-btn {

            width: 42px;
            height: 42px;

            border-radius: 13px;

            color: #9fd9ec;

            background:
                rgba(31,51,77,0.72);

            font-size: 17px;
        }

        .send-btn {

            min-width: 74px;

            height: 42px;

            padding: 0 16px;

            border-radius: 13px;

            color: #00141d;

            background:
                linear-gradient(
                    135deg,
                    #8ff3ff,
                    #30ccef
                );

            font-weight: 800;

            font-size: 12px;

            letter-spacing: .8px;

            box-shadow:
                0 7px 20px
                rgba(48,204,239,.14);
        }


        .footer-status {

            text-align: center;

            color: #506a82;

            font-size: 10px;

            margin-top: 7px;

            letter-spacing: 1px;
        }


        /* TABLET */

        @media (max-width: 800px) {

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
                padding:
                    15px 17px;
            }

            .chat {
                padding:
                    10px
                    16px
                    16px;
            }

            .quick {
                padding-left: 16px;
                padding-right: 16px;
            }

            .message {
                max-width: 88%;
            }
        }


        /* MOBILE */

        @media (max-width: 520px) {

            .brand h1 {
                font-size: 17px;
                letter-spacing: 2px;
            }

            .brand p {
                font-size: 8px;
            }

            .logo {
                width: 40px;
                height: 40px;
                border-radius: 12px;
            }

            .online {
                font-size: 10px;
                padding: 7px 9px;
            }

            .hero {
                padding-top: 15px;
            }

            .orb {
                width: 82px;
                height: 82px;
            }

            .orb-core {
                width: 20px;
                height: 20px;
            }

            .hero-title {
                font-size: 12px;
                margin-top: 10px;
            }

            .message {
                max-width: 92%;
                font-size: 13px;
                padding: 11px 13px;
            }

            .composer {
                padding:
                    10px
                    10px
                    max(
                        10px,
                        env(safe-area-inset-bottom)
                    );
            }

            input {
                font-size: 14px;
            }

            .send-btn {
                min-width: 58px;
                padding: 0 11px;
            }

            .icon-btn {
                width: 38px;
                height: 38px;
            }

        }

    </style>

</head>


<body>

<div class="app">

    <main class="shell">


        <!-- HEADER -->

        <header class="header">

            <div class="brand">

                <div class="logo">
                    ◉
                </div>

                <div>
                    <h1>KULDEEP AI</h1>

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


        <!-- HERO -->

        <section class="hero">

            <div class="orb">
                <div class="orb-core"></div>
            </div>

            <div class="hero-title">
                JARVIS IS READY
            </div>

        </section>


        <!-- CHAT -->

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


            <div
                class="message-row ai"
                id="typing-row"
            >

                <div class="typing" id="typing">

                    <span></span>
                    <span></span>
                    <span></span>

                </div>

            </div>

        </section>


        <!-- QUICK -->

        <div class="quick">

            <button onclick="quickAsk('What is Python?')">
                🐍 Python
            </button>

            <button onclick="quickAsk('Explain artificial intelligence')">
                🤖 AI
            </button>

            <button onclick="quickAsk('Tell me about JavaScript')">
                JS
            </button>

            <button onclick="quickAsk('What is React?')">
                ⚛ React
            </button>

            <button onclick="quickAsk('Give me a programming tip')">
                💡 Tip
            </button>

        </div>


        <!-- COMPOSER -->

        <footer class="composer">

            <div class="input-wrap">

                <button
                    class="icon-btn"
                    onclick="focusInput()"
                    title="Focus"
                >
                    ✦
                </button>


                <input
                    id="question"
                    type="text"
                    autocomplete="off"
                    placeholder="Ask Jarvis anything..."
                >


                <button
                    class="send-btn"
                    onclick="askGemini()"
                >
                    ASK
                </button>

            </div>


            <div
                class="footer-status"
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


    input.addEventListener(
        "keydown",
        function(event) {

            if (
                event.key === "Enter"
                && !event.shiftKey
            ) {

                event.preventDefault();

                askGemini();
            }

        }
    );


    function focusInput() {

        input.focus();

    }


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


        const message =
            document.createElement("div");

        message.className =
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


        message.appendChild(
            senderElement
        );

        message.appendChild(
            content
        );

        row.appendChild(
            message
        );


        chat.insertBefore(
            row,
            typingRow
        );


        chat.scrollTo({
            top: chat.scrollHeight,
            behavior: "smooth"
        });

    }


    function showTyping() {

        typing.style.display =
            "flex";

        typingRow.style.display =
            "flex";

        status.textContent =
            "JARVIS IS THINKING...";


        chat.scrollTo({
            top: chat.scrollHeight,
            behavior: "smooth"
        });

    }


    function hideTyping() {

        typing.style.display =
            "none";

        typingRow.style.display =
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

                        body:
                            JSON.stringify({
                                question:
                                    question
                            })
                    }
                );


            const data =
                await response.json();


            hideTyping();


            if (
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
                    "Something went wrong.",
                    "ai"
                );

            }

        } catch (error) {

            hideTyping();

            addMessage(
                "ERROR",
                "Unable to connect to Jarvis server.",
                "ai"
            );

            console.error(error);

        } finally {

            input.disabled = false;

            input.focus();

        }

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

    return render_template_string(
        HTML
    )


# =========================================================
# HEALTH
# =========================================================

@app.get("/health")
def health():

    return jsonify({
        "status": "ok",
        "gemini_configured":
            client is not None
    })


# =========================================================
# ASK - GET
# =========================================================

@app.get("/ask")
def ask_get():

    return jsonify({
        "success": True,
        "message":
            "Use the web interface or POST /ask."
    })


# =========================================================
# ASK - POST
# =========================================================

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
            "message":
                "Question is required."
        }), 400


    if not client:

        return jsonify({
            "success": False,
            "message":
                "GEMINI_API_KEY is not configured."
        }), 500


    try:

        interaction =
            client.interactions.create(
                model="gemini-3.6-flash",
                input=question
            )


        answer =
            interaction.output_text


        return jsonify({
            "success": True,
            "question": question,
            "answer": answer
        })


    except Exception as error:

        print(
            "Gemini Error:",
            error
        )


        return jsonify({
            "success": False,
            "message":
                "Gemini request failed.",
            "error":
                str(error)
        }), 500


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )


    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
