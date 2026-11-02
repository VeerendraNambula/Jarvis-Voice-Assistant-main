# Jarvis Voice Assistant

A Python desktop voice assistant that listens for the wake word **“Jarvis”**, recognizes spoken commands, opens common websites, reads top news headlines, plays configured music links, and optionally answers general questions with the OpenAI API.

## Features

- Speech recognition through SpeechRecognition and Google's recognition service.
- Text-to-speech through pyttsx3, with console output when speech synthesis is unavailable.
- Website shortcuts for Google, Facebook, X, and YouTube.
- News headlines through NewsAPI (India by default; configure `NEWS_COUNTRY` to change it).
- Optional AI responses through the OpenAI Chat Completions API.
- An editable music-link dictionary in `musiclibrary.py`.

## Requirements

- Python 3.10+
- A working microphone and speakers for voice interaction
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

Install the core dependencies:

```bash
pip install -r requirements.txt
```

For microphone input, install the optional audio dependency:

```bash
pip install -r requirements-audio.txt
```

On Debian/Ubuntu, PyAudio may require `sudo apt install portaudio19-dev`. On Windows, a compatible PyAudio wheel may be needed. Grant microphone access to your terminal or Python environment.

Copy `.env.example` to `.env` and add your own credentials:

```dotenv
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini
NEWS_API_KEY=your_news_api_key
NEWS_COUNTRY=in
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

## Run tests

```bash
pip install pytest
pytest -q
```

## Project structure

```text
Jarvis-Voice-Assistant/
├── main.py
├── musiclibrary.py
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── requirements-audio.txt
```

## Privacy and limitations

This is a learning project. Speech recognition sends audio to Google's recognition service, news requests go to NewsAPI, and AI prompts go to OpenAI when those features are enabled. Review those services' privacy terms before use. The assistant is intended for local desktop use and does not provide background service management.
