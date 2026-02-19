import json
import subprocess
from pathlib import Path
from typing import List

from .analyzer_models import AnalyzerFinding


class SemgrepRunner:
    """
    Runs Semgrep on a given file and parses results.
    """

    def run(self, file_path: str) -> List[AnalyzerFinding]:
        if not Path(file_path).exists():
            return []

        try:
            result = subprocess.run(
                ["semgrep", "--json", file_path],
                capture_output=True,
                text=True,
            )

            if result.returncode not in (0, 1):
                return []

            data = json.loads(result.stdout)
            findings: List[AnalyzerFinding] = []

            for res in data.get("results", []):
                findings.append(
                    AnalyzerFinding(
                        tool="semgrep",
                        file_path=res.get("path"),
                        message=res.get("extra", {}).get("message", ""),
                        severity=res.get("extra", {}).get("severity", "INFO"),
                        line=res.get("start", {}).get("line"),
                    )
                )

            return findings

        except Exception:
            return []
