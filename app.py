import os
import requests

from flask import (
    Flask,
    request,
    jsonify,
    render_template_string,
    Response,
)

from dotenv import load_dotenv


# =====================================================
# ENV
# =====================================================

load_dotenv()

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

if GEMINI_API_KEY:
    print(
        "Gemini API key loaded successfully."
    )
else:
    print(
        "WARNING: GEMINI_API_KEY is not configured."
    )


# =====================================================
# FLASK
# =====================================================

app = Flask(__name__)


# =====================================================
# HTML
# =====================================================

HTML = r"""
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
/>

<meta
    name="theme-color"
    content="#030712"
/>

<title>Kuldeep AI</title>


<style>

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}


body {

    min-height: 100vh;

    font-family:
        Arial,
        Helvetica,
        sans-serif;

    color: white;

    background:
        radial-gradient(
            circle at 20% 10%,
            rgba(0, 217, 255, 0.15),
            transparent 30%
        ),

        radial-gradient(
            circle at 80% 20%,
            rgba(80, 80, 255, 0.12),
            transparent 30%
        ),

        linear-gradient(
            135deg,
            #02040a,
            #06111f,
            #02050c
        );
}


.app {

    min-height: 100vh;

    padding: 20px;

    display: flex;

    justify-content: center;

    align-items: center;
}


.shell {

    width: min(
        1050px,
        100%
    );

    height: min(
        900px,
        94vh
    );

    display: flex;

    flex-direction: column;

    overflow: hidden;

    border-radius: 28px;

    border:
        1px solid
        rgba(
            100,
            220,
            255,
            0.16
        );

    background:
        rgba(
            7,
            15,
            31,
            0.90
        );

    box-shadow:
        0 30px 100px
        rgba(
            0,
            0,
            0,
            0.55
        ),

        0 0 90px
        rgba(
            0,
            210,
            255,
            0.08
        );

    backdrop-filter:
        blur(20px);
}


.header {

    display: flex;

    justify-content:
        space-between;

    align-items: center;

    padding:
        18px 22px;

    border-bottom:
        1px solid
        rgba(
            255,
            255,
            255,
            0.06
        );
}


.brand {

    display: flex;

    align-items: center;

    gap: 12px;
}


.logo {

    width: 46px;

    height: 46px;

    display: grid;

    place-items: center;

    border-radius: 15px;

    font-size: 20px;

    color: #00151c;

    background:
        radial-gradient(
            circle,
            #e9ffff,
            #47dcff 30%,
            #087399 55%,
            #071221 75%
        );

    box-shadow:
        0 0 30px
        rgba(
            54,
            217,
            255,
            0.40
        );
}


.brand h1 {

    font-size: 22px;

    letter-spacing: 3px;
}


.brand p {

    margin-top: 3px;

    font-size: 9px;

    letter-spacing: 1.5px;

    color:
        #7c96ae;
}


.online {

    display: flex;

    align-items: center;

    gap: 7px;

    padding:
        7px 11px;

    border-radius: 999px;

    color:
        #67efaf;

    background:
        rgba(
            70,
            255,
            170,
            0.07
        );

    font-size: 10px;
}


.online-dot {

    width: 7px;

    height: 7px;

    border-radius: 50%;

    background:
        #52ee9f;

    box-shadow:
        0 0 12px
        #52ee9f;
}


.hero {

    display: grid;

    place-items: center;

    padding:
        22px 10px 12px;
}


.orb {

    width: 98px;

    height: 98px;

    position: relative;

    display: grid;

    place-items: center;

    border-radius: 50%;

    background:
        radial-gradient(
            circle at 35% 30%,
            #efffff,
            #5ce9ff 18%,
            #08739c 47%,
            #061322 73%
        );

    box-shadow:
        0 0 40px
        rgba(
            56,
            217,
            255,
            0.45
        ),

        0 0 100px
        rgba(
            56,
            217,
            255,
            0.14
        );

    animation:
        pulse 3s
        ease-in-out
        infinite;
}


.orb::before {

    content: "";

    position: absolute;

    inset: -12px;

    border-radius: 50%;

    border:
        1px solid
        rgba(
            90,
            225,
            255,
            0.35
        );

    animation:
        spin 8s linear infinite;
}


.orb::after {

    content: "";

    position: absolute;

    inset: -22px;

    border-radius: 50%;

    border:
        1px solid
        rgba(
            90,
            225,
            255,
            0.10
        );

    border-left-color:
        rgba(
            90,
            225,
            255,
            0.65
        );

    animation:
        spinReverse
        12s linear infinite;
}


.orb-core {

    width: 24px;

    height: 24px;

    border-radius: 50%;

    background: white;

    box-shadow:
        0 0 30px white;
}


@keyframes pulse {

    0%,
    100% {
        transform:
            scale(1);
    }

    50% {
        transform:
            scale(1.05);
    }
}


@keyframes spin {

    to {
        transform:
            rotate(360deg);
    }
}


@keyframes spinReverse {

    to {
        transform:
            rotate(-360deg);
    }
}


.hero-title {

    margin-top: 13px;

    color:
        #68deff;

    font-size: 12px;

    letter-spacing: 2px;
}


.chat {

    flex: 1;

    overflow-y: auto;

    padding:
        10px 22px 18px;

    scroll-behavior:
        smooth;
}


.chat::-webkit-scrollbar {

    width: 5px;
}


.chat::-webkit-scrollbar-thumb {

    background:
        #18334b;

    border-radius:
        999px;
}


.message-row {

    display: flex;

    margin:
        10px 0;
}


.message-row.user {

    justify-content:
        flex-end;
}


.message-row.ai {

    justify-content:
        flex-start;
}


.message {

    max-width:
        82%;

    padding:
        12px 14px;

    border-radius:
        17px;

    line-height:
        1.55;

    font-size:
        14px;

    white-space:
        pre-wrap;

    word-break:
        break-word;
}


.message.user {

    background:
        linear-gradient(
            135deg,
            #0a5776,
            #123958
        );

    border-bottom-right-radius:
        5px;
}


.message.ai {

    background:
        rgba(
            17,
            30,
            54,
            0.90
        );

    border:
        1px solid
        rgba(
            100,
            220,
            255,
            0.08
        );

    border-bottom-left-radius:
        5px;
}


.sender {

    margin-bottom:
        5px;

    color:
        #7893ab;

    font-size:
        9px;

    letter-spacing:
        1px;
}


.quick {

    display: flex;

    gap: 8px;

    overflow-x: auto;

    padding:
        0 22px 12px;
}


.quick::-webkit-scrollbar {

    display: none;
}


.quick button {

    flex:
        0 0 auto;

    border:
        1px solid
        rgba(
            80,
            210,
            255,
            0.12
        );

    border-radius:
        999px;

    padding:
        9px 14px;

    color:
        #c9efff;

    background:
        rgba(
            14,
            29,
            52,
            0.80
        );

    cursor:
        pointer;
}


.composer {

    padding:
        12px 18px 15px;

    border-top:
        1px solid
        rgba(
            255,
            255,
            255,
            0.06
        );

    background:
        rgba(
            3,
            8,
            17,
            0.80
        );
}


.input-wrap {

    display:
        flex;

    align-items:
        center;

    gap:
        7px;

    padding:
        6px;

    border-radius:
        18px;

    border:
        1px solid
        rgba(
            80,
            210,
            255,
            0.14
        );

    background:
        rgba(
            11,
            22,
            40,
            0.96
        );
}


input {

    flex:
        1;

    min-width:
        0;

    border:
        none;

    outline:
        none;

    background:
        transparent;

    color:
        white;

    padding:
        12px 10px;

    font-size:
        15px;
}


input::placeholder {

    color:
        #59728a;
}


.mic,
.send {

    flex-shrink:
        0;

    border:
        none;

    cursor:
        pointer;
}


.mic {

    width:
        44px;

    height:
        44px;

    border-radius:
        13px;

    color:
        white;

    background:
        rgba(
            35,
            55,
            80,
            0.90
        );

    font-size:
        18px;
}


.mic.listening {

    background:
        #ef4444;

    box-shadow:
        0 0 25px
        rgba(
            239,
            68,
            68,
            0.45
        );
}


.send {

    height:
        44px;

    min-width:
        74px;

    border-radius:
        13px;

    background:
        linear-gradient(
            135deg,
            #9af4ff,
            #2bc8ef
        );

    color:
        #00131a;

    font-weight:
        bold;
}


.status {

    margin-top:
        7px;

    text-align:
        center;

    color:
        #526c84;

    font-size:
        9px;

    letter-spacing:
        1px;
}


@media (
    max-width: 700px
) {

    .app {

        padding:
            0;
    }


    .shell {

        width:
            100%;

        height:
            100svh;

        border:
            none;

        border-radius:
            0;
    }


    .header {

        padding:
            14px 15px;
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


    .chat {

        padding:
            10px 15px 16px;
    }


    .message {

        max-width:
            92%;

        font-size:
            13px;
    }


    .quick {

        padding:
            0 15px 11px;
    }


    .composer {

        padding:
            10px 10px
            max(
                10px,
                env(
                    safe-area-inset-bottom
                )
            );
    }


    input {

        font-size:
            14px;
    }


    .send {

        min-width:
            62px;
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
/>


<button
    class="mic"
    id="mic"
    onclick="startListening()"
>
🎤
</button>


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
● SECURE • AI ONLINE • READY
</div>

</footer>


</main>

</div>


<script src="/speech.js"></script>

</body>

</html>
"""


