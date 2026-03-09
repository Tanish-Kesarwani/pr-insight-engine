from pr_insight_engine.diff.diff_parser import GitDiffParser
from pr_insight_engine.analyzers.analyzer_service import AnalyzerService
from pr_insight_engine.complexity.complexity_service import ComplexityService
from pr_insight_engine.scoring.risk_engine import RiskEngine
from pr_insight_engine.scoring.pr_risk_aggregator import PRRiskAggregator
from pr_insight_engine.context.context_analyzer import ContextAnalyzer
from pr_insight_engine.explain.explanation_engine import ExplanationEngine
from pr_insight_engine.scoring.merge_recommender import MergeRecommender
from pr_insight_engine.context.test_mismatch_detector import TestMismatchDetector
from pr_insight_engine.explain.heatmap_generator import HeatmapGenerator
from pr_insight_engine.explain.risk_table_generator import RiskTableGenerator
from pr_insight_engine.explain.report_generator import ReportGenerator

def run_pipeline_test():
    print("\n=== PR Insight Engine - Phase 11 Test ===\n")

    # Step 1: detect changed files
    parser = GitDiffParser(".")
    diffs = parser.parse()

    if not diffs:
        print("No uncommitted changes detected.")
        return

    # --- initialize services ---
    analyzer = AnalyzerService()
    complexity_service = ComplexityService()
    risk_engine = RiskEngine()
    pr_aggregator = PRRiskAggregator()
    context_analyzer = ContextAnalyzer()
    explanation_engine = ExplanationEngine()
    merge_recommender = MergeRecommender()
    test_mismatch_detector = TestMismatchDetector()
    heatmap_generator = HeatmapGenerator()
    risk_table_generator = RiskTableGenerator()
    report_generator = ReportGenerator()

    file_risks = []

    # ✅ PR-level test mismatch detection
    changed_paths = [d.file_path for d in diffs]
    test_mismatch_result = test_mismatch_detector.analyze(changed_paths)

    # Step 2: analyze each changed file
    for d in diffs:
        print(f"\nAnalyzing file: {d.file_path}")

        # --- static analysis ---
        analyzer_summary = analyzer.analyze_file(d.file_path)
        print(f"  Total findings: {analyzer_summary.total_findings}")
        print(f"  Semgrep findings: {analyzer_summary.semgrep_findings}")
        print(f"  Bandit findings: {analyzer_summary.bandit_findings}")

        # --- complexity analysis ---
        complexity_summary = complexity_service.analyze_file(d.file_path)
        print(f"  Avg complexity: {complexity_summary.average_complexity:.2f}")
        print(f"  Max complexity: {complexity_summary.max_complexity}")

        # --- context analysis ---
        context = context_analyzer.analyze_file(d.file_path)
        print(f"  Context tags: {context.tags}")
        print(f"  Context weight: {context.weight}")

        # --- risk scoring ---
        risk = risk_engine.compute_file_risk(
            analyzer_summary,
            complexity_summary,
            context.weight,
        )

        file_risks.append(risk)

        print(f"  Risk score: {risk.numeric_score}")
        print(f"  Risk level: {risk.risk_level}")

        # --- explanation ---
        explanation = explanation_engine.generate_file_explanation(
            analyzer_summary,
            complexity_summary,
            context,
        )

        print("  Explanation:")
        for msg in explanation.messages:
            print(f"    - {msg}")

        print("-" * 60)

    # --- PR level risk ---
    pr_risk = pr_aggregator.compute_pr_risk(file_risks)

    print("\n=== PR Risk Summary ===")
    print(f"PR Risk score: {pr_risk.numeric_score}")
    print(f"PR Risk level: {pr_risk.risk_level}")
    print("=" * 60)

    risk_table_generator.generate(file_risks)

    # ✅ test mismatch output
    print("\n=== Test Coverage Signal ===")
    print(f"Test mismatch detected: {test_mismatch_result.mismatch}")

    # --- merge recommendation ---
    recommendation = merge_recommender.recommend(pr_risk.risk_level)

    print("\n=== Merge Recommendation ===")
    print(f"Decision: {recommendation.decision}")
    print(f"Message: {recommendation.message}")
    print("=" * 60)

    report_generator.generate(pr_risk, file_risks, test_mismatch_result.mismatch, recommendation)


if __name__ == "__main__":
    run_pipeline_test()