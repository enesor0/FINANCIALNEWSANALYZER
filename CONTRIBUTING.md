# Contributing

## Setup

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
npx vercel dev
```

## Before opening a pull request

```bash
python -m unittest discover -s financial_news_analyzer/tests -v
python -m compileall -q api financial_news_analyzer
node --check app.js
```

Keep domain rules framework-free, define external capabilities as application-owned ports, and implement provider-specific behavior in infrastructure adapters. Do not add simulated market or news data to production paths.

Use focused commits and update tests and documentation with behavioral changes.
