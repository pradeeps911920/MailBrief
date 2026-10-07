# 📬 MailBrief Product Architecture
### One brief. Every important email.

**MailBrief** is an AI-powered personal email intelligence system designed to solve a simple but common problem: **important emails are often buried inside a large volume of routine emails.**

Students and professionals can receive dozens of emails every day—college announcements, internship opportunities, placement updates, event invitations, forms, deadlines, newsletters, notifications, and promotional messages. Reading every email individually is time-consuming, and important information can easily be missed.

MailBrief acts as an intelligent layer between the user's inbox and the user. It processes incoming emails, filters sensitive information, understands the relevant messages, summarizes them, identifies important actions and deadlines, and presents the result as one concise and actionable briefing.

> **Instead of searching through your inbox to find what matters, MailBrief brings what matters to you.**

---

## 🎯 The Core Problem

Email overload is not simply a problem of receiving too many messages. The bigger problem is that **important information is mixed together with unimportant information**.

For example, a student may receive 30 emails in a day, but only a few may actually require attention:

- An internship application deadline.
- A placement registration notice.
- A course registration deadline.
- An important college announcement.
- An event that requires registration.

Without an intelligent filtering and summarization layer, the user has to manually open, read, understand, and prioritize every message.

MailBrief is designed to reduce this effort.

---

## 💡 The Core Concept

The central idea of MailBrief is:

```text
Inbox
  ↓
Fetch Emails
  ↓
Understand Content
  ↓
Filter Sensitive Information
  ↓
Analyze Importance
  ↓
Extract Actions & Deadlines
  ↓
Prioritize
  ↓
Generate One Actionable Brief
```

MailBrief is designed to answer four important questions:

1. **What happened today?**
2. **What is important?**
3. **What do I need to do?**
4. **What am I likely to miss?**

The ultimate goal is:

> **Turn a crowded inbox into one clear, actionable brief.**

---

## 🧠 Product Philosophy

MailBrief combines **AI-based understanding** with **deterministic rules**.

AI is useful for understanding unstructured email content, but the system should not depend entirely on an AI model for critical prioritization.

Therefore, MailBrief separates the process into two layers:

### AI Intelligence

Gemini is responsible for understanding email content and extracting structured information such as:

- Category
- Summary
- Importance
- Required action
- Deadline
- Relevant entities
- Why the email matters

### Deterministic Safety Layer

A rule-based prioritization layer provides a predictable safety net.

For example:

- An email with an explicit deadline can be elevated in priority.
- An email requiring user action can be highlighted.
- Time-sensitive information can be surfaced even if the AI classification varies.

This combination allows MailBrief to use AI for understanding while retaining deterministic behavior for important decisions.

---

## 🔐 Privacy-First Architecture

Not every email should be sent to an AI model.

MailBrief therefore places a privacy filter **before AI processing**.

Emails containing sensitive information such as:

- OTPs
- Banking alerts
- Password-related messages
- Security notifications
- Other sensitive transactional information

can be identified and filtered before they reach Gemini.

The privacy-first pipeline is:

```text
Gmail
  ↓
Email Fetcher
  ↓
Privacy Filter
  ↓
Relevant Emails
  ↓
Gemini Analysis
  ↓
Structured Information
  ↓
Prioritization
  ↓
SQLite
  ↓
MailBrief Dashboard
```

This architecture minimizes unnecessary exposure of sensitive inbox content to the AI layer.

---

## 🛠️ Current MVP Implementation

The current MVP is a functional end-to-end application that demonstrates the complete email-intelligence workflow.

| Component | Implementation |
|---|---|
| Frontend | HTML + Tailwind CSS + Vanilla JavaScript |
| Backend | FastAPI |
| Database | SQLite via SQLAlchemy |
| Gmail | Gmail API + Google OAuth 2.0 |
| AI | Gemini API via Google GenAI SDK |
| AI Model | Gemini 3.5 Flash-Lite |
| Scope | Single Gmail account |
| Processing | Manual brief generation |

---

## ⚙️ Key Features of the MVP

### 1. Manual Brief Generation

The user explicitly triggers email processing by clicking **Process New Emails**.

This keeps the current MVP simple and avoids unnecessary background processing.

---

### 2. Privacy Filter

A layered filtering system uses keyword and pattern-based rules to identify sensitive emails such as OTPs, banking alerts, and security-related messages **before AI processing**.

---

### 3. Full Email Body Parsing

MailBrief does not rely only on email snippets.

It extracts readable content from complex multipart MIME emails so that the AI receives meaningful email content for analysis.

---

### 4. AI-Powered Email Analysis

Gemini converts unstructured emails into structured information.

The current analysis includes:

```text
Category
Importance
Summary
Action Required
Action
Deadline
Entities
Why Important
```

