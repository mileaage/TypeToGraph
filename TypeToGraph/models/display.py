from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class DisplayNode:
    """Unified represenation"""
    id: str
    x: float
    y: float
    label: str
    data: Any = None
    parent_id: Optional[str] = None