# Andorra Bot 🤖

Telegram bot that integrates Interactive Brokers live data, Claude AI, and market data to monitor and analyze a passive investment portfolio.

Built as a personal finance tool following Boglehead investment principles.

## Features

- `/portfolio` — Real-time account summary from Interactive Brokers (net liquidation, cash, unrealized P&L)
- `/performance` — Normalized % return chart vs MSCI World benchmark (IWDA) over the last 6 months
- `/projection` — Compound interest projection with configurable initial capital, monthly contributions, annual return, and time horizon
- `/ask` — Free-form financial questions answered by Claude AI with Boglehead context

## Architecture
andorra-bot/

├── main.py              # Entry point

├── src/

│   ├── bot.py           # Telegram handlers

│   ├── ibkr.py          # Interactive Brokers connection (ib_async)

│   ├── claude.py        # Anthropic API integration

│   ├── performance.py   # Chart generation (yfinance + matplotlib)

│   └── projection.py    # Compound interest calculations

├── config/

│   └── settings.py      # Environment configuration

└── .env                 # API keys (not committed)
## Tech Stack

| Tool | Purpose |
|---|---|
| `python-telegram-bot` v22 | Telegram bot framework (async) |
| `ib_async` v2.1.0 | Interactive Brokers TWS API |
| `anthropic` v0.112.0 | Claude AI API |
| `yfinance` | Market data (ETF prices, benchmark) |
| `pandas` + `matplotlib` | Data processing and chart generation |

## Prerequisites

- Python 3.11+
- Interactive Brokers account with TWS running locally on port 7497
- Anthropic API key ([console.anthropic.com](https://console.anthropic.com))
- Telegram bot token ([@BotFather](https://t.me/BotFather))

## Setup

**1. Clone the repository**
```bash
git clone https://github.com/david-deluca/andorra-bot.git
cd andorra-bot
```

**2. Create virtual environment**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure environment variables**
```bash
cp .env.example .env
```
Edit `.env` with your credentials:
```env
TELEGRAM_TOKEN=your_telegram_bot_token
ANTHROPIC_API_KEY=your_anthropic_api_key
IBKR_HOST=127.0.0.1
IBKR_PORT=7497
IBKR_CLIENT_ID=1
```

**5. Run**
```bash
python main.py
```

## Usage
/portfolio                          → Live IBKR account summary

/performance                        → Portfolio vs benchmark chart

/projection 10000 500 7 20          → €10k initial, €500/month, 7% return, 20 years

/ask Should I rebalance my portfolio now?
## Key Technical Decisions

- **Fully async architecture** — all Telegram handlers and IBKR calls use `asyncio` to avoid blocking
- **In-memory chart generation** — matplotlib charts are generated as `BytesIO` objects, never written to disk
- **Stateless Claude integration** — Boglehead context injected via system prompt on every API call
- **EUR/BASE currency handling** — IBKR reports P&L as `$LEDGER` tags in `BASE` currency; standard tags filtered by EUR

## Limitations

- `/portfolio` requires TWS running locally — not available when TWS is closed
- Bot runs locally (no cloud deployment yet) — must be started manually

## Author

David De Luca — Élève-ingénieur INSA Toulouse, département MIC (AI & Data)  
[GitHub](https://github.com/david-deluca) · [LinkedIn] (www.linkedin.com/in/david-de-luca-soares-34a93029b)
