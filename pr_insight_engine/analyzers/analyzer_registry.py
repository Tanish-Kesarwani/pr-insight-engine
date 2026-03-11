from .python_analyzer import PythonAnalyzer

class AnalyzerRegistry:
    """
    Registry that maps file extensions to analyzers.
    """

    def __init__(self):
        self.registry = {
            ".py": PythonAnalyzer(),
        }

    def get_analyzer(self, file_path: str):
        for ext, analyzer in self.registry.items():
            if file_path.endswith(ext):
                return analyzer
        return None