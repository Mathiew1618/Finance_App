import json
import requests
from finance_agent import tools


class MarketInterpreter:
    """
    Full tool-enabled LLM interface for LM Studio.
    Supports:
    - chat()
    - chat_with_tools()
    - automatic tool-call execution
    """

    def __init__(self):
        self.api_url = "http://localhost:1234/v1/chat/completions"
        self.model_name = "mistralai/ministral-3-3b"  # MUST MATCH LM STUDIO EXACTLY

        self.system_prompt = (
            "You are a financial analysis assistant. "
            "You can call tools using JSON when needed. "
            "If you need market data, ALWAYS call a tool instead of guessing."
        )

        # Tool registry
        self.TOOLS = {
            "snapshot_symbol": {
                "description": "Get latest price and basic stats for a stock symbol.",
                "args": ["symbol"],
                "func": tools.snapshot_symbol,
            },
            "get_ohlc": {
                "description": "Get OHLC candles for a stock symbol.",
                "args": ["symbol", "timeframe", "limit"],
                "func": tools.get_ohlc,
            },
            "render_chart": {
                "description": "Render a candlestick chart and return the file path.",
                "args": ["symbol", "ohlc"],
                "func": tools.render_chart,
            },
        }

    # ---------------------------------------------------------
    # BASIC CHAT (no tools)
    # ---------------------------------------------------------
    def chat(self, message: str) -> str:
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": message},
            ],
            "temperature": 0.7,
        }

        try:
            response = requests.post(
                self.api_url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(payload),
            )
            data = response.json()
        except Exception as e:
            return f"[LM Studio Error] {e}"

        try:
            return data["choices"][0]["message"]["content"]
        except Exception:
            return f"[Unexpected LM Studio Response] {data}"

    # ---------------------------------------------------------
    # TOOL-ENABLED CHAT
    # ---------------------------------------------------------
    def chat_with_tools(self, message: str) -> str:
        """
        Allows the LLM to call Python tools using JSON.
        """

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": message},
        ]

        while True:
            payload = {
                "model": self.model_name,
                "messages": messages,
                "temperature": 0.7,
            }

            try:
                response = requests.post(
                    self.api_url,
                    headers={"Content-Type": "application/json"},
                    data=json.dumps(payload),
                )
                data = response.json()
            except Exception as e:
                return f"[LM Studio Error] {e}"

            msg = data["choices"][0]["message"]

            # If it's a normal assistant response → return it
            if "tool_calls" not in msg:
                return msg["content"]

            # Otherwise, execute tool calls
            for tool_call in msg["tool_calls"]:
                name = tool_call["function"]["name"]
                args = json.loads(tool_call["function"]["arguments"])

                if name not in self.TOOLS:
                    messages.append({
                        "role": "tool",
                        "content": f"[Error] Unknown tool: {name}",
                        "tool_call_id": tool_call["id"],
                    })
                    continue

                try:
                    result = self.TOOLS[name]["func"](**args)
                except Exception as e:
                    result = f"[Tool Error] {e}"

                # Send tool result back to LLM
                messages.append({
                    "role": "tool",
                    "content": json.dumps(result),
                    "tool_call_id": tool_call["id"],
                })