# =====================================================
# HOME
# =====================================================

@app.get("/")
def home():

    return render_template_string(
        HTML
    )


# =====================================================
# SPEECH JS
# =====================================================

@app.get("/speech.js")
def speech_js():

    js_path = os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)
        ),
        "speech.js"
    )

    try:

        with open(
            js_path,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read()

        return Response(
            content,
            mimetype="application/javascript"
        )

    except FileNotFoundError:

        return Response(
            "console.error('speech.js not found');",
            mimetype="application/javascript"
        ), 404


# =====================================================
# HEALTH
# =====================================================

@app.get("/health")
def health():

    return jsonify({
        "status": "ok",
        "gemini_configured":
            bool(GEMINI_API_KEY)
    })


# =====================================================
# ASK
# =====================================================

@app.get("/ask")
def ask_get():

    return jsonify({
        "success": True,
        "message":
            "Use POST /ask or the web interface."
    })


# =====================================================
# GEMINI ASK
# =====================================================

@app.post("/ask")
def ask():

    data = (
        request.get_json(
            silent=True
        )
        or {}
    )


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


    if not GEMINI_API_KEY:

        return jsonify({
            "success": False,
            "message":
                "GEMINI_API_KEY is not configured."
        }), 500


    try:

        url = (
            "https://generativelanguage.googleapis.com"
            "/v1beta/interactions"
        )


        headers = {

            "x-goog-api-key":
                GEMINI_API_KEY,

            "Content-Type":
                "application/json",

        }


        # Enable Google Search only when
        # the user explicitly asks for search/current info.

        search_words = [
            "search",
            "latest",
            "today",
            "news",
            "current",
            "recent",
            "who won",
        ]


        use_search = any(
            word in question.lower()
            for word in search_words
        )


        payload = {

            "model":
                "gemini-3.6-flash",

            "input":
                question,
        }


        if use_search:

            payload["tools"] = [
                {
                    "type":
                        "google_search"
                }
            ]


        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=90
        )


        if not response.ok:

            print(
                "Gemini HTTP error:",
                response.status_code,
                response.text
            )

            return jsonify({

                "success":
                    False,

                "message":
                    "Gemini API request failed.",

                "error":
                    response.text

            }), 502


        result = response.json()


        answer = (
            result.get(
                "output_text"
            )
            or ""
        )


        # Fallback extraction
        # for responses where output_text
        # is not directly present.

        if not answer:

            for step in result.get(
                "steps",
                []
            ):

                if step.get(
                    "type"
                ) == "model_output":

                    for block in step.get(
                        "content",
                        []
                    ):

                        if block.get(
                            "type"
                        ) == "text":

                            answer += (
                                block.get(
                                    "text",
                                    ""
                                )
                            )


        if not answer:

            answer = (
                "Gemini returned no text response."
            )


        return jsonify({

            "success":
                True,

            "question":
                question,

            "answer":
                answer,

        })


    except requests.RequestException as error:

        print(
            "Network error:",
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
            "Server error:",
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


# =====================================================
# START
# =====================================================

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
