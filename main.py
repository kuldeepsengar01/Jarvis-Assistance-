import os
import threading
import datetime
import webbrowser

from dotenv import load_dotenv
from google import genai

import speech_recognition as sr
import pyttsx3

from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput


# ============================================================
# ANDROID DETECTION
# ============================================================

ANDROID = False

try:
    from android.permissions import request_permissions, Permission
    from jnius import autoclass
    ANDROID = True

except ImportError:
    pass


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    print("Gemini API Key loaded successfully.")
    gemini = genai.Client(
        api_key=GEMINI_API_KEY
    )
else:
    print("WARNING: GEMINI_API_KEY is not set.")
    gemini = None


# ============================================================
# TEXT TO SPEECH
# ============================================================

try:
    engine = pyttsx3.init()
    engine.setProperty("rate", 170)

except Exception:
    engine = None


def speak(text):

    print("Jarvis:", text)

    if engine:

        try:
            engine.say(text)
            engine.runAndWait()

        except Exception as e:
            print("TTS Error:", e)


# ============================================================
# ANDROID PERMISSIONS
# ============================================================

def request_android_permissions():

    if not ANDROID:
        return

    try:

        permissions = [
            Permission.RECORD_AUDIO,
            Permission.READ_CONTACTS,
            Permission.CALL_PHONE
        ]

        request_permissions(
            permissions
        )

        print(
            "Android permissions requested."
        )

    except Exception as e:

        print(
            "Permission error:",
            e
        )


# ============================================================
# OPEN ANDROID APP
# ============================================================

def open_android_app(package_name):

    if not ANDROID:
        return False

    try:

        PythonActivity = autoclass(
            "org.kivy.android.PythonActivity"
        )

        activity = PythonActivity.mActivity

        package_manager = (
            activity.getPackageManager()
        )

        intent = package_manager.getLaunchIntentForPackage(
            package_name
        )

        if intent:

            activity.startActivity(
                intent
            )

            return True

    except Exception as e:

        print(
            "Open app error:",
            e
        )

    return False


# ============================================================
# OPEN URL
# ============================================================

def open_url(url):

    try:

        webbrowser.open(url)

        return True

    except Exception:

        return False


# ============================================================
# OPEN YOUTUBE
# ============================================================

def open_youtube():

    if ANDROID:

        if open_android_app(
            "com.google.android.youtube"
        ):

            return "Opening YouTube."

    open_url(
        "https://youtube.com"
    )

    return "Opening YouTube."


# ============================================================
# OPEN WHATSAPP
# ============================================================

def open_whatsapp():

    if ANDROID:

        if open_android_app(
            "com.whatsapp"
        ):

            return "Opening WhatsApp."

    open_url(
        "https://web.whatsapp.com"
    )

    return "Opening WhatsApp Web."


# ============================================================
# OPEN SNAPCHAT
# ============================================================

def open_snapchat():

    if ANDROID:

        if open_android_app(
            "com.snapchat.android"
        ):

            return "Opening Snapchat."

    open_url(
        "https://www.snapchat.com"
    )

    return "Opening Snapchat."


# ============================================================
# CONTACTS
# ============================================================

def get_contacts():

    if not ANDROID:
        return []

    try:

        PythonActivity = autoclass(
            "org.kivy.android.PythonActivity"
        )

        ContactsContract = autoclass(
            "android.provider.ContactsContract$CommonDataKinds$Phone"
        )

        activity = PythonActivity.mActivity

        resolver = (
            activity.getContentResolver()
        )

        cursor = resolver.query(
            ContactsContract.CONTENT_URI,
            None,
            None,
            None,
            None
        )

        contacts = []

        if cursor:

            name_index = cursor.getColumnIndex(
                ContactsContract.DISPLAY_NAME
            )

            number_index = cursor.getColumnIndex(
                ContactsContract.NUMBER
            )

            while cursor.moveToNext():

                name = cursor.getString(
                    name_index
                )

                number = cursor.getString(
                    number_index
                )

                if name and number:

                    contacts.append(
                        (
                            name,
                            number
                        )
                    )

            cursor.close()

        return contacts

    except Exception as e:

        print(
            "Contacts error:",
            e
        )

        return []


