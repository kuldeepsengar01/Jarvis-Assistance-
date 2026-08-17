import os
import datetime

from dotenv import load_dotenv
from google import genai


load_dotenv()

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)


if not GEMINI_API_KEY:

    print(
        "GEMINI_API_KEY is missing."
    )

    raise SystemExit(1)


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def speak(text):

    print()
    print("JARVIS:")
    print(text)
    print()


def ask_gemini(question):

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=question
        )

        return response.text or "No response received."

    except Exception as error:

        print(
            "Gemini error:",
            error
        )

        return (
            "Gemini is currently unavailable."
        )


def process_command(command):

    text = command.strip()

    lower = text.lower()


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

        now = datetime.datetime.now()

        return (
            "The time is "
            +
            now.strftime("%I:%M %p")
        )


    return ask_gemini(
        text
    )


def main():

    speak(
        "Hello Kuldeep. Jarvis is online."
    )


    while True:

        try:

            command =
                input("You: ").strip()


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


if __name__ == "__main__":

    main()
