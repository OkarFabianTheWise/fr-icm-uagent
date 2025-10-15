# icm_ai_trader_agent.py
# =========================================================
# ICM Trading Agent – ASI:One Compatible (Chat + Trading)
# =========================================================

from uagents import Agent, Context, Model, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatMessage,
    ChatAcknowledgement,
    TextContent,
    chat_protocol_spec,
)
import statistics
import time
import uuid

# =========================================================
#  Models
# =========================================================
class PriceRequest(Model):
    token: str
    current_price: float
    entry_price: float
    historical_prices: list
    current_holdings: float


class TradeSignal(Model):
    signal: str
    percent: float


# =========================================================
#  Agent Setup
# =========================================================
agent = Agent(
    name="icm_ai_trader",
    seed="want human trial stomach room begin fever minimum east shoulder trumpet electric",
    port=8000,
    mailbox=True,
    publish_agent_details=True,
    # Hardcoded insecure key for ASI:One (replace later)
    api_key="sk_69b779d0e215476a880045ea71cf12cd9e0d7c56c204448dbbbdd3605cab0f9c",
)

# Create Chat Protocol
chat_protocol = Protocol(spec=chat_protocol_spec)


# =========================================================
#  Core Trading Logic
# =========================================================
@agent.on_message(model=PriceRequest, replies=TradeSignal)
async def decide(ctx: Context, sender: str, msg: PriceRequest):
    prices = msg.historical_prices
    current = msg.current_price
    entry = msg.entry_price
    holdings = msg.current_holdings

    if not prices or len(prices) < 2:
        await ctx.send(sender, TradeSignal(signal="HOLD", percent=0))
        return

    mean_price = statistics.mean(prices)
    std_price = statistics.pstdev(prices) if len(prices) > 1 else 0.0
    pnl = ((current - entry) / entry) * 100

    if pnl <= -10 and holdings < 50:
        decision = "DCA"
        percent = min(10, 50 - holdings)
    elif pnl >= 10 and holdings > 10:
        decision = "SELL"
        percent = min(25, holdings - 10)
    elif current < mean_price - 0.5 * std_price and holdings < 50:
        decision = "BUY"
        percent = min(50 - holdings, ((mean_price - current) / mean_price) * 100)
    elif current > mean_price + 0.5 * std_price and holdings > 10:
        decision = "SELL"
        percent = min(holdings - 10, ((current - mean_price) / mean_price) * 100)
    else:
        decision = "HOLD"
        percent = 0

    ctx.logger.info(
        f"📊 {msg.token}: {decision} {percent:.1f}% | pnl={pnl:.1f}% | holdings={holdings}%"
    )

    await ctx.send(sender, TradeSignal(signal=decision, percent=round(percent, 2)))


# =========================================================
#  Chat Protocol Logic
# =========================================================
@chat_protocol.on_message(ChatMessage)
async def handle_chat(ctx: Context, sender: str, msg: ChatMessage):
    # Acknowledge receipt
    await ctx.send(
        sender,
        ChatAcknowledgement(
            timestamp=int(time.time()),
            acknowledged_msg_id=msg.msg_id,
        ),
    )

    # Extract full chat text
    user_message = ""
    for content in msg.content:
        if isinstance(content, TextContent):
            user_message += content.text

    ctx.logger.info(f"💬 Chat message received: {user_message}")

    # Simple logic to respond conversationally
    user_message_lower = user_message.lower()
    if "buy" in user_message_lower:
        reply_text = "I'd recommend checking the trend first. If momentum is strong, buy gradually (DCA)."
    elif "sell" in user_message_lower:
        reply_text = "If your PnL is above 10%, consider partial profit-taking."
    elif "hold" in user_message_lower:
        reply_text = "Holding might be best if volatility is high but fundamentals are unchanged."
    elif "signal" in user_message_lower or "what should i do" in user_message_lower:
        reply_text = "I can analyze portfolio data and market gossip to suggest BUY, HOLD, or SELL."
    else:
        reply_text = "Hello! I’m the ICM AI Trading Agent — I provide trade signals and insights using market gossip and portfolio data."

    # Send chat response
    reply = ChatMessage(
        msg_id=str(uuid.uuid4()),
        content=[TextContent(text=reply_text)],
    )

    await ctx.send(sender, reply)


# =========================================================
#  Run
# =========================================================
if __name__ == "__main__":
    agent.add_protocol(chat_protocol)
    agent.run()
