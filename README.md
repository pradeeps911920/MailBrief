# ðŸ“¬ MailBrief
### One brief. Every important email.

**MailBrief** is an AI-powered personal email intelligence system that turns a user's inbox into a concise, actionable briefingâ€”showing what matters, what requires action, and what deadlines are approaching, while keeping sensitive emails away from the AI model.

---

## âœ¨ Features

- **Privacy-First:** Automatically intercepts and filters out sensitive emails (OTPs, bank alerts, passwords) before they reach the AI model.
- **AI Summarization:** Uses Google Gemini to read unstructured emails and convert them into structured information such as category, summary, and importance.
- **Action & Deadline Extraction:** Highlights tasks that require user action and identifies clearly stated upcoming deadlines.
- **Prioritization Engine:** A rule-based safety net that helps ensure important deadlines and actions are properly prioritized.
- **Local Storage:** Uses SQLite to remember processed emails and avoid unnecessary repeated AI processing.
- **Gmail Integration:** Connects securely to Gmail using Google OAuth 2.0.
- **Simple Dashboard:** Presents processed emails in categories such as General, Internships, Important, Actions, and Deadlines.

---

## ðŸ—ï¸ Architecture

```text
                 â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                 â”‚    Gmail     â”‚
                 â””â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜
                        â”‚ OAuth
                        â–¼
                â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                â”‚ Email Fetcher â”‚
                â””â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜
                        â–¼
                â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                â”‚ Privacy Guard â”‚
                â””â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜
                        â–¼
                â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                â”‚ Gemini / LLM  â”‚
                â””â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜
                        â–¼
                â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                â”‚    SQLite     â”‚
                â””â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜
                        â–¼
                â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                â”‚ Daily Brief   â”‚
                â””â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜
                        â–¼
                â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                â”‚   Dashboard   â”‚
                â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

**Tech Stack:**

- **Frontend:** Vanilla HTML/JS + Tailwind CSS (served directly by the backend).
- **Backend:** FastAPI (Python).
- **AI:** Google GenAI Python SDK with Gemini 3.5 Flash-Lite.
- **Database:** SQLite & SQLAlchemy.
- **Authentication:** Google OAuth 2.0.

---

## ðŸš€ Quickstart Setup

### 1. Google Cloud Setup (Required)

MailBrief requires a Google Cloud project to access Gmail.

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create or select a Google Cloud project (for example, `MailBrief`).
3. Go to **APIs & Services â†’ Library** and enable the **Gmail API**.
4. Go to **Google Auth Platform â†’ Audience**.
5. Set the publishing status to **Testing** for development.
6. Add your Gmail address under **Test users**.
7. Go to **Google Auth Platform â†’ Clients**.
8. Create an **OAuth 2.0 Client ID**.
9. Select **Web application**.
10. Set the **Authorized redirect URI** to:

```text
http://localhost:8000/auth/callback
```

11. Download the OAuth client JSON file.
12. Rename it exactly to:

```text
credentials.json
```

13. Place `credentials.json` inside the `backend/` folder.

> During development, only Google accounts added as test users can authorize the application.

---

### 2. Gemini Setup

MailBrief uses the Google Gemini API for email analysis.

1. Go to [Google AI Studio](https://aistudio.google.com/).
2. Open **API Keys**.
3. Create a new Gemini API key.
4. Keep the key private and do not upload it to GitHub.

The current MailBrief configuration uses:

```text
gemini-3.5-flash-lite
```

---

### 3. Backend Setup

Open **PowerShell** in the `backend/` folder.

```powershell
cd backend/
```

#### First-time setup

Create the virtual environment:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\activate
```

If PowerShell blocks the activation script, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

and then activate again:

```powershell
.\venv\Scripts\activate
```

Install the dependencies:

```powershell
pip install -r requirements.txt
```

Create the environment file:

```powershell
copy ..\.env.example .\.env
```

Open `backend/.env` and add your Gemini API key:

```text
LLM_API_KEY=your_gemini_api_key
```

> The virtual environment and dependencies only need to be created/installed during initial setup or when the dependencies change.

---

### 4. Run the Application

