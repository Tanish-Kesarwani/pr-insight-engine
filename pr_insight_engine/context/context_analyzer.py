from .context_models import ContextResult


class ContextAnalyzer:
    """
    Advanced context analyzer that assigns context tags
    based on file paths.
    """

    SENSITIVE_PATHS = [
        "auth",
        "security",
        "crypto",
        "token",
        "password",
    ]

    CRITICAL_PATHS = [
        "payment",
        "billing",
        "checkout",
        "transaction",
        "order",
    ]

    DATA_PATHS = [
        "database",
        "models",
        "repository",
        "dao",
    ]

    TEST_PATHS = [
        "test",
        "tests",
    ]

    CORE_PATHS = [
        "core",
        "engine",
        "service",
    ]

    def analyze_file(self, file_path: str):

        path = file_path.lower()

        tags = []
        weight = 1.0

        # sensitive security modules
        if any(p in path for p in self.SENSITIVE_PATHS):
            tags.append("sensitive_module")
            weight = 1.4

        # critical business logic
        elif any(p in path for p in self.CRITICAL_PATHS):
            tags.append("critical_business_logic")
            weight = 1.5

        # data layer
        elif any(p in path for p in self.DATA_PATHS):
            tags.append("data_layer")
            weight = 1.3

        # test code
        elif any(p in path for p in self.TEST_PATHS):
            tags.append("test_code")
            weight = 0.8

        # core infrastructure
        elif any(p in path for p in self.CORE_PATHS):
            tags.append("core_module")
            weight = 1.2

        return ContextResult(
            file_path=file_path,
            tags=tags,
            weight=weight,
        )