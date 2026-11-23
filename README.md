# GrammarLens

A grammar and spelling checker built for an NLP course project. Paste any English text and it marks spelling, grammar and style problems, with a one-click fix for each.

Live demo: https://grammarlens-red.vercel.app/

## Features

- Spelling check with pyspellchecker plus a list of common misspellings
- 18 grammar rule groups: a / an by sound, subject-verb agreement, confused words (their / there, its / it's), verb forms, double negatives, punctuation and spacing, and more
- Style hints: filler words, wordy phrases, cliches, passive voice
- Flesch readability score
- Highlighted preview, Fix all, Copy text, history and analytics
- Sign in and sign up screens (browser-only demo)

## How it works

The engine (`engine.py`) is rule based. It uses regular expressions and a dictionary lookup, so every result can be explained. `main.py` exposes it through FastAPI, and `public/index.html` is the front end.

## Evaluation

I wrote 55 test sentences and measured precision, recall and F1 with `test_engine.py`. All three scored 1.00. The test sentences were written for the rules themselves, so this score is optimistic. A fair test would use an outside dataset such as JFLEG or CoNLL-2014.

## Limitations

- Rules match patterns and do not understand context, so a real word used wrongly (form instead of from) is not caught.
- Login is stored in the browser only. A real login needs a database.

## Run locally

    python -m venv venv
    venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    uvicorn main:app --reload

Then open http://127.0.0.1:8000

## Tech stack

Python, FastAPI, pyspellchecker, HTML, CSS, JavaScript. Deployed on Vercel.