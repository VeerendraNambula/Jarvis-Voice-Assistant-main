import os
import sys
import webbrowser

import pyttsx3
import requests
import speech_recognition as sr
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

import musiclibrary

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

ai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
recognizer = sr.Recognizer()
speech_engine = pyttsx3.init()


def speak(text: str) -> None:
    speech_engine.say(text)
    speech_engine.runAndWait()


def ai_process(command: str) -> str:
    if ai_client is None:
        return "AI responses are unavailable. Add your OpenAI API key to the local environment file."

    try:
        response = ai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a concise, helpful desktop voice assistant.",
                },
                {"role": "user", "content": command},
            ],
            temperature=0.7,
            max_tokens=150,
        )
        return response.choices[0].message.content or "I couldn't generate a response."
    except OpenAIError as error:
        print(f"OpenAI API error: {error}")
        return "Sorry, there was an issue processing your request."


def process_command(command: str) -> None:
    normalized = command.lower().strip()
    print(f"Received command: {command}")

    if "open google" in normalized:
        webbrowser.open("https://www.google.com/")
    elif "open facebook" in normalized:
        webbrowser.open("https://www.facebook.com/")
    elif "open twitter" in normalized or "open x" in normalized:
        webbrowser.open("https://x.com/home")
    elif "open youtube" in normalized:
        webbrowser.open("https://www.youtube.com/")
    elif normalized.startswith("play"):
        parts = normalized.split(maxsplit=1)
        song = parts[1] if len(parts) > 1 else ""
        link = musiclibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak("Please specify a song from your music library.")
    elif "news" in normalized:
        if not NEWS_API_KEY:
            speak("News is unavailable. Add a News API key to your local environment file.")
            return

        try:
            response = requests.get(
                "https://newsapi.org/v2/top-headlines",
                params={"country": "us", "apiKey": NEWS_API_KEY},
                timeout=10,
            )
            response.raise_for_status()
            articles = response.json().get("articles", [])
            if not articles:
                speak("There are no headlines available right now.")
                return
            for article in articles[:5]:
                title = article.get("title")
                if title:
                    speak(title)
        except requests.RequestException as error:
            print(f"News API error: {error}")
            speak("Sorry, I couldn't fetch the news.")
    elif "exit" in normalized or "quit" in normalized:
        speak("Shutting down. Goodbye!")
        raise SystemExit(0)
    else:
        speak(ai_process(command))


def main() -> None:
    speak("Initializing Jarvis.")

    while True:
        print("Listening for wake word...")
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.3)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

            phrase = recognizer.recognize_google(audio)
            print(f"Recognized: {phrase}")

            if "jarvis" not in phrase.lower():
                continue

            speak("Yes, how can I assist you?")
            with sr.Microphone() as source:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            command = recognizer.recognize_google(audio)
            process_command(command)

        except sr.UnknownValueError:
            print("Sorry, I couldn't understand the audio.")
        except sr.RequestError as error:
            print(f"Speech recognition request failed: {error}")
        except sr.WaitTimeoutError:
            print("No speech detected before timeout.")
        except SystemExit:
            break
        except Exception as error:
            print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()
