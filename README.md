# Dxora Test - Automated Multi-Platform Posting System

A FastAPI application that automatically publishes a short message across multiple third-party platforms through their APIs.

## Endpoint (port 4000)

| Endpoint | Method | Description |
|---|---|---|
| `POST /posting` | POST | Post a message to multiple third-party platforms independently |
| `GET /docs` | GET | Interactive Swagger UI |
| `GET /` | GET | Service info |

## Project structure

```
dxora-test/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app + /posting endpoint
│   ├── config.py        # Pydantic Settings (.env)
│   ├── schemas.py       # Pydantic request/response models
│   ├── services/
│   │   ├── __init__.py
│   │   └── posting_service.py   # Platform registry + fan-out posting
│   └── platforms/
│       ├── __init__.py
│       ├── base.py
│       ├── twitter.py
│       ├── linkedin.py
│       ├── facebook.py
│       ├── instagram.py
│       ├── reddit.py
│       ├── telegram.py
│       ├── devto.py
│       └── medium.py
├── .env.example
├── requirements.txt
└── README.md
```

## Setup

```bash
# 1. Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env and add credentials for the platforms you want to use

# 4. Run the server
uvicorn app.main:app --host 0.0.0.0 --port 4000
```

Open http://localhost:4000/docs for the interactive API docs.

## Example request

```http
POST http://localhost:4000/posting
Content-Type: application/json

{
  "message": "Check out our latest business platform and grow your online visibility. https://example.com"
}
```

## Example response

```json
{
  "success": true,
  "results": [
    {
      "platform": "Twitter (X)",
      "status": "failed",
      "posted_url": null,
      "public_access": false,
      "date": "2026-11-16",
      "time": "11:30:00",
      "error": "TWITTER_BEARER_TOKEN not configured"
    },
    {
      "platform": "LinkedIn",
      "status": "failed",
      "posted_url": null,
      "public_access": false,
      "date": "2026-11-16",
      "time": "11:30:00",
      "error": "LINKEDIN_ACCESS_TOKEN not configured"
    },
    {
      "platform": "Telegram",
      "status": "failed",
      "posted_url": null,
      "public_access": false,
      "date": "2026-11-16",
      "time": "11:30:00",
      "error": "TELEGRAM_BOT_TOKEN not configured"
    }
  ]
}
```

Platforms integrated (8): Twitter (X), LinkedIn, Facebook, Instagram, Reddit, Telegram, Dev.to, Medium. Each platform posts independently — one failure does not block the others.

## Input validation

- Message must not exceed 200 characters.
- Exactly one CTA link (URL) must be included in the message.
- The URL must be valid.
- Invalid input returns a 422 validation error.

## Configuration (`.env.example`)

Platform credentials are read from environment variables via `app/config.py`. Unconfigured platforms return a `failed` status with a clear error message instead of crashing the request.

## Error handling

- Platform credentials missing → that platform reports `status: "failed"` with an error message; other platforms still post.
- Network/API errors per platform are caught individually and reported in that platform's result.

## Submission notes

- No API keys or secrets are committed. Use `.env` (gitignored) for credentials.
- Follow Dxora Technologies on LinkedIn and CREST on Instagram as part of application verification.
- Share your LinkedIn and Instagram profile links when submitting.
- Email: hr@chivoxai.com — Subject: `Your Name - Python Practical test review`
