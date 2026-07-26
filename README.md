# Financial News Analyzer

Research global market instruments and source-linked financial coverage from one responsive web application.

**Live:** [financialnewsanalyzer.vercel.app](https://financialnewsanalyzer.vercel.app)

## Features

- Search equities, BIST instruments, ETFs, indices, commodities, currencies, futures, and crypto.
- Inspect latest prices, market cap, P/E ratios, 52-week range, volume, beta, sector, and exchange metadata.
- View split- and dividend-adjusted daily OHLCV history from five days to five years.
- Switch between line and candlestick charts.
- Compare up to eight companies, tickers, sectors, or market topics.
- Review explainable sentiment scores, confidence, matched keywords, categories, and coverage distributions.
- Filter and sort provider-linked articles without additional network requests.
- Check normal weekday schedules for fourteen global exchanges.

## Architecture

```text
.
├── api/index.py                         # FastAPI delivery layer for Vercel
├── index.html                           # Static application shell
├── app.js                               # Client-side search, analysis, and charts
├── styles.css                           # Responsive Color Hunt-based design system
├── financial_news_analyzer/
│   ├── src/
│   │   ├── domain/                      # Entities and deterministic policies
│   │   ├── application/                 # Use cases and outbound ports
│   │   ├── infrastructure/              # Yahoo Finance and schedule adapters
│   │   └── bootstrap.py                 # Composition root
│   └── tests/                           # Unit and architecture tests
├── requirements.txt
└── vercel.json
```

Dependencies point inward: domain code has no framework dependency, application code owns provider contracts, and infrastructure implements those contracts.

## Local development

Requirements:

- Python 3.12
- Node.js with `npx`

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
npx vercel dev
```

Open `http://localhost:3000`.

## Tests

```bash
python -m unittest discover -s financial_news_analyzer/tests -v
python -m compileall -q api financial_news_analyzer
node --check app.js
```

## API

- `GET /api/search?q=ASML`
- `GET /api/market?symbols=AAPL,MSFT,NVDA`
- `GET /api/profile/ASELS.IS`
- `GET /api/history/BTC-USD?days=365`
- `GET /api/news?companies=Apple,NVIDIA&limit=8`
- `GET /api/schedules`
- `GET /api/docs`

Responses are cached briefly in each warm function instance. The browser also caches completed research requests and cancels stale discovery searches.

## Data notice

Market values and article metadata are retrieved through `yfinance` and may be delayed, incomplete, or temporarily unavailable. Historical charts use adjusted OHLC data. Exchange schedules cover normal weekdays only; holidays and early closes are not modeled.

This project is for research and education, not investment advice. Review original sources and obtain an appropriately licensed provider before commercial use.

## License

[MIT](LICENSE)
