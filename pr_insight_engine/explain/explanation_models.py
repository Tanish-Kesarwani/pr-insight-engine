from dataclasses import dataclass
from typing import List

@dataclass
class RiskExplanation:
    file_path: str
    messages: List[str]