# ============================================================
# CALL CONTACT
# ============================================================

def call_contact(name):

    contacts = get_contacts()

    if not contacts:

        return (
            False,
            "I cannot access your contacts."
        )


    name = name.lower().strip()


    for contact_name, number in contacts:

        if name in contact_name.lower():

            if make_call(number):

                return (
                    True,
                    f"Calling {contact_name}."
                )


    return (
        False,
        f"I could not find {name}."
    )


# ============================================================
# MAKE CALL
# ============================================================

def make_call(number):

    if not ANDROID:

        return False

    try:

        PythonActivity = autoclass(
            "org.kivy.android.PythonActivity"
        )

        Intent = autoclass(
            "android.content.Intent"
        )

        Uri = autoclass(
            "android.net.Uri"
        )

        activity = PythonActivity.mActivity

        intent = Intent(
            Intent.ACTION_CALL
        )

        intent.setData(
            Uri.parse(
                "tel:" + number
            )
        )

        activity.startActivity(
            intent
        )

        return True

    except Exception as e:

        print(
            "Call error:",
            e
        )

        return False


# ============================================================
# CONTACT LIST
# ============================================================

def contact_list():

    contacts = get_contacts()

    if not contacts:

        return (
            "I could not access your contacts."
        )


    names = []

    for name, number in contacts:

        names.append(
            name
        )


    names = names[:40]

    return (
        "Your contacts are:\n\n"
        + "\n".join(names)
    )


# ============================================================
# WIKIPEDIA
# ============================================================

def wikipedia_search(query):

    try:

        import wikipedia

        result = wikipedia.summary(
            query,
            sentences=3
        )

        return result

    except Exception as e:

        print(
            "Wikipedia error:",
            e
        )

        return (
            "I could not find that topic on Wikipedia."
        )


# ============================================================
# GOOGLE SEARCH
# ============================================================

def google_search(query):

    url = (
        "https://www.google.com/search?q="
        + query.replace(
            " ",
            "+"
        )
    )

    open_url(url)

    return (
        f"Searching Google for {query}."
    )


# ============================================================
# GEMINI
# ============================================================

def ask_gemini(question):

    if not gemini:

        return (
            "Gemini API key is not configured."
        )


    try:

        response = gemini.models.generate_content(
            model="gemini-3.6-flash",
            contents=question
        )

        return response.text

    except Exception as e:

        print(
            "Gemini Error:",
            e
        )

        return (
            "Sorry, Gemini could not answer right now."
        )


# ============================================================
# VOICE INPUT
# ============================================================

def listen():

    recognizer = sr.Recognizer()

    try:

        with sr.Microphone() as source:

            print(
                "Listening..."
            )

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            audio = recognizer.listen(
                source,
                timeout=6,
                phrase_time_limit=10
            )

        print(
            "Recognizing..."
        )

        text = recognizer.recognize_google(
            audio
        )

        print(
            "You:",
            text
        )

        return text

    except Exception as e:

        print(
            "Voice Error:",
            e
        )

        return ""


# ============================================================
# COMMAND PROCESSOR
# ============================================================

