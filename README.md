# 🤖 fr-icm trading agent — Multi-Agent AI for Market Intelligence & Automated Trade Decisions

## 🧩 Overview

The **ICM Trading Agent** is a **multi-agent, AI-powered autonomous trading system** that operates within the **Internet Capital Markets (ICM)** ecosystem.
It is designed to enable **collaborative, intelligent trading decisions** by combining **local portfolio analytics** with **decentralized market intelligence** gathered from other agents — known as **market gossip**.

This gossip-based communication model allows the agent to analyze both **real market signals** (industry news, trends, social buzz) and **internal system data** (historical pool prices, holdings, and portfolio metrics) to determine whether to **buy**, **sell**, **hold**, or **DCA (dollar-cost average)** — including the **percentage** of capital to allocate.

---

## 💡 Key Capabilities

* 🕸️ **Multi-Agent Communication** — Exchanges market insights and strategies through decentralized gossip with other agents.
* 📊 **Portfolio Awareness** — Accesses internal data such as pool history, current holdings, and token performance.
* 🧠 **AI Decision Logic** — Analyzes historical prices and profit/loss to generate precise trade signals and allocation percentages.
* ⚙️ **Automated Signal Response** — Produces structured trade decisions usable by trading systems, bots, or dashboards.
* 🌍 **Interoperable by Design** — Built using the **uAgents framework**, compatible with the **Fetch.ai Agentverse** ecosystem.

---

## 🧭 Use Case Examples

### 1. Autonomous Portfolio Adjustment

A local agent collects pool data and sends it to the gossip agent.
The gossip agent analyzes price trends and returns a **“BUY 15%”** or **“SELL 10%”** signal, allowing automated rebalancing without human input.

### 2. Market Sentiment-Driven Decision Making

When several connected agents report bearish sentiment or declining on-chain liquidity, the gossip agent suggests **“HOLD”** or **“REDUCE EXPOSURE”** decisions.

### 3. Cross-Agent Intelligence

By aggregating news and trading signals across multiple ecosystems, the gossip agent becomes a **collective intelligence node** — improving accuracy through shared context.

---

## 🔌 Capabilities & APIs

### Supported Message Models

| Model            | Description                                                                                        |
| ---------------- | -------------------------------------------------------------------------------------------------- |
| **PriceRequest** | Sent by the local agent to provide token data (current price, entry, historical prices, holdings). |
| **TradeSignal**  | Returned by the gossip agent with a recommended action and allocation percentage.                  |

### Interaction Flow

1. **Local Agent → Gossip Agent:** Sends `PriceRequest`
2. **Gossip Agent → Local Agent:** Returns `TradeSignal` (e.g. `BUY 15%`)
3. **Executor (optional):** Applies trade action through ICM or connected DEX infrastructure

---

### Example Interaction

**Request**

```json
{
  "token": "RAY",
  "current_price": 0.35,
  "entry_price": 0.4,
  "historical_prices": [0.42, 0.38, 0.36, 0.35],
  "current_holdings": 25
}
```

**Response**

```json
{
  "signal": "BUY",
  "percent": 15.0
}
```

---

## ⚙️ Implementation Summary

The gossip agent uses **statistical reasoning** to analyze prices and holdings:

* **DCA** when PnL < -10% and holdings < 50%
* **SELL** when PnL > 10% and holdings > 10%
* **BUY** when current price is significantly below mean
* **SELL** when current price is significantly above mean
* **HOLD** otherwise

This makes it adaptable to changing market conditions without constant retraining or fine-tuning.

---

## 🧠 Interaction Modes

* **Agent-to-Agent Messaging** — Communicates directly with other Fetch.ai or uAgents-compatible nodes.
* **Local Integration** — Can be embedded into backend systems to send/receive trade signals.
* **API Calls** — Accessible via HTTP or agent mailboxes for connected clients.

---

## 🚫 Limitations & Scope

* The agent **does not execute trades** directly — it only provides **signals**.
* It **does not interpret real-world news feeds** unless connected to other data-providing agents.
* It **requires** portfolio and price data input from an external system or another ICM node.
* The decision model is **rule-based** with statistical reasoning, not deep learning (for now).

---

## 🔍 Relevant Keywords & Tags

`autonomous trading`, `crypto`, `gossip protocol`, `portfolio intelligence`,
`Fetch.ai`, `uAgents`, `AI trading`, `ICM`, `Solana trading bot`, `decentralized finance`,
`AI market signals`, `DeFi agent`, `trading signal API`, `AI portfolio management`

---

## 🧾 License

This project is licensed under the **MIT License**.
See the `LICENSE` file for full terms.

---

## 💬 Contact

* **Project Repository**: [[GitHub Repository Link](https://github.com/OkarFabianTheWise/fr-icm-uagent)]

---

*Built for the decentralized trading era — where AI agents learn, share, and trade together.*
