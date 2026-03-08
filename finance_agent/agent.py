# finance_agent/agent.py

from finance_agent.llm.local_agent import MarketInterpreter

_interpreter = MarketInterpreter()

def chat(message: str) -> str:
    """
    Public entrypoint for the rest of your app.
    Uses tool-aware chat by default.
    """
    return _interpreter.chat_with_tools(message)
