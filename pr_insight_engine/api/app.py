from fastapi import FastAPI

from pr_insight_engine.diff.diff_parser import GitDiffParser
from pr_insight_engine.analyzers.analyzer_service import AnalyzerService
from pr_insight_engine.complexity.complexity_service import ComplexityService
from pr_insight_engine.scoring.risk_engine import RiskEngine
from pr_insight_engine.scoring.pr_risk_aggregator import PRRiskAggregator
from pr_insight_engine.context.context_analyzer import ContextAnalyzer
from pr_insight_engine.scoring.merge_recommender import MergeRecommender
from pr_insight_engine.api.api_models import(PRAnalysisRequest, PRAnalysisResponse)

app= FastAPI(title="PR Insight Engine API")

@app.post("/analyzer_pr", response_model=PRAnalysisResponse)
def analyze_pr(request: PRAnalysisRequest):
    parser= GitDiffParser(request.repo_path)
    diffs= parser.parse()

    if not diffs:
        return PRAnalysisResponse(
            pr_risk_score= 0.0,
            pr_risk_level= "LOW",
            decision= "SAFE_TO_MERGE",
            message= "No changes detected.",
        )
    analyzer= AnalyzerService()
    complexity_service= ComplexityService()
    risk_engine= RiskEngine()
    pr_aggregator= PRRiskAggregator()
    context_analyzer= ContextAnalyzer()
    merge_recommender= MergeRecommender()

    file_risks= []

    for d in diffs:
        analyzer_summary= analyzer.analyze_file(d.file_path)
        complexity_summary= complexity_service.analyze_file(d.file_path)
        context= context_analyzer.analyze_file(d.file_path)

        risk= risk_engine.compute_file_risk(
            analyzer_summary, complexity_summary, context.weight,
        )
        file_risks.append(risk)

    pr_risk= pr_aggregator.compute_pr_risk(file_risks)
    recommendation=merge_recommender.recommend(pr_risk.risk_level)

    return PRAnalysisResponse(
        pr_risk_score=pr_risk.numeric_score,
        pr_risk_level=pr_risk.risk_level,
        decision=recommendation.decision,
        message=recommendation.message,
    )