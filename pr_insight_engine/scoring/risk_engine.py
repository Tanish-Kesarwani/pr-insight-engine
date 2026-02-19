from pr_insight_engine.analyzers.analyzer_models import AnalyzerSummary
from pr_insight_engine.complexity.complexity_models import ComplexitySummary
from .risk_models import RiskScore

class RiskEngine:
    """
    Computest contextual risk score using multiple signals
    """
    def compute_file_risk(
            self,
            analyzer_summary: AnalyzerSummary,
            complexity_summary: ComplexitySummary,
            context_weight: float = 1.0,
    ) -> RiskScore:
        score = 0.0

        # --- signal 1: analyzer findings ---
        score+=analyzer_summary.total_findings*5

        # --- signal 2: severity weighting ---
        for finding in analyzer_summary.findings:
            sev= (finding.severity or "").upper()

            if sev == "HIGH":
                score+=15
            elif sev== "MEDIUM":
                score+=8
            elif sev== "LOW":
                score+=3

        # --- signal 3: complexity ---
        max_complexity = complexity_summary.max_complexity

        if max_complexity >= 15:
            score+=20
        elif max_complexity >= 10:
            score+=10
        elif max_complexity >=6:
            score+=4

        # --- apply context weighting ---
        score*=context_weight
        
        # --- clamp score ---
        score=min(score, 100)

        # --- map to risk level ---
        if score>= 50:
            level ="HIGH"
        if score >= 20:
            level ="MEDIUM"
        else:
            level="LOW"
        
        return RiskScore(
            file_path=analyzer_summary.file_path,
            numeric_score=round(score, 2),
            risk_level=level,
        )