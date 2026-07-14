# AI Mock Interview Chatbot

A Streamlit web app that simulates a job interview using OpenAI's GPT-4o. The user provides their personal info, target role, and target company, then goes through a short AI-driven interview and receives a scored feedback report at the end.

## Features

- Candidate setup form (name, experience, skills, seniority level, position, company)
- Live chat-based interview powered by OpenAI (`gpt-4o`), limited to 5 exchanges
- Automated feedback and scoring (1–10) generated after the interview
- One-click restart

## Tech Stack

- Python
- [Streamlit](https://streamlit.io/) — UI framework
- [OpenAI API](https://platform.openai.com/) — chat completions (streaming)
- `streamlit-js-eval` — page reload on restart

## Project Structure

```
.
├── app.py                 # Main Streamlit application
├── requirements.txt        # Python dependencies
├── Exercises/              # Practice/example scripts
└── .streamlit/secrets.toml # Local secrets (OpenAI API key) - not committed
```

## Setup & Installation

1. Clone the repository and create a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Add your OpenAI API key to `.streamlit/secrets.toml`:
   ```toml
   OPENAI_API_KEY = "sk-..."
   ```
4. Run the app:
   ```bash
   streamlit run app.py
   ```

## Presentation Checklist

Everything you need to prepare before presenting this project.

### 1. Project Overview (slide/talking points)
- [ ] Problem statement: why an AI mock interview tool is useful (interview practice, instant feedback)
- [ ] Target users: job seekers preparing for interviews
- [ ] One-sentence pitch of the app

### 2. Architecture & Tech Explanation
- [ ] Explain the tech stack (Streamlit for UI, OpenAI API for the conversational logic)
- [ ] Walk through the app flow/state machine:
  1. Setup form → candidate info collected
  2. Interview stage → 5 user/assistant exchanges via streamed chat completions
  3. Feedback stage → transcript sent back to GPT-4o for scoring
  4. Restart
- [ ] Explain how `st.session_state` is used to manage app state across reruns

### 3. Live Demo Preparation
- [ ] Valid OpenAI API key configured in `.streamlit/secrets.toml`
- [ ] App tested end-to-end right before presenting (setup → interview → feedback → restart)
- [ ] Stable internet connection (API calls require it)
- [ ] Have a fallback: screen recording/screenshots in case the live demo or API fails
- [ ] Prepare sample answers in advance to keep the demo interview quick and smooth

### 4. Code Walkthrough
- [ ] Be ready to show/explain key snippets in `app.py`:
  - Session state initialization
  - The system prompt that configures the interviewer persona
  - The streaming chat completion call
  - The feedback-generation prompt and scoring format
- [ ] Mention current limitations (e.g., no persistence, exposed prompt engineering choices, fixed 5-question limit)

### 5. Q&A Prep
- [ ] Anticipate questions on cost (OpenAI API usage), scalability, and data privacy (API key handling, no storage of user data)
- [ ] Have ideas ready for future improvements (e.g., configurable question count, multiple interview types, saving history, authentication)

### 6. Logistics
- [ ] Slides or one-pager summarizing features and architecture
- [ ] Confirm screen-sharing/demo environment works before the presentation
- [ ] Time the demo to fit the presentation slot
