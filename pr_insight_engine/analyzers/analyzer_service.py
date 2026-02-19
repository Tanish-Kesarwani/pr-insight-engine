from typing import List

from .analyzer_models import AnalyzerSummary
from .semgrep_runner import SemgrepRunner
from .bandit_runner import BanditRunner

class AnalyzerService:
    """
    Cordinates multiple analyzers for a file
    """

    def __init__(self):
        self.semgrep_runner = SemgrepRunner()
        self.bandit_runner = BanditRunner()

    def analyze_file(self, file_path: str) -> AnalyzerSummary:
        semgrep_findings = self.semgrep_runner.run(file_path)
        bandit_findings = self.bandit_runner.run(file_path)

        all_findings = semgrep_findings + bandit_findings

        return AnalyzerSummary(
            file_path=file_path,
            total_findings=len(all_findings),
            semgrep_findings=len(semgrep_findings),
            bandit_findings=len(bandit_findings),
            findings=all_findings,
        )