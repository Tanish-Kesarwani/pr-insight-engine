from typing import List

from .complexity_models import ComplexitySummary
from .radon_runner import RadonRunner


class ComplexityService:
    """
    Provides file-level complexity summary.
    """

    def __init__(self):
        self.radon = RadonRunner()

    def analyze_file(self, file_path: str) -> ComplexitySummary:
        functions = self.radon.run(file_path)

        if not functions:
            return ComplexitySummary(
                file_path=file_path,
                average_complexity=0.0,
                max_complexity=0,
                functions=[],
            )

        complexities = [f.complexity for f in functions]

        avg_complexity = sum(complexities) / len(complexities)
        max_complexity = max(complexities)

        return ComplexitySummary(
            file_path=file_path,
            average_complexity=avg_complexity,
            max_complexity=max_complexity,
            functions=functions,
        )
