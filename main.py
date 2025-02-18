import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
import sys
import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(r"C:\Users\BQ562TS\Desktop\Jarvis-Voice-Assistant-main\.env")  # Use relative path
openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure the .env has the key correctly set
newsapi = os.getenv("NEWS_API_KEY")  # Load the News API key

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def aiprocess(command):
    try:
        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            prompt=f"You are a helpful virtual assistant. The user asked: {command}",
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except openai.error.OpenAIError as e:
        print(f"OpenAI API Error: {e}")
        speak("Sorry, there was an issue processing your request.")
    except Exception as e:
        print(f"Error: {e}")
        speak("Sorry, I couldn't process your request.")

def processcommand(c):
    print(f"Received command: {c}")  # Debugging line

    if "open google" in c.lower():
        try:
            webbrowser.open("https://www.google.co.in/")
        except Exception as e:
            print(f"Error opening Google: {e}")
            speak("Sorry, I couldn't open Google.")
    elif "open facebook" in c.lower():
        try:
            webbrowser.open("https://www.facebook.com/")
        except Exception as e:
            print(f"Error opening Facebook: {e}")
            speak("Sorry, I couldn't open Facebook.")
    elif "open twitter" in c.lower():
        try:
            webbrowser.open("https://x.com/home")
        except Exception as e:
            print(f"Error opening Twitter: {e}")
            speak("Sorry, I couldn't open Twitter.")
    elif "open youtube" in c.lower():
        try:
            webbrowser.open("https://www.youtube.com/")
        except Exception as e:
            print(f"Error opening YouTube: {e}")
            speak("Sorry, I couldn't open YouTube.")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musiclibrary.music.get(song)
        if link:
            try:
                webbrowser.open(link)
            except Exception as e:
                print(f"Error playing song {song}: {e}")
                speak(f"Sorry, I couldn't play {song}.")
        else:
            speak(f"Sorry, I couldn't find the song {song}.")
    elif "news" in c.lower():
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
            if r.status_code == 200:
                data = r.json()
                articles = data.get('articles', [])
                for article in articles:
                    speak(article['title'])
        except Exception as e:
            print(f"Error fetching news: {e}")
            speak("Sorry, I couldn't fetch the news.")
    elif "exit" in c.lower():
        speak("Shutting down. Goodbye!")
        sys.exit()
    else:
        output = aiprocess(c)
        speak(output)

if __name__ == "__main__":
    speak("Initializing Jarvis...")

    while True:
        r = recognizer
        print("Listening for wake word...")

        try:
            with sr.Microphone() as source:
                print("Listening...")
                # Adjust for ambient noise for a shorter duration or skip adjustment
                r.adjust_for_ambient_noise(source, duration=0.1)  # Shortened duration for quicker response
                audio = r.listen(source, timeout=5, phrase_time_limit=5)  # Shortened timeout
            word = r.recognize_google(audio)
            print(f"Recognized: {word}")

            if "jarvis" in word.lower():
                speak("Yes, how can I assist you?")
                with sr.Microphone() as source:
                    print("Listening for command...")
                    audio = r.listen(source, timeout=5, phrase_time_limit=5)  # Shortened timeout
                    command = r.recognize_google(audio)
                    print(f"Command: {command}")
                    processcommand(command)

        except sr.UnknownValueError:
            print("Sorry, I couldn't understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"Error: {e}")