import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
from datetime import datetime

# ---------- Gemini Setup ----------
with open("api_key.txt", "r") as file:
    api_key = file.read().strip()

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

# ---------- TTS Setup ----------
engine = pyttsx3.init()

# ---------- Speech Recognition ----------
recognizer = sr.Recognizer()


def speak(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)

        print("You said:", text)

        return text

    except Exception:
        print("Sorry, couldn't understand.")

        return None


def save_log(user_msg, bot_msg):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("conversation_log.txt", "a", encoding="utf-8") as file:

        file.write(f"\n[{timestamp}]\n")
        file.write(f"User: {user_msg}\n")
        file.write(f"Bot: {bot_msg}\n")
        file.write("-" * 40 + "\n")


print("=" * 50)
print("VOICE AI CHATBOT")
print("=" * 50)

while True:

    print("\nChoose Input Method")
    print("1. Type Message")
    print("2. Voice Message")
    print("3. Exit")

    choice = input("\nEnter choice: ")

    if choice == "3":
        print("Goodbye!")
        speak("Goodbye")
        break

    elif choice == "1":

        user_input = input("\nYou: ")

    elif choice == "2":

        user_input = listen()

        if user_input is None:
            continue

    else:
        print("Invalid choice")
        continue

    try:

        response = model.generate_content(user_input)

        bot_reply = response.text

        print("\nBot:", bot_reply)

        speak(bot_reply)

        save_log(user_input, bot_reply)

    except Exception as e:

        print("Error:", e)