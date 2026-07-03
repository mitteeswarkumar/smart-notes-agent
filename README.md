# 📄 Smart Notes Agent

A simple AI-powered agent that reads your PDF, summarizes it, answers questions
about it, and explains difficult topics in plain English — built with Python,
Streamlit, and Google's Gemini API.

## Features

1. Upload a PDF file
2. Extract text from the PDF
3. Generate a short summary
4. Ask questions about the PDF content
5. Get simple explanations of difficult topics

## Project Structure

```
smart_notes_agent/
│
├── app.py              # Main Streamlit app (run this file)
├── pdf_reader.py        # Extracts text from uploaded PDFs
├── gemini_helper.py      # Talks to the Gemini API (summary, Q&A, explanations)
├── requirements.txt      # List of Python packages needed
├── .env                 # Your secret Gemini API key (keep this private!)
└── README.md            # This file
```

## Setup Instructions

### 1. Get a free Gemini API key

- Go to https://aistudio.google.com/app/apikey
- Sign in with a Google account
- Click "Create API Key" and copy it

### 2. Add your key to the `.env` file

Open `.env` in this folder and replace the placeholder with your real key:

```
GEMINI_API_KEY=your_actual_api_key_here
```

Do NOT share this file or upload it to GitHub — it's your private key.

### 3. Install the required packages

Open a terminal in this folder and run:

```
pip install -r requirements.txt
```

This installs Streamlit, the Gemini library, PyPDF2, and python-dotenv.

### 4. Run the app

```
streamlit run app.py
```

This will open the app automatically in your web browser
(usually at http://localhost:8501).

## How to Use

1. Click "Upload your PDF file" and choose a PDF from your computer.
2. Click "Summarize PDF" to get a short summary.
3. Type a question in the text box and click "Get Answer" to ask
   about the PDF's content.
4. Type a confusing topic/term and click "Explain Simply" to get
   a beginner-friendly explanation.

## Common Errors & Fixes

| Error | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError` | Packages not installed | Run `pip install -r requirements.txt` |
| `PermissionDenied` / `Unauthenticated` | Wrong or missing API key | Check your `.env` file has the correct key |
| Empty extracted text | PDF is scanned images, not real text | Try a different, text-based PDF |
| `429 Resource Exhausted` | Hit the free API rate limit | Wait a bit before trying again |
| App doesn't open in browser | Streamlit didn't launch correctly | Check the terminal for the local URL and open it manually |

## Tech Stack

- **Python** — core programming language
- **Streamlit** — simple web UI framework
- **Google Gemini API** — the AI model powering summaries, Q&A, and explanations
- **PyPDF2** — extracts text from PDF files

## Notes

- This is a beginner-friendly project with no advanced frameworks
  (no LangChain, no databases, no multi-agent systems) — just plain
  Python functions calling an AI API.
- The whole PDF's text is sent to Gemini in each request. For very
  large PDFs, you may hit input size limits — this project is designed
  for short-to-medium length documents (like notes, articles, or
  short reports).
