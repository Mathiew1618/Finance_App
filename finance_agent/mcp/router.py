from typing import Any, Callable, Dict
from .protocol import MCPRequest, MCPResponse, ToolResult

ToolFunc = Callable[..., Any]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: Dict[str, ToolFunc] = {}

    def register(self, name: str, func: ToolFunc) -> None:
        if name in self._tools:
            raise ValueError(f"Tool '{name}' already registered")
        self._tools[name] = func

    def get(self, name: str) -> ToolFunc:
        if name not in self._tools:
            raise KeyError(f"Unknown tool '{name}'")
        return self._tools[name]


registry = ToolRegistry()


def tool(name: str):
    def decorator(func: ToolFunc) -> ToolFunc:
        registry.register(name, func)
        return func
    return decorator


def handle_request(request: MCPRequest) -> MCPResponse:
    results: list[ToolResult] = []

    for call in request.tool_calls:
        try:
            func = registry.get(call.name)
            value = func(**call.arguments)
            results.append(ToolResult(id=call.id, ok=True, result=value))
        except Exception as exc:
            results.append(ToolResult(id=call.id, ok=False, error=str(exc)))

    return MCPResponse(id=request.id, type="tool_result", results=results)
