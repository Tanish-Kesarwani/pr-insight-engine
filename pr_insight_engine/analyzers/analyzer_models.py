from dataclasses import dataclass
from typing import List


@dataclass
class AnalyzerFinding:
    tool: str
    file_path: str
    message: str
    severity: str
    line: int | None = None


@dataclass
class AnalyzerSummary:
    file_path: str
    total_findings: int
    semgrep_findings: int
    bandit_findings: int
    findings: List[AnalyzerFinding]
