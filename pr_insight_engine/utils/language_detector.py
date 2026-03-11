import os


class LanguageDetector:
    """
    Detects programming languages used in a repository
    while ignoring system directories.
    """

    EXTENSION_MAP = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".java": "java",
        ".go": "go",
        ".rb": "ruby",
        ".cpp": "cpp",
        ".c": "c",
        ".cs": "csharp",
    }

    IGNORED_DIRS = {
        "venv",
        ".git",
        "__pycache__",
        "node_modules",
        "dist",
        "build"
    }

    def detect_languages(self, repo_path: str):
        languages = set()

        for root, dirs, files in os.walk(repo_path):

            # remove ignored directories from traversal
            dirs[:] = [d for d in dirs if d not in self.IGNORED_DIRS]

            for file in files:
                _, ext = os.path.splitext(file)

                if ext in self.EXTENSION_MAP:
                    languages.add(self.EXTENSION_MAP[ext])

        return sorted(languages)