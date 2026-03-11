# PDF Chat

A Streamlit web app that lets you upload a PDF and ask questions about its content using the Claude API.

## How it works

1. Upload a PDF file via the file uploader
2. Type questions in the chat input
3. Claude reads the file content and answers your questions

## Setup

**Prerequisites:** Python 3.11+, an [Anthropic API key](https://console.anthropic.com/)

```bash
# Clone the repo
git clone <your-repo-url>
cd pdf-chat

# Create and activate a virtual environment
python3.11 -m venv py311env
source py311env/bin/activate  # On Windows: py311env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set your API key
export ANTHROPIC_API_KEY=your_api_key_here
# Or create a .env file (see .env.example)
```

## Running the app

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

## Environment variables

| Variable | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Your Anthropic API key (required) |

Copy `.env.example` to `.env` and fill in your key, or export it directly in your shell.

## Tech stack

- [Streamlit](https://streamlit.io/) — UI framework
- [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python) — Claude API client
- Model: `claude-opus-4-6`
