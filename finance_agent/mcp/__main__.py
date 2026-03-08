from .protocol import MCPRequest, ToolCall
from .router import handle_request
from .. import agent  # ensures tools register


def main() -> None:
    req = MCPRequest(
        id="demo-1",
        type="tool_call",
        tool_calls=[ToolCall(id="1", name="ping", arguments={"message": "hello"})],
    )
    resp = handle_request(req)
    print(resp.model_dump())


if __name__ == "__main__":
    main()
