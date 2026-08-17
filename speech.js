"use strict";

(function () {

    const input =
        document.getElementById("question");

    const status =
        document.getElementById("status");

    const micButton =
        document.getElementById("mic");


    if (!input || !status || !micButton) {

        console.error(
            "Speech UI elements not found."
        );

        return;
    }


    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;


    if (!SpeechRecognition) {

        micButton.disabled =
            true;

        micButton.textContent =
            "🚫";

        status.textContent =
            "VOICE NOT SUPPORTED";

        console.warn(
            "SpeechRecognition is not supported."
        );

        return;
    }


    const recognition =
        new SpeechRecognition();


    recognition.lang =
        "en-IN";


    recognition.continuous =
        false;


    recognition.interimResults =
        false;


    recognition.maxAlternatives =
        1;


    let listening =
        false;


    recognition.onstart =
        function () {

            listening =
                true;


            micButton.classList.add(
                "listening"
            );


            micButton.textContent =
                "🛑";


            status.textContent =
                "🎤 LISTENING...";
        };


    recognition.onresult =
        function (event) {

            const result =
                event.results[0];


            if (!result) {

                status.textContent =
                    "NO SPEECH";

                return;
            }


            const transcript =
                result[0]
                    .transcript
                    .trim();


            console.log(
                "Recognized text:",
                transcript
            );


            if (!transcript) {

                status.textContent =
                    "NO SPEECH DETECTED";

                return;
            }


            // =========================================
            // SPEECH -> TEXT
            // =========================================

            input.value =
                transcript;


            status.textContent =
                "VOICE → TEXT";


            // =========================================
            // TEXT -> EXISTING JARVIS
            // =========================================

            setTimeout(
                function () {

                    if (
                        typeof window.askGemini ===
                        "function"
                    ) {

                        window.askGemini();

                    } else {

                        console.error(
                            "askGemini function not found."
                        );
                    }

                },
                150
            );
        };


    recognition.onerror =
        function (event) {

            console.error(
                "Speech recognition error:",
                event.error
            );


            listening =
                false;


            micButton.classList.remove(
                "listening"
            );


            micButton.textContent =
                "🎤";


            if (
                event.error ===
                "not-allowed"
            ) {

                status.textContent =
                    "MIC PERMISSION DENIED";

            } else if (
                event.error ===
                "no-speech"
            ) {

                status.textContent =
                    "NO SPEECH DETECTED";

            } else if (
                event.error ===
                "audio-capture"
            ) {

                status.textContent =
                    "MICROPHONE NOT FOUND";

            } else if (
                event.error ===
                "network"
            ) {

                status.textContent =
                    "SPEECH SERVICE NETWORK ERROR";

            } else {

                status.textContent =
                    "VOICE ERROR: " +
                    event.error;
            }
        };


    recognition.onend =
        function () {

            listening =
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

                status.textContent =
                    "● ONLINE";
            }
        };


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

            console.error(
                "Speech start error:",
                error
            );
        }
    }


    window.startListening =
        startListening;


})();
