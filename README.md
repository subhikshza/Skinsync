# SkinSync

> Indian students who are new to skincare actives buy several products and do not know which ones clash or how to space them across the week.
> Other tools explain ingredients or flag a clash; SkinSync builds the whole AM/PM week for you from products sold in India, and shows the source behind every rule.

Pick the products you own. SkinSync finds the conflicts between them (for example retinol + glycolic acid) and builds a 7-day morning and night routine that keeps the clashing ones apart. Every rule links to a dermatology or cosmetic-chemistry source.

**Not medical advice.** It is a planning aid based on general published guidance.

## What is in v1

- 30 products sold in India (25 from Indian brands), each with a source link
- 7 conflict rules and 4 timing rules, each with a source
- Beginner and regular levels (beginners get strong actives on fewer days)
- A reasons table: why each product is on the days it is on

## Stack

React + Vite · FastAPI + Pydantic · JSON data files · pytest

## Run it

```
# terminal 1: backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload        # API docs at http://localhost:8000/docs

# terminal 2: frontend
cd frontend
npm install
npm run dev                          # app at http://localhost:5173
```

Tests: `cd backend && pytest`

## Docs

- [`docs/PHASE1_RESEARCH.md`](docs/PHASE1_RESEARCH.md): competitors, rules table, sources
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md): design, algorithm, diagrams, API
- [`INTERVIEW_NOTES.md`](INTERVIEW_NOTES.md): decisions, trade-offs, key code, interview questions

## Next

A1: explain my routine in simple words (LLM). A2: scan a label photo. Later: Q&A over the sources.
