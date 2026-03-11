from abc import ABC, abstractmethod
"""
Base interface for all language analyzers.
Every analyzer must implement analyze()
"""
class BaseAnalyzer(ABC):
    @abstractmethod
    def analyze(self, file_path: str):
        pass