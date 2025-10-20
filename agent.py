# =========================================================
#  ICM AI Trader Agent – ASI:One Compatible
# =========================================================
from datetime import datetime
from uuid import uuid4
from uagents import Agent, Context, Protocol, Model
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    StartSessionContent,
    TextContent,
    chat_protocol_spec,
)
import statistics, re, os, uuid

# =========================================================
#  Models
# =========================================================
class MarketNewsRequest(Model):
    request_id: str


class MarketNewsResponse(Model):
    sentiment: str
    impact_score: float
    summary: str


# =========================================================
#  Helper Function for Chat Messages
# =========================================================
def create_text_chat(text: str, end_session: bool = False) -> ChatMessage:
    content = [TextContent(type="text", text=text)]
    if end_session:
        content.append(EndSessionContent(type="end-session"))
    return ChatMessage(timestamp=datetime.utcnow(), msg_id=uuid4(), content=content)


# =========================================================
#  Agent Setup
# =========================================================
agent = Agent(
    name="icm_ai_trader",
    seed="want human trial stomach room begin fever minimum east shoulder trumpet electric",
    port=8000,
    mailbox=True,
    publish_agent_details=True,
    api_key=os.getenv("ASI_API_KEY"),
)

chat_protocol = Protocol(spec=chat_protocol_spec)

# =========================================================
#  Core Logic (Solana Portfolio Analyzer)
# =========================================================
def analyze_portfolio(text: str) -> str:
    # Example extraction
    text_lower = text.lower()
    token = re.search(r"(sol|eth|btc|usdc|ada|dot|avax)", text_lower)
    token = token.group(1).upper() if token else "SOL"

    price = re.search(r"\$?(\d+(\.\d+)?)", text_lower)
    current_price = float(price.group(1)) if price else 200.0

    entry = re.search(r"entry\s*\$?(\d+(\.\d+)?)", text_lower)
    entry_price = float(entry.group(1)) if entry else 180.0

    pnl = ((current_price - entry_price) / entry_price) * 100
    advice = (
        f"📊 {token} is currently ${current_price:.2f}, entry at ${entry_price:.2f}. "
        f"PnL: {pnl:.2f}%. "
    )

    if pnl < -10:
        advice += "It’s dipping — consider DCAing gradually."
    elif pnl > 10:
        advice += "You’re in profit — think about partial take-profit."
    else:
        advice += "Hold steady, market is sideways."

    return advice


# =========================================================
#  Chat Protocol Handlers
# =========================================================
@chat_protocol.on_message(ChatMessage)
async def handle_chat(ctx: Context, sender: str, msg: ChatMessage):
    await ctx.send(
        sender,
        ChatAcknowledgement(timestamp=datetime.utcnow(), acknowledged_msg_id=msg.msg_id),
    )

    if any(isinstance(c, StartSessionContent) for c in msg.content):
        await ctx.send(sender, create_text_chat("Hi! I can analyze your Solana or crypto portfolio.", end_session=False))
        return

    # FIXED text extraction
    text = " ".join(
        c.text.strip() for c in msg.content if isinstance(c, TextContent) and hasattr(c, "text")
    ).strip()

    if not text:
        return

    try:
        reply_text = analyze_portfolio(text)
    except Exception as e:
        ctx.logger.exception("Error in analyze_portfolio")
        reply_text = f"⚠️ Something went wrong: {e}"

    await ctx.send(sender, create_text_chat(reply_text, end_session=True))


@chat_protocol.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    pass


# =========================================================
#  Include and Run Agent
# =========================================================
agent.include(chat_protocol, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
