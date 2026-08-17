"use strict";

document.addEventListener("DOMContentLoaded", function () {

    const input = document.getElementById("question");
    const status = document.getElementById("status");
    const micButton = document.getElementById("mic");

    if (!input || !status || !micButton) {
        console.error("Jarvis speech UI elements not found.");
        return;
    }


    // =========================================================
    // BROWSER SPEECH RECOGNITION
    // =========================================================

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;


    if (!SpeechRecognition) {

        console.error(
            "SpeechRecognition is not supported in this browser."
        );

        micButton.disabled = true;
        micButton.textContent = "🚫";

        status.textContent =
            "VOICE NOT SUPPORTED";

        return;
    }


    const recognition =
        new SpeechRecognition();


    // =========================================================
    // SETTINGS
    // =========================================================

    recognition.lang = "en-IN";

    recognition.continuous = false;

    recognition.interimResults = false;

    recognition.maxAlternatives = 1;


    let listening = false;


    // =========================================================
    // START
    // =========================================================

    recognition.onstart = function () {

        listening = true;

        micButton.classList.add("listening");

        micButton.textContent = "🛑";

        status.textContent =
            "🎤 LISTENING...";

        console.log(
            "Jarvis microphone started."
        );
    };


    // =========================================================
    // RESULT
    // =========================================================

    recognition.onresult = function (event) {

        try {

            const result =
                event.results[0];

            if (!result) {
                return;
            }


            const transcript =
                result[0].transcript.trim();


            console.log(
                "Recognized:",
                transcript
            );


            if (!transcript) {

                status.textContent =
                    "NO SPEECH DETECTED";

                return;
            }


            // =================================================
            // SPEECH -> TEXT
            // =================================================

            input.value =
                transcript;


            status.textContent =
                "VOICE → TEXT";


            // =================================================
            // TEXT -> EXISTING JARVIS
            // =================================================

            /*
                askGemini() already exists inside app.py's
                HTML page.

                We call it after speech becomes text.
            */

            if (
                typeof window.askGemini ===
                "function"
            ) {

                setTimeout(
                    function () {

                        window.askGemini();

                    },
                    150
                );

            } else {

                console.error(
                    "askGemini() function not found."
                );

                status.textContent =
                    "JARVIS FUNCTION NOT FOUND";
            }


        } catch (error) {

            console.error(
                "Speech result error:",
                error
            );

            status.textContent =
                "VOICE PROCESSING ERROR";
        }
    };


    // =========================================================
    // ERROR
    // =========================================================

    recognition.onerror = function (event) {

        console.error(
            "Speech recognition error:",
            event.error
        );


        listening = false;

        micButton.classList.remove(
            "listening"
        );

        micButton.textContent =
            "🎤";


        switch (event.error) {

            case "not-allowed":

                status.textContent =
                    "MIC PERMISSION DENIED";

                break;


            case "no-speech":

                status.textContent =
                    "NO SPEECH DETECTED";

                break;


            case "audio-capture":

                status.textContent =
                    "MICROPHONE NOT FOUND";

                break;


            case "network":

                status.textContent =
                    "SPEECH NETWORK ERROR";

                break;


            case "service-not-allowed":

                status.textContent =
                    "SPEECH SERVICE BLOCKED";

                break;


            case "aborted":

                status.textContent =
                    "VOICE STOPPED";

                break;


            default:

                status.textContent =
                    "VOICE ERROR";
        }
    };


    // =========================================================
    // END
    // =========================================================

    recognition.onend = function () {

        listening = false;

        micButton.classList.remove(
            "listening"
        );

        micButton.textContent =
            "🎤";


        if (
            status.textContent ===
                "🎤 LISTENING..." ||
            status.textContent ===
                "VOICE → TEXT"
        ) {

            status.textContent =
                "● ONLINE";
        }
    };


    // =========================================================
    // MICROPHONE BUTTON
    // =========================================================

    function startListening() {

        if (listening) {

            try {

                recognition.stop();

            } catch (error) {

                console.error(
                    error
                );
            }

            return;
        }


        try {

            recognition.start();

        } catch (error) {

            /*
                Some browsers throw an error when
                start() is called twice very quickly.
            */

            console.error(
                "Speech start error:",
                error
            );
        }
    }


    // =========================================================
    // GLOBAL FUNCTION
    // =========================================================

    window.startListening =
        startListening;


    console.log(
        "Jarvis speech recognition ready."
    );

});
