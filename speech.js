"use strict";

const input = document.getElementById("question");
const chat = document.getElementById("chat");
const status = document.getElementById("status");
const sendButton = document.getElementById("send");
const micButton = document.getElementById("mic");

let recognition = null;
let isListening = false;


// =====================================================
// MESSAGE
// =====================================================

function addMessage(sender, text, type) {

    if (!chat) {
        console.error("Chat element not found.");
        return;
    }

    const row = document.createElement("div");
    row.className = "message-row " + type;

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


// =====================================================
// STATUS
// =====================================================

function setStatus(text) {

    if (status) {
        status.textContent = text;
    }
}


// =====================================================
// TEXT TO SPEECH
// =====================================================

function speak(text) {

    if (!("speechSynthesis" in window)) {
        console.warn("Speech synthesis not supported.");
        return;
    }

    if (!text) {
        return;
    }

    window.speechSynthesis.cancel();

    const utterance =
        new SpeechSynthesisUtterance(text);

    utterance.lang = "en-IN";
    utterance.rate = 1;
    utterance.pitch = 1;
    utterance.volume = 1;

    window.speechSynthesis.speak(
        utterance
    );
}


// =====================================================
// BROWSER SPEECH RECOGNITION
// =====================================================

const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;


if (!SpeechRecognition) {

    console.error(
        "SpeechRecognition is not supported by this browser."
    );

    if (micButton) {
        micButton.disabled = true;
        micButton.textContent = "🚫";
    }

    setStatus(
        "VOICE NOT SUPPORTED"
    );

} else {

    recognition =
        new SpeechRecognition();

    recognition.lang = "en-IN";

    recognition.continuous = false;

    recognition.interimResults = false;

    recognition.maxAlternatives = 1;


    // =================================================
    // START
    // =================================================

    recognition.onstart = function () {

        isListening = true;

        if (micButton) {

            micButton.disabled = false;

            micButton.classList.add(
                "listening"
            );

            micButton.textContent = "🛑";
        }

        setStatus(
            "🎤 LISTENING..."
        );
    };


    // =================================================
    // RESULT
    // =================================================

    recognition.onresult = function (event) {

        try {

            const result =
                event.results[0];

            const transcript =
                result[0].transcript.trim();

            console.log(
                "Voice result:",
                transcript
            );


            if (!transcript) {

                setStatus(
                    "NO SPEECH DETECTED"
                );

                return;
            }


            input.value = transcript;

            setStatus(
                "VOICE RECEIVED"
            );


            // Automatically send to Gemini
            if (
                typeof window.askGemini ===
                "function"
            ) {

                window.askGemini();

            } else {

                console.error(
                    "askGemini() is not available."
                );

            }

        } catch (error) {

            console.error(
                "Result processing error:",
                error
            );

            setStatus(
                "VOICE RESULT ERROR"
            );
        }
    };


    // =================================================
    // ERROR
    // =================================================

    recognition.onerror = function (event) {

        console.error(
            "Speech recognition error:",
            event.error
        );


        isListening = false;


        if (micButton) {

            micButton.classList.remove(
                "listening"
            );

            micButton.textContent = "🎤";
        }


        switch (event.error) {

            case "not-allowed":

                setStatus(
                    "MICROPHONE PERMISSION DENIED"
                );

                addMessage(
                    "JARVIS",
                    "Microphone permission was denied. Allow microphone access for this website and try again.",
                    "ai"
                );

                break;


            case "audio-capture":

                setStatus(
                    "NO MICROPHONE FOUND"
                );

                addMessage(
                    "JARVIS",
                    "No microphone was detected by the browser.",
                    "ai"
                );

                break;


            case "no-speech":

                setStatus(
                    "NO SPEECH DETECTED"
                );

                break;


            case "network":

                setStatus(
                    "VOICE NETWORK ERROR"
                );

                addMessage(
                    "JARVIS",
                    "Speech recognition could not connect to the browser's recognition service.",
                    "ai"
                );

                break;


            case "language-not-supported":

                setStatus(
                    "LANGUAGE NOT SUPPORTED"
                );

                break;


            case "aborted":

                setStatus(
                    "VOICE STOPPED"
                );

                break;


            default:

                setStatus(
                    "VOICE ERROR: " +
                    event.error
                );
        }
    };


    // =================================================
    // END
    // =================================================

    recognition.onend = function () {

        isListening = false;

        if (micButton) {

            micButton.classList.remove(
                "listening"
            );

            micButton.textContent = "🎤";
        }

        if (
            status &&
            status.textContent ===
            "🎤 LISTENING..."
        ) {

            setStatus(
                "● ONLINE"
            );
        }
    };
}


// =====================================================
// MICROPHONE
// =====================================================

async function startListening() {

    if (!recognition) {

        addMessage(
            "JARVIS",
            "Speech recognition is not supported in this browser. Try Chrome or another supported browser.",
            "ai"
        );

        return;
    }


    if (isListening) {

        recognition.stop();

        return;
    }


    // Check secure context.
    // Render is HTTPS, so this should normally be true.

    if (!window.isSecureContext) {

        addMessage(
            "JARVIS",
            "Microphone requires a secure HTTPS connection.",
            "ai"
        );

        return;
    }


    // Ask for microphone permission first.

    if (
        navigator.mediaDevices &&
        navigator.mediaDevices.getUserMedia
    ) {

        try {

            const stream =
                await navigator.mediaDevices.getUserMedia({
                    audio: true
                });


            // We only needed permission.
            // SpeechRecognition will manage the microphone.

            stream.getTracks().forEach(
                function (track) {
                    track.stop();
                }
            );


        } catch (error) {

            console.error(
                "Microphone permission error:",
                error
            );

            setStatus(
                "MICROPHONE PERMISSION DENIED"
            );

            addMessage(
                "JARVIS",
                "Please allow microphone access in your browser settings.",
                "ai"
            );

            return;
        }
    }


    try {

        setStatus(
            "STARTING MICROPHONE..."
        );

        recognition.start();

    } catch (error) {

        console.error(
            "Recognition start error:",
            error
        );

        // Browser may throw InvalidStateError
        // if recognition is already running.

        if (
            error.name !==
            "InvalidStateError"
        ) {

            addMessage(
                "JARVIS",
                "Could not start speech recognition.",
                "ai"
            );

        }
    }
}


// =====================================================
// GLOBAL
// =====================================================

window.startListening =
    startListening;

window.speak =
    speak;
