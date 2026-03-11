from dataclasses import dataclass
from typing import List

@dataclass
class ContextResult:
    file_path: str
    tags: List[str]
    weight: float