def process_command(text):

    command = text.lower().strip()


    # -------------------------
    # EXIT
    # -------------------------

    if command in [
        "exit",
        "quit",
        "stop jarvis",
        "goodbye"
    ]:

        return "__EXIT__"


    # -------------------------
    # TIME
    # -------------------------

    if (
        "what time" in command
        or command == "time"
    ):

        current_time = datetime.datetime.now()

        return (
            "The time is "
            + current_time.strftime(
                "%I:%M %p"
            )
        )


    # -------------------------
    # YOUTUBE
    # -------------------------

    if (
        "open youtube" in command
        or "youtube kholo" in command
    ):

        return open_youtube()


    # -------------------------
    # WHATSAPP
    # -------------------------

    if (
        "open whatsapp" in command
        or "whatsapp kholo" in command
    ):

        return open_whatsapp()


    # -------------------------
    # SNAPCHAT
    # -------------------------

    if (
        "open snapchat" in command
        or "snapchat kholo" in command
    ):

        return open_snapchat()


    # -------------------------
    # GOOGLE
    # -------------------------

    if (
        command == "open google"
        or "google kholo" in command
    ):

        open_url(
            "https://google.com"
        )

        return "Opening Google."


    # -------------------------
    # SEARCH
    # -------------------------

    if command.startswith(
        "search "
    ):

        query = text[7:].strip()

        return google_search(
            query
        )


    # -------------------------
    # WIKIPEDIA
    # -------------------------

    if command.startswith(
        "wikipedia "
    ):

        query = text[10:].strip()

        return wikipedia_search(
            query
        )


    # -------------------------
    # SHOW CONTACTS
    # -------------------------

    if (
        "show contacts" in command
        or "show my contacts" in command
        or "contact list" in command
        or "contacts dikhao" in command
    ):

        return contact_list()


    # -------------------------
    # CALL
    # -------------------------

    if command.startswith(
        "call "
    ):

        name = text[5:].strip()

        success, message = call_contact(
            name
        )

        return message


    # -------------------------
    # SETTINGS
    # -------------------------

    if (
        "open settings" in command
        and ANDROID
    ):

        try:

            PythonActivity = autoclass(
                "org.kivy.android.PythonActivity"
            )

            Intent = autoclass(
                "android.content.Intent"
            )

            Settings = autoclass(
                "android.provider.Settings"
            )

            activity = (
                PythonActivity.mActivity
            )

            intent = Intent(
                Settings.ACTION_SETTINGS
            )

            activity.startActivity(
                intent
            )

            return (
                "Opening Android settings."
            )

        except Exception:

            return (
                "Could not open settings."
            )


    # -------------------------
    # GEMINI
    # -------------------------

    return ask_gemini(
        text
    )


# ============================================================
# UI
# ============================================================

