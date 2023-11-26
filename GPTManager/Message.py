from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class TextContent:
    value: str
    annotations: List[Any] = field(default_factory=list)

@dataclass
class Content:
    type: str
    text: TextContent

@dataclass
class MessageObject:
    id: str
    object: str
    created_at: int
    thread_id: str
    role: str
    content: List[Content]
    file_ids: List[Any] = field(default_factory=list)
    assistant_id: str
    run_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    