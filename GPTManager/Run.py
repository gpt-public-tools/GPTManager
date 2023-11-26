
from dataclasses import dataclass, field
from typing import Dict, Any, Optional

@dataclass
class Tool:
    type: str

@dataclass
class RunObject:
    id: str
    object: str
    created_at: int
    assistant_id: str
    thread_id: str
    status: str
    started_at: int
    expires_at: Optional[int]
    cancelled_at: Optional[int]
    failed_at: Optional[int]
    completed_at: Optional[int]
    last_error: Optional[str]
    model: str
    instructions: Optional[str]
    tools: list[Tool]
    file_ids: list[Any] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

class Run:
    __run: RunObject  = None
