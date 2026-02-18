import subprocess
from dataclasses import dataclass, asdict
from typing import List


@dataclass
class FileDiff:
    file_path: str
    added_lines: List[str]
    deleted_lines: List[str]


class GitDiffParser:
    """
    Git diff parser for PR Insight Engine.
    Extracts changed files and line-level additions/deletions.
    """

    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path

    def _run_git_diff(self) -> str:
        result = subprocess.run(
            ["git", "diff"],
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError("git diff command failed")

        return result.stdout

    def parse(self) -> List[FileDiff]:
        diff_text = self._run_git_diff()

        if not diff_text.strip():
            return []

        return self._parse(diff_text)

    def _parse(self, diff_text: str) -> List[FileDiff]:
        results = []
        current = None

        for line in diff_text.splitlines():

            # detect new file block
            if line.startswith("diff --git"):
                if current:
                    results.append(current)

                file_path = line.split()[-1].replace("b/", "")

                current = FileDiff(
                    file_path=file_path,
                    added_lines=[],
                    deleted_lines=[]
                )

            elif line.startswith("+") and not line.startswith("+++"):
                if current:
                    current.added_lines.append(line[1:])

            elif line.startswith("-") and not line.startswith("---"):
                if current:
                    current.deleted_lines.append(line[1:])

        if current:
            results.append(current)

        return results

    @staticmethod
    def to_dict(file_diffs: List[FileDiff]):
        return [asdict(d) for d in file_diffs]
