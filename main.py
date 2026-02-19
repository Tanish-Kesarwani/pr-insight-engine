from pr_insight_engine.diff.diff_parser import GitDiffParser
from pr_insight_engine.analyzers.analyzer_service import AnalyzerService
from pr_insight_engine.complexity.complexity_service import ComplexityService
from pr_insight_engine.scoring.risk_engine import RiskEngine

def run_pipeline_test():
    print("\n=== PR Insight Engine - Phase 4.5 Test ===\n")

    #step 1: detect changed files
    parser= GitDiffParser(".")
    diffs=parser.parse()
    if not diffs:
        print("no uncommitted changes detected")
        return
    
    analyzer=AnalyzerService()
    complexity_service= ComplexityService()
    risk_engine= RiskEngine()

    #step 2: analyze each changed file
    for d in diffs:
        print(f"\nAnalyzing file: {d.file_path}")
        
        # --- static analysis ---
        analyzer_summary= analyzer.analyze_file(d.file_path)
        print(f"  Total findings: {analyzer_summary.total_findings}")
        print(f"  Semgrep findings: {analyzer_summary.semgrep_findings}")
        print(f"  Bandit findings: {analyzer_summary.bandit_findings}")

        # --- complexity analysis ---
        complexity_summary= complexity_service.analyze_file(d.file_path)
        print(f"  Avg complexity: {complexity_summary.average_complexity:.2f}")
        print(f"  Max complexity: {complexity_summary.max_complexity}")

        #--- risk scoring ---
        risk = risk_engine.compute_file_risk(
            analyzer_summary,
            complexity_summary,
        )

        print(f" Risk score: {risk.numeric_score}")
        print(f" Risk level: {risk.risk_level}")

        print("-" * 60)

if __name__ == "__main__":
    run_pipeline_test()

#test 4.5