For normal future runs, open PowerShell in the `backend/` folder and use:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\activate
python -m uvicorn main:app --reload
```

You should see:

```text
Uvicorn running on http://127.0.0.1:8000
Application startup complete.
```

Open the application in your browser:

```text
http://localhost:8000
```

or:

```text
http://127.0.0.1:8000
```

---

### 5. Connect Gmail

When the MailBrief dashboard opens:

1. Click **Connect Gmail**.
2. Sign in with a Google account that has been added as a test user.
3. Review and allow the requested Gmail permissions.
4. After successful authentication, you will be redirected back to the MailBrief dashboard.

The Gmail credentials are stored locally for development so you do not need to repeat the OAuth process every time you start the application.

---

### 6. Process New Emails

After Gmail is connected:

1. Click **Process New Emails**.
2. MailBrief fetches newly processed emails from Gmail.
3. Sensitive emails are filtered according to the privacy rules.
4. The remaining emails are analyzed using Gemini.
5. MailBrief extracts:
   - Category
   - Summary
   - Importance
   - Required action
   - Deadline
   - Important entities
   - Reason for importance
6. The results are stored in SQLite and displayed on the dashboard.

---

## ðŸ”„ Normal Startup Workflow

Once MailBrief has been set up already, you **do not need to repeat the entire installation process**.

Every time you want to run the project:

```powershell
cd "C:\path\to\MailBrief\backend"
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\activate
python -m uvicorn main:app --reload
```

Then open:

```text
http://localhost:8000
```

You do **not** need to:

- create the virtual environment again
- reinstall dependencies every time
- create a new Gemini API key
- create new Google OAuth credentials
- repeat Gmail authorization every time

Those are initial setup steps.

---

## ðŸ” Security Notes

Never commit the following files to GitHub:

```text
.env
credentials.json
token.json
*.db
```

These files may contain API keys, OAuth credentials, access tokens, or local database data.

Make sure they are included in `.gitignore`.

---

## ðŸ“‚ Project Structure

```text
MailBrief/
â”‚
â”œâ”€â”€ README.md                  # Project documentation
â”œâ”€â”€ idea.md                    # Project concept and roadmap
â”œâ”€â”€ .env.example               # Environment variable template
â”œâ”€â”€ .gitignore
â”‚
â”œâ”€â”€ frontend/
â”‚   â””â”€â”€ index.html             # Web Dashboard UI
â”‚
â””â”€â”€ backend/
    â”œâ”€â”€ main.py                # FastAPI API entry point
    â”œâ”€â”€ requirements.txt       # Python dependencies
    â”œâ”€â”€ .env                   # Local environment variables
    â”œâ”€â”€ credentials.json       # Google OAuth client credentials
    â”œâ”€â”€ token.json             # Generated Gmail OAuth token
    â”œâ”€â”€ mailbrief.db           # Local SQLite database
    â”‚
    â”œâ”€â”€ auth/                  # Google OAuth flow
    â”œâ”€â”€ mail/                  # Email fetching, parsing and privacy filtering
    â”œâ”€â”€ ai/                    # Gemini integration and Pydantic schemas
    â”œâ”€â”€ database/              # SQLite database models and operations
    â”œâ”€â”€ briefing/              # Briefing generation and prioritization
    â””â”€â”€ scheduler/             # Scheduled processing functionality
```

---

## ðŸ§  AI Analysis

MailBrief uses Gemini to convert unstructured email content into structured information.

For example, an email such as:

> "The deadline to submit internship applications is November 1, 2026."

can be converted into:

```json
{
  "category": "Internships",
  "importance": "high",
  "summary": "Internship applications must be submitted by November 1, 2026.",
  "action_required": true,
  "deadline": "2026-11-01"
}
```

This makes large volumes of emails easier to understand and act upon.

---

## ðŸ“Š Dashboard

The MailBrief dashboard provides:

- Total processed emails
- Important emails
- Required actions
- Upcoming deadlines
- Category-based organization
- Email summaries
- Deadline badges
- Action-required indicators
- Importance indicators

---

## ðŸ§ª Development Notes

MailBrief is currently designed as an MVP and runs locally using FastAPI and SQLite.

The project can later be extended with:

- Multiple Gmail accounts
- Scheduled daily email processing
- Cloud deployment
- PostgreSQL
- Background task queues
- Email notifications
- Better filtering and personalization
- Production OAuth configuration
- More advanced email categorization

---

## ðŸ“ Current Status

MailBrief MVP currently supports:

- âœ… Gmail OAuth authentication
- âœ… Gmail email fetching
- âœ… Email privacy filtering
- âœ… Gemini AI analysis
- âœ… Email categorization
- âœ… Importance detection
- âœ… Action extraction
- âœ… Deadline extraction
- âœ… SQLite storage
- âœ… Rule-based prioritization
- âœ… Web dashboard
- âœ… Local development workflow

---

## ðŸ“¸ Screenshots

Add screenshots here showing:

1. MailBrief dashboard
2. Google OAuth authentication
3. Connected Gmail account
4. Processed email
5. AI-generated analysis
6. Deadline and action indicators

---

## ðŸ“„ License

This project is currently intended for educational and personal development purposes.
