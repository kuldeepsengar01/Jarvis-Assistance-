"use strict";

const input = document.getElementById("question");
const chat = document.getElementById("chat");
const status = document.getElementById("status");
const micButton = document.getElementById("mic");

let recognition = null;
let isListening = false;


// =====================================================
// ADD MESSAGE
// =====================================================

function addMessage(sender, text, type) {

    if (!chat) {
        return;
    }

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


// =====================================================
// STATUS
// =====================================================

function setStatus(text) {

    if (status) {
        status.textContent =
            text;
    }
}


// =====================================================
// SPEECH RECOGNITION
// =====================================================

const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;


if (SpeechRecognition) {

    recognition =
        new SpeechRecognition();


    recognition.lang =
        "en-IN";


    recognition.continuous =
        false;


    recognition.interimResults =
        false;


    recognition.maxAlternatives =
        1;


    recognition.onstart =
        function() {

            isListening =
                true;


            micButton.classList.add(
                "listening"
            );


            micButton.textContent =
                "🛑";


            setStatus(
                "🎤 LISTENING..."
            );
        };


    recognition.onresult =
        function(event) {

            const result =
                event.results[0];


            if (!result) {
                return;
            }


            const transcript =
                result[0].transcript.trim();


            console.log(
                "Speech:",
                transcript
            );


            if (!transcript) {

                setStatus(
                    "NO SPEECH DETECTED"
                );

                return;
            }


            input.value =
                transcript;


            setStatus(
                "VOICE RECEIVED"
            );


            if (
                typeof window.askGemini ===
                "function"
            ) {

                window.askGemini();
            }
        };


    recognition.onerror =
        function(event) {

            console.error(
                "Speech error:",
                event.error
            );


            isListening =
                false;


            micButton.classList.remove(
                "listening"
            );


            micButton.textContent =
                "🎤";


            switch (event.error) {

                case "not-allowed":

                    setStatus(
                        "MIC PERMISSION DENIED"
                    );

                    addMessage(
                        "JARVIS",
                        "Microphone permission denied. Allow microphone access for this website.",
                        "ai"
                    );

                    break;


                case "no-speech":

                    setStatus(
                        "NO SPEECH DETECTED"
                    );

                    break;


                case "audio-capture":

                    setStatus(
                        "NO MICROPHONE FOUND"
                    );

                    break;


                case "network":

                    setStatus(
                        "VOICE NETWORK ERROR"
                    );

                    addMessage(
                        "JARVIS",
                        "The browser speech service could not be reached.",
                        "ai"
                    );

                    break;


                default:

                    setStatus(
                        "VOICE ERROR: " +
                        event.error
                    );
            }
        };


    recognition.onend =
        function() {

            isListening =
                false;


            micButton.classList.remove(
                "listening"
            );


            micButton.textContent =
                "🎤";


            if (
                status.textContent ===
                "🎤 LISTENING..."
            ) {

                setStatus(
                    "● ONLINE"
                );
            }
        };


} else {

    console.error(
        "SpeechRecognition not supported."
    );


    micButton.disabled =
        true;


    micButton.textContent =
        "🚫";


    setStatus(
        "VOICE NOT SUPPORTED"
    );
}


// =====================================================
// START LISTENING
// =====================================================

async function startListening() {

    if (!recognition) {

        addMessage(
            "JARVIS",
            "Speech recognition is not supported in this browser. Use Chrome or Edge.",
            "ai"
        );

        return;
    }


    if (isListening) {

        recognition.stop();

        return;
    }


    if (
        !window.isSecureContext
    ) {

        addMessage(
            "JARVIS",
            "Microphone requires HTTPS.",
            "ai"
        );

        return;
    }


    /*
        Ask browser permission first.
        This also gives us a clear permission error.
    */

    if (
        navigator.mediaDevices &&
        navigator.mediaDevices.getUserMedia
    ) {

        try {

            const stream =
                await navigator.mediaDevices.getUserMedia({
                    audio: true
                });


            stream
                .getTracks()
                .forEach(
                    function(track) {
                        track.stop();
                    }
                );


        } catch (error) {

            console.error(
                "Microphone permission:",
                error
            );


            setStatus(
                "MIC PERMISSION DENIED"
            );


            addMessage(
                "JARVIS",
                "Please allow microphone permission in your browser.",
                "ai"
            );


            return;
        }
    }


    try {

        recognition.start();

    } catch (error) {

        console.error(
            "Recognition start error:",
            error
        );
    }
}


window.startListening =
    startListening;
