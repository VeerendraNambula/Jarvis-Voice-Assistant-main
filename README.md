# Jarvis Voice Assistant

A Python desktop voice assistant that listens for the wake word **“Jarvis”**, recognizes spoken commands, opens common websites, reads top news headlines, plays entries from a configurable music library, and can answer general questions with the OpenAI API.

## Features

- Speech input with SpeechRecognition and Google Speech Recognition.
- Text-to-speech responses with pyttsx3.
- Website shortcuts for Google, Facebook, X, and YouTube.
- News headlines through NewsAPI.
- Optional AI responses through the OpenAI Chat Completions API.
- A small editable music-link dictionary in `musiclibrary.py`.

## Requirements

- Python 3.10+
- A working microphone and speakers
- PyAudio-compatible audio input for your operating system
- Optional OpenAI and NewsAPI keys

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv

# Windows
.venv\\Scripts\\activate

# macOS / Linux
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

On Windows, installing PyAudio may require a compatible wheel or audio build tools. Microphone access must also be enabled for your terminal or Python environment.

Copy `.env.example` to `.env` and add your own API keys:

```dotenv
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini
NEWS_API_KEY=your_news_api_key
```

Keep `.env` private. Never commit API keys.

## Run

```bash
python main.py
```

Say “Jarvis” to activate the command listener. Example commands:

- “Open Google”
- “Open YouTube”
- “Open X”
- “News”
- “Play Skyfall” (after adding a matching key in `musiclibrary.py`)
- “What is machine learning?”
- “Exit”

AI responses require `OPENAI_API_KEY`; news requires `NEWS_API_KEY`. Website shortcuts and configured music links work without those keys.

## Project structure

```text
Jarvis-Voice-Assistant/
├── main.py
├── musiclibrary.py
├── .env.example
├── .gitignore
└── requirements.txt
```

## Notes

This is a learning project. Speech recognition sends audio to Google's recognition service, and news/AI requests use their respective external APIs. Review the privacy terms of services you enable.
