const input = document.getElementById("question");
const chat = document.getElementById("chat");
const status = document.getElementById("status");
const sendButton = document.getElementById("send");
const micButton = document.getElementById("mic");

let recognition = null;
let isListening = false;


// =====================================================
// CHAT MESSAGE
// =====================================================

function addMessage(sender, text, type) {

    const row = document.createElement("div");
    row.className = `message-row ${type}`;

    const box = document.createElement("div");
    box.className = `message ${type}`;

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


// =====================================================
// TEXT TO SPEECH
// =====================================================

function speak(text) {

    if (!("speechSynthesis" in window)) {
        return;
    }

    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);

    utterance.lang = "en-IN";
    utterance.rate = 1;
    utterance.pitch = 1;

    window.speechSynthesis.speak(utterance);
}


// =====================================================
// SPEECH RECOGNITION
// =====================================================

const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;


if (SpeechRecognition) {

    recognition = new SpeechRecognition();

    recognition.lang = "en-IN";
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;


    recognition.onstart = function () {

        isListening = true;

        micButton.classList.add("listening");
        micButton.textContent = "🛑";

        status.textContent = "🎤 LISTENING...";
    };


    recognition.onresult = function (event) {

        const transcript =
            event.results[0][0].transcript;

        input.value = transcript;

        status.textContent = "VOICE RECEIVED";

        askGemini();
    };


    recognition.onerror = function (event) {

        console.error(
            "Speech recognition error:",
            event.error
        );

        isListening = false;

        micButton.classList.remove("listening");
        micButton.textContent = "🎤";

        if (event.error === "not-allowed") {

            status.textContent =
                "MICROPHONE PERMISSION DENIED";

        } else if (event.error === "no-speech") {

            status.textContent =
                "NO SPEECH DETECTED";

        } else {

            status.textContent =
                "VOICE ERROR: " + event.error;
        }
    };


    recognition.onend = function () {

        isListening = false;

        micButton.classList.remove("listening");
        micButton.textContent = "🎤";

        if (
            status.textContent ===
            "🎤 LISTENING..."
        ) {

            status.textContent =
                "SECURE • AI ONLINE • READY";
        }
    };

} else {

    console.warn(
        "Speech Recognition is not supported."
    );

    micButton.disabled = true;
    micButton.textContent = "🚫";

    status.textContent = "VOICE NOT SUPPORTED";
}


// =====================================================
// START / STOP MICROPHONE
// =====================================================

function startListening() {

    if (!recognition) {

        addMessage(
            "JARVIS",
            "Speech recognition is not supported. Try Chrome or Edge.",
            "ai"
        );

        return;
    }


    if (isListening) {

        recognition.stop();

        return;
    }


    try {

        recognition.start();

    } catch (error) {

        console.error(
            "Speech start error:",
            error
        );

    }
}


// =====================================================
// ASK GEMINI
// =====================================================

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

    sendButton.disabled = true;
    micButton.disabled = true;

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


        // ---------------------------------------------
        // SAFE RESPONSE PARSING
        // ---------------------------------------------

        const contentType =
            response.headers.get("content-type") || "";

        const raw =
            await response.text();


        let data;


        if (
            contentType.includes(
                "application/json"
            )
        ) {

            try {

                data = JSON.parse(raw);

            } catch (parseError) {

                throw new Error(
                    "Server returned invalid JSON."
                );
            }

        } else {

            // Render/Flask returned HTML or plain text

            console.error(
                "Non-JSON server response:",
                raw
            );

            throw new Error(
                `Server returned ${response.status}: ${raw.slice(0, 300)}`
            );
        }


        // ---------------------------------------------
        // HTTP ERROR
        // ---------------------------------------------

        if (!response.ok) {

            throw new Error(
                data.error ||
                data.message ||
                `HTTP ${response.status}`
            );
        }


        // ---------------------------------------------
        // APPLICATION ERROR
        // ---------------------------------------------

        if (!data.success) {

            throw new Error(
                data.error ||
                data.message ||
                "Gemini request failed"
            );
        }


        // ---------------------------------------------
        // SUCCESS
        // ---------------------------------------------

        addMessage(
            "JARVIS",
            data.answer || "No answer received.",
            "ai"
        );


        speak(
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
            "Unable to connect to Jarvis.",
            "ai"
        );


        status.textContent =
            "⚠ REQUEST FAILED";


    } finally {

        sendButton.disabled = false;

        micButton.disabled =
            !recognition;

        input.focus();
    }
}


// =====================================================
// ENTER KEY
// =====================================================

input.addEventListener(
    "keydown",
    function (event) {

        if (
            event.key === "Enter"
        ) {

            event.preventDefault();

            askGemini();
        }
    }
);


// =====================================================
// GLOBAL
// =====================================================

window.askGemini = askGemini;
window.startListening = startListening;
