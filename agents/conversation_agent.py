from XAUUSD_Data.utils.context import dump
from XAUUSD_Data.utils.openai_helper import ask_gpt
from XAUUSD_Data.utils.telegram_alert import send_telegram_message
from XAUUSD_Data.agents.strategy_improver_agent import improve_strategy

def simulate_agent_conversation():
    ctx = dump()

    chat_prompt = f"""
The following is a roundtable conversation between AI agents in an automated trading system. Each agent has a unique role.

They are reviewing this shared trading context:
{ctx}

Now they will discuss if a trade should be executed and what to improve.

Each agent speaks in character. Format:
AgentName: "Response here."

Start the conversation:
"""

    return ask_gpt(chat_prompt, temperature=0.4)
