# 🧠 Yerb's Forex Trading Agents

An advanced AI-powered trading system where GPT-driven agents collaborate to analyze, improve, and execute forex strategies. Each agent plays a unique role — from risk management to strategy evolution — and they talk to each other to optimize performance over time.

> 🤖 Agents talk. Strategies evolve. Trades get smarter.

---

## 🚀 Features

- ✅ GPT-powered strategy improvement
- 🧠 Agents for backtesting, journaling, correlation, and more
- 💬 Telegram integration for logging and conversation summaries
- 📊 Self-improving logic based on journal + backtest feedback
- 🔁 Modular design for future agent expansion

---

## 🧩 Agent System Overview



your_project/
│
├── agents/
│   ├── agent_orchestrator.py        
│   ├── backtesting_agent.py
│   ├── conversation_agent.py
│   ├── correlation_agent.py
│   ├── correlation_discovery_agent.py
│   ├── decision_agent.py
│   ├── journal_agent.py
│   ├── log_agent.py
│   ├── market_watcher_agent.py
│   ├── risk_manager_agent.py
│   ├── self_improver_agent.py
│   ├── sentiment_agent.py
│   ├── strategy_agent.py
│   ├── strategy_creator_agent.py
│   ├── strategy_improver_agent.py
│   ├── trade_executor_agent.py
│
├── utils/
│   ├── config_loader.py
│   ├── context.py
│   ├── openai_helper.py
│   ├── strategy_selector.py
│   ├── telegram_alert.py
│
├── strategies/                      
│   └── ...
│
├── data/
│   └── trade_logs.db
│
├── .env
├── strategy_config.json
├── requirements.txt
├── README.md


---

## 🧪 Getting Started

1. Clone the repo  
   `git clone https://github.com/YOUR_USERNAME/Yerb-Forex-Agents.git`

2. Install dependencies  
   `pip install -r requirements.txt`

3. Setup `.env` file  
   ```env
   OPENAI_API_KEY=your_openai_key
   TELEGRAM_BOT_TOKEN=your_bot_token
   TELEGRAM_CHAT_ID=your_chat_id

python -m XAUUSD_Data.main


SelfImprov Agent:
- Strategy too strict. No trades last 24h.
- Consider using RSI + EMA instead of EMA only.

StrategyImprover Agent:
Strategy updated and saved as: ema_strategy_v2_...

🗣️ Agent Roundtable:
SelfImprov: "The strategy's too passive."
Sentiment: "Market's bullish — act!"
Decision: "We should trigger a BUY."

Final Agent Context:
symbol: XAUUSD
sentiment: positive
signal: BUY
...

Built With
Python

MetaTrader5

OpenAI GPT API

Backtesting.py

Telegram Bot API

## ⚡ Future Ideas
Dynamic agent evaluation (fire bad agents)

Auto-deployment to live trading

Strategy marketplace

Real-time sentiment feeds

Author - Yerba_M
> ⚠️ Never commit your `.env` or API keys to GitHub.
