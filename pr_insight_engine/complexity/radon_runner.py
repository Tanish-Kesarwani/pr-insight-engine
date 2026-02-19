import subprocess
import json
from pathlib import Path
from typing import List

from .complexity_models import FunctionComplexity


class RadonRunner:
    """
    Runs Radon to compute cyclomatic complexity.
    """

    def run(self, file_path: str) -> List[FunctionComplexity]:
        if not Path(file_path).exists():
            return []

        try:
            result = subprocess.run(
                ["radon", "cc", "-j", file_path],
                capture_output=True,
                text=True,
            )

            if not result.stdout:
                return []

            data = json.loads(result.stdout)
            functions: List[FunctionComplexity] = []

            for item in data.get(file_path, []):
                functions.append(
                    FunctionComplexity(
                        name=item.get("name"),
                        complexity=item.get("complexity"),
                        lineno=item.get("lineno"),
                    )
                )

            return functions

        except Exception:
            return []
