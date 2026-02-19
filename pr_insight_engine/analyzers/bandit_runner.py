import json
import subprocess
from pathlib import Path
from typing import List

from .analyzer_models import AnalyzerFinding

class BanditRunner:
    """
    Runs Bandit on a given file
    """

    def run(self, file_path: str) -> List[AnalyzerFinding]:
        if not Path(file_path).exists():
            return []

        try:
            result = subprocess.run(
                ["bandit", "-f", "json", file_path],
                capture_output=True,
                text=True,
            )

            if not result.stdout:
                return []

            data = json.loads(result.stdout)
            findings: List[AnalyzerFinding] = []

            for issue in data.get("results", []):
                findings.append(
                    AnalyzerFinding(
                        tool="bandit",
                        file_path=issue.get("filename"),
                        message=issue.get("issue_text", ""),
                        severity=issue.get("issue_severity", "LOW"),
                        line=issue.get("line_number"),
                    )
                )

            return findings

        except Exception:
            return []