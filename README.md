# ✍️ AI Content Studio

> Generate professional blog posts, LinkedIn captions, and cold emails instantly using AI — powered by LLaMA 3 via Groq API.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35.0-FF4B4B?style=flat-square&logo=streamlit)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3-orange?style=flat-square)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat-square&logo=docker)
![Status](https://img.shields.io/badge/Status-In_Progress-yellow?style=flat-square)

---

## What It Does

AI Content Studio is a Streamlit web app that generates professional, ready-to-use content in seconds. Enter a topic, pick a content type, and get polished output instantly.

| Content Type | What You Get |
|---|---|
| Blog Post | 400–500 word structured article with headings |
| LinkedIn Caption | Hook-driven post with hashtags and engagement question |
| Cold Email | Subject line, value proposition, clear CTA |

---

## Demo

```
Topic: "The future of AI in hiring"
Content Type: LinkedIn Caption

→ Generates a professional LinkedIn post in under 3 seconds
→ Copy to clipboard or download as .txt
→ All generations saved in session history
```

---

## Tech Stack

| Layer | Tool | Why |
|---|---|---|
| LLM | Groq API (LLaMA 3.3 70B) | Free tier, fastest inference available |
| UI | Streamlit | Rapid prototyping, clean Python-native UI |
| Prompts | Custom prompt templates | Structured output per content type |
| Config | python-dotenv | Secure API key management |
| Deploy | Docker | Consistent, portable containerized deployment |

---

## Project Structure

```
AI Content Studio/
├── prompts/
│   ├── __init__.py
│   └── templates.py        # Prompt templates for each content type
├── utils/
│   ├── __init__.py
│   └── generator.py        # Groq API call + error handling
├── .env.example            # Environment variable template
├── .gitignore
├── config.py               # Centralised app settings
├── Dockerfile              # Container definition
├── requirements.txt
├── streamlit_app.py        # Main Streamlit UI
└── README.md
```

---

## Getting Started

### Option 1 — Run with Docker (recommended)

```bash
# Pull and run in one command
docker run -p 8501:8501 --env GROQ_API_KEY=your_key_here yourname/ai-content-studio
```

Then open `http://localhost:8501` in your browser.

### Option 2 — Run locally

**1. Clone the repo**
```bash
git clone https://github.com/Shirin0511/AI-Content-Studio.git
cd AI-Content-Studio
```

**2. Create and activate virtual environment**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up your API key**
```bash
cp .env.example .env
# Open .env and add your Groq API key
# Get a free key at console.groq.com
```

**5. Run the app**
```bash
streamlit run streamlit_app.py
```

---

## Environment Variables

Create a `.env` file at the root (never commit this):

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your free Groq API key at [console.groq.com](https://console.groq.com)

---

## Features

- **3 content types** — Blog Post, LinkedIn Caption, Cold Email
- **Instant generation** — LLaMA 3.3 70B via Groq, results in ~2–3 seconds
- **Copy to clipboard** — one-click copy on every result
- **Download as .txt** — save any generated content locally
- **Generation history** — all results saved in session, expandable
- **Clear history** — reset with one click
- **Error handling** — graceful messages for rate limits, API errors, empty responses
- **Dockerized** — run anywhere with a single command

---

## How It Works

```
User enters topic + selects content type
            ↓
Prompt template fills in the topic
            ↓
Groq API sends prompt to LLaMA 3.3 70B
            ↓
LLM returns structured professional content
            ↓
Streamlit renders it with copy + download options
            ↓
Result saved to session history
```

---

## Roadmap

- [ ] Add ad copy as a content type
- [ ] Tone selector (professional / casual / persuasive)
- [ ] Export history as PDF
- [ ] Deploy to Streamlit Cloud with public URL
- [ ] Add usage analytics

---

## License

MIT License — free to use, modify, and distribute.

---

<p align="center">Built with Python, Streamlit, and Groq API &nbsp;•&nbsp; <a href="https://console.groq.com">Get your free Groq API key</a></p>
