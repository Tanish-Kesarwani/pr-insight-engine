from pr_insight_engine.diff.diff_parser import GitDiffParser
from pr_insight_engine.analyzers.analyzer_service import AnalyzerService

def run_pipeline_test():
    print("\n=== PR Insight Engine - Phase 2.5 Test ===")

    #step 1: get changed files
    parser= GitDiffParser(".")
    diffs=parser.parse()

    if not diffs:
        print("No uncommitted changes detected.")
        return
    
    analyzer = AnalyzerService()

    #step 2: analyze each changed file
    for d in diffs:
        print(f"\nAnalyzing file: {d.file_path}")
        summary = analyzer.analyze_file(d.file_path)
        print(f"Total Findings: {summary.total_findings}")
        print(f"Semgrep Findings: {summary.semgrep_findings}")
        print(f"Bandit Findings: {summary.bandit_findings}")

        if summary.total_findings ==0:
            print("No issues found.")
        else:
            print("Issues Detected")

        print("-" * 50)

if __name__ == "__main__":    run_pipeline_test()