class JarvisUI(BoxLayout):

    def __init__(
        self,
        **kwargs
    ):

        super().__init__(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10),
            **kwargs
        )


        # HEADER
        header = Label(
            text="◉  J A R V I S",
            font_size=dp(27),
            bold=True,
            color=(
                0.2,
                0.8,
                1,
                1
            ),
            size_hint_y=None,
            height=dp(60)
        )

        self.add_widget(
            header
        )


        # STATUS
        self.status = Label(
            text="● SYSTEM ONLINE",
            font_size=dp(12),
            color=(
                0.2,
                1,
                0.5,
                1
            ),
            size_hint_y=None,
            height=dp(30)
        )

        self.add_widget(
            self.status
        )


        # CHAT
        self.scroll = ScrollView()

        self.chat = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            size_hint_y=None
        )

        self.chat.bind(
            minimum_height=
            self.chat.setter(
                "height"
            )
        )

        self.scroll.add_widget(
            self.chat
        )

        self.add_widget(
            self.scroll
        )


        # QUICK ACTIONS
        actions = GridLayout(
            cols=3,
            spacing=dp(7),
            size_hint_y=None,
            height=dp(120)
        )


        buttons = [
            (
                "▶ YouTube",
                "open youtube"
            ),
            (
                "💬 WhatsApp",
                "open whatsapp"
            ),
            (
                "👻 Snapchat",
                "open snapchat"
            ),
            (
                "👥 Contacts",
                "show contacts"
            ),
            (
                "📚 Wikipedia",
                "wikipedia "
            ),
            (
                "🌐 Search",
                "search "
            )
        ]


        for title, command in buttons:

            button = Button(
                text=title,
                background_color=(
                    0.04,
                    0.12,
                    0.20,
                    1
                )
            )

            button.bind(
                on_press=
                lambda btn,
                cmd=command:
                self.quick_command(cmd)
            )

            actions.add_widget(
                button
            )


        self.add_widget(
            actions
        )


        # INPUT
        bottom = BoxLayout(
            spacing=dp(7),
            size_hint_y=None,
            height=dp(58)
        )


        self.input = TextInput(
            hint_text="Ask Jarvis...",
            multiline=False,
            font_size=dp(16)
        )

        self.input.bind(
            on_text_validate=
            self.send_message
        )


        mic = Button(
            text="🎤",
            size_hint_x=None,
            width=dp(65)
        )

        mic.bind(
            on_press=self.voice_command
        )


        send = Button(
            text="SEND",
            size_hint_x=None,
            width=dp(70)
        )

        send.bind(
            on_press=self.send_message
        )


        bottom.add_widget(
            self.input
        )

        bottom.add_widget(
            mic
        )

        bottom.add_widget(
            send
        )


        self.add_widget(
            bottom
        )


        # WELCOME
        self.add_message(
            "JARVIS",
            "Hello Kuldeep. Systems online. How can I help?"
        )


        # ANDROID PERMISSIONS
        Clock.schedule_once(
            lambda dt:
            request_android_permissions(),
            1
        )


    # ========================================================
    # ADD MESSAGE
    # ========================================================

    def add_message(
        self,
        sender,
        message
    ):

        label = Label(
            text=(
                sender
                + "\n"
                + message
            ),
            size_hint_y=None,
            font_size=dp(14),
            halign="left",
            valign="top"
        )


        label.bind(
            width=lambda obj, width:
            setattr(
                obj,
                "text_size",
                (
                    width - dp(10),
                    None
                )
            )
        )


        label.texture_update()

        label.height = (
            label.texture_size[1]
            + dp(15)
        )


        self.chat.add_widget(
            label
        )


        Clock.schedule_once(
            lambda dt:
            setattr(
                self.scroll,
                "scroll_y",
                0
            ),
            0.1
        )


    # ========================================================
    # QUICK COMMAND
    # ========================================================

    def quick_command(
        self,
        command
    ):

        if command.endswith(" "):

            self.input.text = command

            self.input.focus = True

            return


        self.execute(
            command
        )


    # ========================================================
    # SEND MESSAGE
    # ========================================================

    def send_message(
        self,
        *args
    ):

        text = (
            self.input.text
            .strip()
        )

        if not text:
            return


        self.input.text = ""

        self.execute(
            text
        )


    # ========================================================
    # EXECUTE
    # ========================================================

    def execute(
        self,
        text
    ):

        self.add_message(
            "YOU",
            text
        )

        self.status.text = (
            "● JARVIS IS THINKING..."
        )


        threading.Thread(
            target=self.process,
            args=(text,),
            daemon=True
        ).start()


    # ========================================================
    # PROCESS
    # ========================================================

    def process(
        self,
        text
    ):

        response = process_command(
            text
        )


        Clock.schedule_once(
            lambda dt:
            self.show_response(
                response
            )
        )


    # ========================================================
    # RESPONSE
    # ========================================================

    def show_response(
        self,
        response
    ):

        if response == "__EXIT__":

            speak(
                "Goodbye Kuldeep."
            )

            App.get_running_app().stop()

            return


        self.add_message(
            "JARVIS",
            response
        )


        self.status.text = (
            "● SYSTEM ONLINE"
        )


        threading.Thread(
            target=speak,
            args=(response,),
            daemon=True
        ).start()


    # ========================================================
    # VOICE
    # ========================================================

    def voice_command(
        self,
        *args
    ):

        self.status.text = (
            "● LISTENING..."
        )


        threading.Thread(
            target=self.voice_worker,
            daemon=True
        ).start()


    def voice_worker(
        self
    ):

        text = listen()


        if text:

            Clock.schedule_once(
                lambda dt:
                self.execute(text)
            )

        else:

            Clock.schedule_once(
                lambda dt:
                setattr(
                    self.status,
                    "text",
                    "● SYSTEM ONLINE"
                )
            )


# ============================================================
# APP
# ============================================================

class JarvisApp(App):

    def build(self):

        self.title = (
            "JARVIS AI"
        )

        return JarvisUI()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    JarvisApp().run()