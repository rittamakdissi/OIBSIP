from click import command
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
from urllib.parse import quote_plus
import subprocess
import sys
from nltk.stem import PorterStemmer
from nltk.tokenize import wordpunct_tokenize

recognizer = sr.Recognizer()


stemmer = PorterStemmer()

# الترتيب بيحسم التعادل بالنقاط
INTENT_KEYWORDS = {
    "exit":     ["goodbye", "bye", "exit", "quit", "stop"],
    "reminder": ["remind", "reminder", "timer"],
    "search":   ["search", "google", "look", "find"],
    "time":     ["time", "clock"],
    "date":     ["date", "day", "today"],
    "greeting": ["hello", "hi", "hey", "morning", "afternoon", "evening"],
}

# نحوّل الكلمات المفتاحية لجذورها مرة وحدة
INTENT_STEMS = {
    intent: {stemmer.stem(word) for word in words}
    for intent, words in INTENT_KEYWORDS.items()
}


def parse_intent(command):
    """Score each intent using stemmed tokens and return the best one."""
    tokens = {stemmer.stem(token) for token in wordpunct_tokenize(command)}

    best_intent, best_score = "unknown", 0
    for intent, stems in INTENT_STEMS.items():
        score = len(tokens & stems)
        if score > best_score:
            best_intent, best_score = intent, score
    return best_intent


def speak(text):
    """Speak a response aloud using a separate process each time."""
    print("Assistant:", text)
    code = (
        "import pyttsx3, sys;"
        "e = pyttsx3.init();"
        "e.say(sys.argv[1]);"
        "e.runAndWait()"
    )
    try:
        subprocess.run([sys.executable, "-c", code, text])
    except Exception as e:
        print("TTS Error:", e)


def listen():
    """Listen to the microphone and convert speech to text."""
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(
                source, timeout=5, phrase_time_limit=8
            )

        command = recognizer.recognize_google(audio)
        print("You:", command)
        return command.lower().strip()

    except sr.WaitTimeoutError:
        speak("I did not hear anything. Please try again.")
    except sr.UnknownValueError:
        speak("Sorry, I did not understand. Please repeat.")
    except sr.RequestError:
        speak("Speech recognition is unavailable. Check your internet connection.")
    except OSError:
        speak("I could not access the microphone. Please check your settings.")

    return ""


def handle_command(command):
    """Identify the command and perform the requested action."""

    if not command:
        return True

    if command in ["hello", "hi"] or command.startswith(("hello ", "hi ")):
        speak("Hello! How can I help you?")

    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")

    elif "date" in command or "today" in command:
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {current_date}")

    elif "search for" in command or command.startswith("search "):
        topic = command.split("search", 1)[1]
        topic = topic.strip().removeprefix("for").strip()

        if topic:
            url = "https://www.google.com/search?q=" + quote_plus(topic)
            webbrowser.open(url)
            speak(f"Searching the web for {topic}")
        else:
            speak("Please tell me what you want to search for.")

    elif "goodbye" in command or "exit" in command or "stop" == command:
        speak("Goodbye!")
        return False

    else:
        speak("Sorry, I do not know that command yet. Please try again.")

    return True


def main():
    speak("Voice assistant started. Say hello to begin.")
    
    running = True
    while running:
        command = listen()
        running = handle_command(command)


if __name__ == "__main__":
    main()





