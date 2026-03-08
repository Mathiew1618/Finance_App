from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ToolCall(BaseModel):
    id: str
    name: str
    arguments: Dict[str, Any] = Field(default_factory=dict)


class ToolResult(BaseModel):
    id: str
    ok: bool
    result: Any | None = None
    error: Optional[str] = None


class MCPRequest(BaseModel):
    id: str
    type: str
    tool_calls: List[ToolCall] = Field(default_factory=list)


class MCPResponse(BaseModel):
    id: str
    type: str
    results: List[ToolResult] = Field(default_factory=list)
