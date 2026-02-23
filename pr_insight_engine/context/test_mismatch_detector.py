from typing import List

class TestMismatchResult:
    def __init__(self, mismatch: bool):
        self.mismatch= mismatch

class TestMismatchDetector:
    """
    Detects if source code changed without corresponding test updates.
    """

    TEST_KEYWORDS=["test", "tests", "spec"]
    SOURCE_KEYWORDS=[".py"]

    def analyze(self, changed_files: List[str]) -> TestMismatchResult:
        has_source_change= False
        has_test_change= False

        for path in changed_files:
            path_lower= path.lower()

            #detect test files
            if any(k in path_lower for k in self.TEST_KEYWORDS):
                has_test_change=True
            #detect source files(simple heuristic)
            elif path_lower.endswith(".py"):
                has_source_change=True

            mismatch= has_source_change and not has_test_change
            return TestMismatchResult(mismatch=mismatch)