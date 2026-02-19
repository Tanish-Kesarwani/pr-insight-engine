from dataclasses import dataclass
from typing import List

@dataclass
class FileContext:
    file_path: str
    tags: List[str]
    weight: float