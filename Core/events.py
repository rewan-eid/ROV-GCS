from dataclasses import dataclass, field
from typing import Any
import time


@dataclass
class Event:
    event_type: str
    data: dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)