---

### 5. Strict Structured Output

Gemini responses are validated using **Pydantic schemas**.

This ensures that the AI response follows the expected structure instead of returning unpredictable free-form text.

---

### 6. Action & Deadline Extraction

MailBrief identifies whether an email requires the user to do something and extracts explicitly stated deadlines.

For example:

```text
Email:
"Internship applications must be submitted by November 1, 2026."

MailBrief:
Category: Internships
Importance: High
Action Required: Yes
Deadline: November 1, 2026
```

---

### 7. Rule-Based Prioritization

The prioritization layer acts as a safety net around AI classification.

For example, an email containing a clear upcoming deadline and requiring action can automatically receive higher priority.

---

### 8. Processed Email Storage

SQLite stores the state of processed emails.

This prevents MailBrief from repeatedly analyzing the same messages and reduces unnecessary AI API usage.

---

### 9. Actionable Dashboard

The frontend presents processed emails through an easy-to-understand dashboard with views such as:

- All
- Important
- Actions
- Deadlines

This allows users to quickly focus on the information that requires attention.

---

## 🔄 End-to-End Workflow

A typical MailBrief workflow is:

```text
1. User connects Gmail
            ↓
2. MailBrief fetches new emails
            ↓
3. Privacy filter removes sensitive emails
            ↓
4. Relevant email content is parsed
            ↓
5. Gemini analyzes the email
            ↓
6. Structured response is validated
            ↓
7. Rule-based prioritization is applied
            ↓
8. Result is stored in SQLite
            ↓
9. Dashboard displays the actionable brief
```

---

## 📊 Example Use Case

Suppose a student receives 30 emails in one day.

Most are routine messages, advertisements, notifications, or low-priority updates.

Among them, three emails contain genuinely important information:

```text
1. Internship application deadline
2. Placement registration form
3. Important academic announcement
```

Instead of reading all 30 emails manually, MailBrief processes them and surfaces the important information.

The user can therefore move from:

```text
30 emails
↓
Open and read individually
↓
Understand
↓
Remember deadlines
↓
Decide what matters
```

to:

```text
30 emails
↓
MailBrief processes them
↓
Important information identified
↓
One concise dashboard
↓
User focuses on what matters
```

---

## 🚀 Future Roadmap

### Phase 2 — Automation & Scale

#### Scheduler
Use **APScheduler** to automatically generate a daily briefing, for example every night, without requiring the user to manually press **Process New Emails**.

#### PostgreSQL Migration
Move from SQLite to PostgreSQL for better concurrency, scalability, and multi-user support.

#### Multiple Gmail Accounts
Allow users to connect multiple Gmail accounts and combine relevant messages into one unified briefing.

#### Weekly Briefs
Generate weekly summaries showing important events, actions completed, pending tasks, and upcoming deadlines.

---

### Phase 3 — Advanced Intelligence

#### Outlook Support
Integrate Microsoft Graph API to support Outlook and Microsoft email accounts.

#### Deadline Calendar
Provide a visual calendar containing extracted deadlines and important dates.

#### Smart Search
Allow users to ask natural-language questions over their processed email knowledge.

Example:

```text
"What placement deadlines are coming this week?"
```

#### Personal Priority Learning
Allow MailBrief to learn the user's explicit preferences over time.

For example, the system could learn that:

```text
Internship emails → High priority
Promotional emails → Low priority
College deadlines → High priority
Routine notifications → Low priority
```

---

## 🎯 Long-Term Vision

The long-term goal of MailBrief is **not to replace email**.

It is to create an intelligent layer on top of the inbox that helps users understand what matters without manually inspecting every message.

The vision is:

> **You receive the emails. MailBrief tells you what matters.**

Ultimately, MailBrief aims to transform email from a constantly growing list of messages into a **clear, prioritized stream of information, actions, and deadlines**.

---

## ✅ Current MVP Status

The current MVP successfully demonstrates:

- ✅ Gmail OAuth authentication
- ✅ Gmail email fetching
- ✅ Privacy filtering
- ✅ Full email body parsing
- ✅ Gemini AI analysis
- ✅ Structured AI output validation
- ✅ Email categorization
- ✅ Importance detection
- ✅ Action detection
- ✅ Deadline extraction
- ✅ Rule-based prioritization
- ✅ SQLite storage
- ✅ Actionable dashboard
- ✅ Manual processing of new emails

---

## 📌 Summary

**MailBrief is an AI-powered email intelligence system that helps users avoid missing important information buried inside a crowded inbox.**

It fetches emails, filters sensitive content, understands relevant messages using Gemini, generates concise summaries, identifies important actions and deadlines, prioritizes what needs attention, and presents the result in one simple dashboard.

> **One brief. Every important email.**