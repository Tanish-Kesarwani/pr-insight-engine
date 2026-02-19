from pr_insight_engine.diff.diff_parser import GitDiffParser
from pr_insight_engine.analyzers.analyzer_service import AnalyzerService
from pr_insight_engine.complexity.complexity_service import ComplexityService

def run_pipeline_test():
    print("\n=== PR Insight Engine - Phase 3.5 Test ===\n")

    #step 1: detect changed files
    parser=GitDiffParser(".")
    diffs=parser.parse()

    if not diffs:
        print("no uncommitted changes detected")
        return
    analyzer= AnalyzerService()
    complexity_service=ComplexityService()

    #step 2 analyze each file
    for d in diffs:
        print(f"\nAnalyzing file: {d.file_path}")
        
        #--- static analysis---
        summary=analyzer.analyze_file(d.file_path)
        print(f" Total findings: {summary.total_findings}")
        print(f" Semgrep findings: {summary.semgrep_findings}")
        print(f" Bandit findings: {summary.bandit_findings}")

        #--- complexity analysis ---
        comp_summary= complexity_service.analyze_file(d.file_path)
        print(f" avg complexity: {comp_summary.average_complexity: .2f}")
        print(f" max complexity: {comp_summary.max_complexity}")

        # --- simple risk hint ---
        if summary.total_findings > 0 or comp_summary.max_complexity >=10:
            print(" review recommended")

        else:
            print(" looks good")
        print("-" * 60)

if __name__ == "__main__":
    run_pipeline_test()