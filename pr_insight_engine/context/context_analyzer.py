from .context_models import FileContext

class ContextAnalyzer:
    """
    Adds repository-aware context weighting
    """

    #simple keyword rules (extensible later)
    SENSITIVE_KEYWORDS = ["auth", "security", "payment", "config", "secret", "token",]
    CORE_KEYWORDS = ["core", "engine", "service", "api",]
    LOW_RISK_KEYWORDS = ["test", "docs", "example", "sample",]

    def analyze_file(self, file_path: str) -> FileContext:
        path_lower = file_path.lower()
        tags=[]
        weight=1.0

        # --- priority-based classification ---
        if any(k in path_lower for k in self.SENSITIVE_KEYWORDS):
            tags.append("sensitive_module")
            weight *= 1.4

        elif any(k in path_lower for k in self.CORE_KEYWORDS):
            tags.append("core_module")
            weight *= 1.2

        elif any(k in path_lower for k in self.LOW_RISK_KEYWORDS):
            tags.append("low_risk_area")
            weight *= 0.8


        return FileContext(
            file_path=file_path,
            tags=tags,
            weight=round(weight,2),
        )