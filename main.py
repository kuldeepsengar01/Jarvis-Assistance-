import os
import datetime
import webbrowser

from dotenv import load_dotenv
from google import genai


# =====================================================
# ENV
# =====================================================

load_dotenv()

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)


if not GEMINI_API_KEY:

    print(
        "GEMINI_API_KEY is not configured."
    )

    raise SystemExit


client =
    genai.Client(
        api_key=GEMINI_API_KEY
    )


# =====================================================
# SPEAK
# =====================================================

def speak(text):

    print()
    print("JARVIS:")
    print(text)
    print()


# =====================================================
# GEMINI
# =====================================================

def ask_gemini(question):

    try:

        response =
            client.models.generate_content(
                model="gemini-3.6-flash",
                contents=question
            )


        return (
            response.text
            or "No response received."
        )


    except Exception as error:

        print(
            "Gemini error:",
            error
        )

        return (
            "Sorry, Gemini request failed."
        )


# =====================================================
# COMMAND
# =====================================================

def process_command(command):

    text =
        command.strip()

    lower =
        text.lower()


    if lower in [
        "exit",
        "quit",
        "bye",
        "stop"
    ]:

        return "__EXIT__"


    if (
        lower == "time"
        or "what time" in lower
    ):

        current_time =
            datetime.datetime.now()

        return (
            "The time is "
            +
            current_time.strftime(
                "%I:%M %p"
            )
        )


    if (
        "open youtube"
        in lower
    ):

        webbrowser.open(
            "https://youtube.com"
        )

        return (
            "Opening YouTube."
        )


    if (
        "open google"
        in lower
    ):

        webbrowser.open(
            "https://google.com"
        )

        return (
            "Opening Google."
        )


    if lower.startswith(
        "search "
    ):

        query =
            text[7:].strip()

        webbrowser.open(
            "https://www.google.com/search?q="
            +
            query.replace(
                " ",
                "+"
            )
        )

        return (
            "Searching Google for "
            +
            query
        )


    return ask_gemini(
        text
    )


# =====================================================
# MAIN
# =====================================================

def main():

    speak(
        "Hello Kuldeep. I am Jarvis."
    )

    speak(
        "Type your command."
    )


    while True:

        try:

            command =
                input(
                    "You: "
                ).strip()


            if not command:

                continue


            response =
                process_command(
                    command
                )


            if response ==
                "__EXIT__":

                speak(
                    "Goodbye Kuldeep."
                )

                break


            speak(
                response
            )


        except KeyboardInterrupt:

            print()

            speak(
                "Goodbye Kuldeep."
            )

            break


        except Exception as error:

            print(
                "Error:",
                error
            )


if __name__ == "__main__":

    main()
