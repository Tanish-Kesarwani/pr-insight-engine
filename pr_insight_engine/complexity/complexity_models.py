from dataclasses import dataclass
from typing import List

@dataclass
class FunctionComplexity:
    name: str
    complexity: int
    lineno: int

@dataclass
class ComplexitySummary:
    file_path: str
    average_complexity: float
    max_complexity: int
    functions: List[FunctionComplexity]