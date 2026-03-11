from .base_analyzer import BaseAnalyzer
from .analyzer_service import AnalyzerService

class PythonAnalyzer(BaseAnalyzer):
    """
    Python analyzer plugin.
    Uses existing AnalyzerService internally.
    """

    def __init__(self):
        self.analyzer_service = AnalyzerService()
    def analyze(self, file_path: str):
        return self.analyzer_service.analyze_file(file_path)