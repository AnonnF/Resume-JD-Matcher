# AI Resume–Job Matcher

A beginner-friendly Streamlit app that compares your resume (PDF) against a job description and produces a structured Markdown matching report using the [DeepSeek API](https://api-docs.deepseek.com/).

## Features

- Upload a PDF resume and paste a job description
- Extract text from the PDF in memory (no files saved to disk)
- Generate a 9-section report: match score, requirement mapping, gaps, bullet rewrites, ATS keywords, tailored profile, and action plan
- Download the report as Markdown

## Prerequisites

- Python 3.10 or newer
- A [DeepSeek API key](https://platform.deepseek.com/api_keys)

## Setup

### 1. Clone or open the project

```bash
cd /path/to/Resume-JD-Matching
```

### 2. Create a virtual environment

**Windows (PowerShell / CMD):**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux (WSL):**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

Copy the example env file and add your key:

**Windows:**

```bash
copy .env.example .env
```

**macOS / Linux:**

```bash
cp .env.example .env
```

Edit `.env` and set:

```env
DEEPSEEK_API_KEY=your_actual_key_here
```

Never commit `.env` — it is listed in `.gitignore`.

## Run the app

```bash
streamlit run app.py
```

Open the URL shown in the terminal (usually http://localhost:8501).

## Usage

1. Upload your resume as a **PDF** (text-based PDFs work best; scanned/image-only PDFs may fail).
2. Paste the full **job description** into the text area.
3. Click **Analyze** and wait for the report (this calls the DeepSeek API and may take a minute).
4. Optionally **Download report (.md)** to save the result.

## Project structure

| File | Role |
|------|------|
| `app.py` | Streamlit UI and workflow orchestration |
| `parser.py` | PDF → plain text via `pypdf` |
| `prompts.py` | System prompt and user message template |
| `llm_client.py` | DeepSeek chat API (OpenAI-compatible SDK) |
| `requirements.txt` | Python dependencies |
| `.env.example` | Template for API key (copy to `.env`) |

## Model configuration

By default the app uses `deepseek-v4-pro` via `https://api.deepseek.com`. You can change the model in `llm_client.py` (e.g. to `deepseek-v4-flash` for faster, lower-cost responses). See the [DeepSeek API docs](https://api-docs.deepseek.com/) for details.

## Troubleshooting

| Problem | What to try |
|---------|-------------|
| API key warning in sidebar | Ensure `.env` exists with `DEEPSEEK_API_KEY=...` (not the placeholder `your_api_key_here`) |
| Invalid API key | Verify the key at [DeepSeek Platform](https://platform.deepseek.com/) |
| Could not extract text from PDF | Use a text-based PDF, not a scan; re-export from Word/Google Docs as PDF |
| Rate limit exceeded | Wait a few minutes and retry |
| Empty or cut-off report | Increase `max_tokens` in `llm_client.py` if the job description is very long |

## Security

- Keep your API key in `.env` only
- Do not commit `.env` or share keys in chat or screenshots
